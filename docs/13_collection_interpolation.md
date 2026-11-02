# 13 — Collection va vaqt bo'yicha interpolyatsiya (kunlik / oylik / yillik ET)

> **Manba fayllar:** `collection.py` (`Collection`), `interpolate.py` (`from_scene_et_fraction`), `openet-core/openet/core/interpolate.py` (`daily`, `aggregate_to_daily`)

---

## 1. Feynman tushuntirish: "Kinodagi bo'sh kadrlarni to'ldirish"

Landsat har 8–16 kunda bir marta o'tadi (L8+L9 birgalikda 8 kun), bulutli kunlar esa tushib qoladi. Bizda ETrF ning "siyrak kadrlari" bor. Oylik ET uchun **har kun** ET kerak.

Yechim:
1. **ET fraction** (nisbat) sekin o'zgaradi (o'simlik fenologiyasi) → kunlar orasida **chiziqli interpolyatsiya** qilsa bo'ladi.
2. **Reference ET** (ob-havo) har kuni keskin o'zgaradi → u **kunlik o'lchangan** gridMET/ERA5 dan olinadi.
3. Har kun: $ET_d = EToF_d^{interp}\times ET_{o,d}$, keyin yig'iladi.

> ❌ ET ning o'zini interpolyatsiya qilish xato: yomg'irli/bulutli kunlarda ETo past, lekin interpolyatsiya buni "ko'rmaydi". Fraksiya interpolyatsiyasi esa ob-havo o'zgarishini saqlab qoladi.

---

## 2. `Collection` klassi

```python
import ee, openet.eemetric as model
ee.Initialize()

coll = model.Collection(
    collections=['LANDSAT/LC09/C02/T1_L2', 'LANDSAT/LC08/C02/T1_L2'],
    start_date='2023-04-01', end_date='2023-10-01',       # end — eksklyuziv
    geometry=ee.Geometry.Point(69.24, 41.30),
    cloud_cover_max=70,
    et_reference_source='IDAHO_EPSCOR/GRIDMET', et_reference_band='eto',
    et_reference_factor=1.0, et_reference_resample='nearest',
    model_args={'conus_only': False},
)
overpass = coll.overpass(variables=['et_fraction', 'ndvi'])
monthly  = coll.interpolate(variables=['et', 'et_reference', 'et_fraction', 'count'],
                            t_interval='monthly', interp_days=32)
```

### 2.1 Validatsiyalar (`__init__`)

| Tekshiruv | Xato |
|---|---|
| Kolleksiya C2 L2 ro'yxatida emas | `ValueError` |
| Bir sputnik ikki marta (masalan LC08 TOA + SR) | `ValueError('duplicate landsat types')` |
| Sana formati `YYYY-MM-DD`, `start < end` | `ValueError` |
| `0 ≤ cloud_cover_max ≤ 100` | `ValueError` |
| `et_reference_factor ≥ 0`, son | `ValueError` |
| `et_reference_resample ∈ {nearest, bilinear, bicubic}` | `ValueError` |

### 2.2 Sputnik vaqt oynalari (avtomatik filtr)

| Sputnik | Ishlatiladigan davr |
|---|---|
| LT04 | 1982–1993 |
| LT05 | 1984 – **2011-12-31** (keyingi yomon tasvirlar chiqariladi) |
| LE07 | 1999 – **2021-12-31** (orbita drift) |
| LC08 | **2013-04-01** dan (pre-operational chiqariladi) |
| LC09 | **2022-01-01** dan |

### 2.3 `_build()`

```python
ee.ImageCollection(coll_id)
  .filterDate(start, end).filterBounds(geometry)
  .filterMetadata('CLOUD_COVER_LAND', 'less_than', cloud_cover_max)
  .filterMetadata('CLOUD_COVER_LAND', 'greater_than', -0.5)     # -1 (noma'lum) chiqariladi
  .filterMetadata('PROCESSING_LEVEL', 'equals', 'L2SP')          # faqat ST bandi borlar
  .map(lambda img: Image.from_landsat_c2_sr(img, **model_args)
                        .calculate(variables).updateMask(model_obj.mask))
```

`filter_args = {coll_id: ee.Filter}` — qo'shimcha filtr (masalan WRS path/row).

---

## 3. `Collection.interpolate()`

### 3.1 Sana kengaytirish

| `t_interval` | start | end |
|---|---|---|
| `annual` | yil boshi | keyingi yil boshi |
| `monthly` | oy boshi | keyingi oy boshi |
| `daily`/`custom` | o'zgarmaydi | |

Interpolyatsiya oynasi: $[start - interp\_days,\ end + interp\_days]$ (default **32 kun**) — chekka kunlar uchun "qo'shni" sahnalar kerak.

### 3.2 Interpolyatsiya qilinadigan o'zgaruvchilar

`_interp_vars = ['ndvi', 'et_fraction']` + har doim `time` (0 UTC millis). `et`/`et_reference` so'ralsa → `et_fraction` avtomatik qo'shiladi; `count` → `mask`.

### 3.3 Reference ET kolleksiyasi

```python
daily_et_ref_coll = ee.ImageCollection(source).filterDate(start, end).select([band], ['et_reference'])
if factor != 1: daily_et_ref_coll = daily_et_ref_coll.map(lambda i: i.multiply(factor)...)
```

---

## 4. Chiziqli interpolyatsiya — `openet.core.interpolate.daily`

Har bir **target** kun $t$ (reference ET tasviri) uchun:

1. `prev` = $[t - N, t)$ oralig'idagi sahnalar, vaqt bo'yicha saralangan → `mosaic()` (eng yaqini ustida)
2. `next` = $[t, t + N + 1)$ → `mosaic()`
3. Bo'sh bo'lsa — masklangan "dummy" tasvir qo'shiladi
4. **Gap-filling:** `prev` yo'q piksellarda `next` qiymati, va aksincha → chekkada **gorizontal chiziq** (konstanta ekstrapolyatsiya)

$$r(t) = \frac{t - t_{prev}}{t_{next} - t_{prev}},\qquad V(t) = V_{prev} + r(t)\,(V_{next} - V_{prev})$$

> 💡 **Piksel-darajasidagi interpolyatsiya:** `mosaic()` tufayli har piksel o'zining eng yaqin **bulutsiz** kuzatuvidan foydalanadi (`time` bandi ham piksel bo'yicha!). Bulut ostidagi piksel uzoqroq sanadan oladi — bu "per-pixel gap-filling".

5. Natija: interpolyatsiya qilingan bandlar + target (`et_reference`).

`use_joins=True` → `Join.saveAll('prev'/'next')` — xotira jihatidan samaraliroq.

### 4.1 ET hisoblash

$$ET_d = EToF_d \times ET_{o,d}$$

(`et_reference_resample` = bilinear/bicubic bo'lsa ETo avval resample qilinadi — 4 km gridMET ni 30 m ga silliq.)

---

## 5. Agregatsiya — `aggregate_image`

| Chiqish | Formula |
|---|---|
| `et` | $\sum_d ET_d$ |
| `et_reference` | $\sum_d ET_{o,d}$ |
| `et_fraction` | $\sum ET_d / \sum ET_{o,d}$ (**og'irlangan** o'rtacha, oddiy o'rtacha emas!) |
| `ndvi` | $\overline{NDVI_d}$ |
| `count` | davrdagi bulutsiz sahnalar soni (`aggregate_to_daily(mask)` → `count()`) |

`interp_properties`: `cloud_cover_max`, `collections`, `interp_days`, `interp_method`, `model_name`, `model_version` + `model_args`.

`system:index` formati: `YYYYMMdd` (daily/custom), `YYYYMM` (monthly), `YYYY` (annual).

---

## 6. `aggregate_to_daily` (openet-core)

Bir kunda bir nechta sahna (bitta path, qo'shni row'lar) → **o'rtacha** bitta tasvir, `system:time_start` = **0 UTC**. Chegaradagi ikki marta kuzatilgan piksellarni ikki marta sanamaslik uchun.

---

## 7. `interpolate.from_scene_et_fraction` (oldindan hisoblangan sahnalardan)

OpenET production oqimi: sahnalar avval asset sifatida eksport qilinadi, keyin bu funksiya bilan interpolyatsiya.

Farqlar `Collection.interpolate` dan:

| | `from_scene_et_fraction` |
|---|---|
| Kirish | Tayyor `et_fraction` sahnalar kolleksiyasi |
| `scale_factor_et_fraction` | xususiyatdan "unscale" (default 1.0) |
| `mask`, `time` bandlari | ichida yaratiladi (`interpolate_prep`) |
| `mask_partial_aggregations` | **True** (default): $count_{days} \ge N_{days} - 1$ bo'lmagan piksellar masklanadi |
| `use_joins` | default **True** |
| `t_interval` | `daily`, `monthly`, `custom` (annual yo'q) |
| `daily_count` | qo'shimcha chiqish (agregatsiya kunlari soni) |
| Reference ET parametrlari | avval `interp_args`, keyin `model_args` dan |

---

## 8. Aniqlik eslatmalari (NoData / gap-filling / CRS)

| Masala | Xatti-harakat |
|---|---|
| **Uzun bulutli davr** (> 32 kun) | Piksel masklanadi (`prev`/`next` ikkalasi dummy) → oylik `et` NoData. `mask_partial_aggregations` qisman oylarni ham kesadi. |
| **Mavsum chegarasi** | Faqat bir tomonda kuzatuv → konstanta ekstrapolyatsiya (ETf "tekis chiziq") |
| **Proyeksiya** | Interpolyatsiya natijasi — sahnalar UTM proyeksiyasida; `et_reference` — o'z grid'ida (gridMET EPSG:4326 ~4 km). Ko'paytirishda EE chiqish proyeksiyasiga qayta namunalaydi; `resample('bilinear')` "blok" artefaktlarini kamaytiradi. |
| **Ikki UTM zonasi** | Aralash zonali sahnalar `mosaic()` da default proyeksiya **WGS84 1°** bo'lishi mumkin — eksportda `crs` va `crsTransform`/`scale` ni **aniq** bering (masalan EPSG:32642, 30 m). |
| **0 UTC** | `time` bandi va target sanalar 0 UTC; gridMET `system:time_start` +6 UTC — kod izohida ochiq savol sifatida qayd etilgan. |
