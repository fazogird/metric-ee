# 01 — Preprocessing: Landsat C2 SR → model kirish ma'lumoti

> **Manba fayllar:** `openet/eemetric/eeflux.py` (`from_landsat_c2_sr`, `get_matched_c2_toa_image`, `set_fallback_toa_image`, `set_default_cloudmask_args`, `cloud_mask_openet`, `mask`), `openet/eemetric/surface_reflectance.py`, `openet-core/openet/core/common.py` (`landsat_c2_sr_cloud_mask`, `landsat_c2_sr_lst_correct`, `landsat_c2_sr_emissivity_correct`)

---

## 1. Feynman tushuntirish: "Oshxonaga mahsulot olib kirish"

Tasavvur qiling, METRIC — bu oshpaz. U ovqat (ET) pishirishdan oldin mahsulotlarni (Landsat piksellarini) **yuvadi, tozalaydi va bir xil o'lchamga keltiradi**:

1. **Raw DN → fizik birlik** (reflectance 0–1, temperatura Kelvin) — "kartoshkani po'stidan tozalash".
2. **Bulut maskasi** — "chirigan kartoshkani tashlab yuborish".
3. **Bandlarni universal nomga o'tkazish** (`SR_B4` → `red`) — Landsat 5/7/8/9 qaysi bo'lmasin, oshpaz bir xil retseptdan foydalanadi.
4. **LST ni qayta hisoblash** (C2 LST correction) — USGS bergan temperaturani ASTER emissivity bilan aniqlashtirish.

---

## 2. Kirish nuqtasi: `EEFlux.from_landsat_c2_sr()`

```python
import openet.eemetric as model
img = model.Image.from_landsat_c2_sr('LANDSAT/LC08/C02/T1_L2/LC08_044033_20170716')
# yoki
img = model.Image.from_image_id('LANDSAT/LC08/C02/T1_L2/LC08_044033_20170716')
```

`from_image_id` → `_COLLECTION_METHODS` lug'atidan kolleksiya ID bo'yicha metod tanlaydi. Qo'llab-quvvatlanadigan kolleksiyalar:

| Kolleksiya | Metod |
|---|---|
| `LANDSAT/LC09/C02/T1_L2` | `from_landsat_c2_sr` |
| `LANDSAT/LC08/C02/T1_L2` | `from_landsat_c2_sr` |
| `LANDSAT/LE07/C02/T1_L2` | `from_landsat_c2_sr` |
| `LANDSAT/LT05/C02/T1_L2` | `from_landsat_c2_sr` |
| `LANDSAT/LT04/C02/T1_L2` | `from_landsat_c2_sr` |

### 2.1 Qadamlar ketma-ketligi

```text
sr_image (C2 L2)
   │
   ├─► QA_PIXEL  ───────────────► bqa_band
   ├─► get_matched_c2_toa_image ─► TOA (LANDSAT_SCENE_ID bo'yicha)
   │        └─► set_fallback_toa_image (TOA topilmasa — shu path/row dan "to'ldiruvchi")
   │                 └─► simpleCloudScore(TOA).select('cloud')   (TOA yo'q bo'lsa → 0)
   ├─► band rename + scale/offset ─► prep_image
   ├─► landsat_c2_sr_cloud_mask (openet-core) → .Not() → cloud_mask (1 = bulut)
   └─► landsat_c2_sr_lst_correct (openet-core) → surface_temperature (K)
```

### 2.2 Bandlarni universal nomga o'tkazish

| Sputnik | blue | green | red | nir | swir1 | swir2 | thermal |
|---|---|---|---|---|---|---|---|
| Landsat 4/5/7 | SR_B1 | SR_B2 | SR_B3 | SR_B4 | SR_B5 | SR_B7 | ST_B6 |
| Landsat 8/9 | SR_B2 | SR_B3 | SR_B4 | SR_B5 | SR_B6 | SR_B7 | ST_B10 |

### 2.3 Scale / offset (Collection 2 Level 2 standarti)

$$\rho_{SR} = DN \times 0.0000275 - 0.2$$

$$T_{ST}\,[K] = DN \times 0.00341802 + 149.0$$

```python
prep_image = (
    sr_image.select(input_bands.get(spacecraft_id), output_bands)
    .multiply([0.0000275]*6 + [0.00341802, 1])
    .add([-0.2]*6 + [149.0, 1])
)
```

> ⚠️ **Aniqlik eslatmasi:** offset `-0.2` sabab, juda qorong'i piksellarda (suv, soya) reflectance **manfiy** bo'lishi mumkin. Kod buni clamp qilmaydi — keyingi bosqichlarda (NDVI `.clamp(-1,1)`, LAI `.max(0)`) bilvosita cheklanadi.

### 2.4 Albedo og'irlik koeffitsientlari (`wb`)

Barcha Landsat uchun bir xil (Tasumi et al., 2008 ga yaqin), `image.set({'wb': ...})` orqali tasvir xususiyatiga yoziladi:

| blue | green | red | nir | swir1 | thermal | swir2 |
|---|---|---|---|---|---|---|
| 0.2545 | 0.1486 | 0.148 | 0.31 | 0.1025 | **0** | 0.0364 |

> Thermal bandi tartibda 6-o'rinda turadi, shuning uchun uning og'irligi `0` — albedo summasiga kirmaydi (qarang: [02_albedo_ndvi_lai.md](02_albedo_ndvi_lai.md)).

---

## 3. Bulut maskasi (Cloud mask)

### 3.1 Asosiy maska — `openet.core.common.landsat_c2_sr_cloud_mask`

eeMETRIC default argumentlari (`set_default_cloudmask_args`):

| Flag | eeMETRIC default | Ma'nosi |
|---|---|---|
| `cirrus_flag` | **True** | Cirrus (faqat L8/L9) |
| `dilate_flag` | **True** | Dilated cloud bit |
| `shadow_flag` | **True** | Bulut soyasi |
| `snow_flag` | **False** | Qor maskalanmaydi (METRIC uchun qor — signal!) |

Core funksiya `QA_PIXEL` bitlaridan maska quradi va **0 = bulut, 1 = toza** qaytaradi. eeMETRIC uni `.Not()` bilan teskari qiladi → `cloud_mask` da **1 = bulut**.

### 3.2 Production maska — `cloud_mask_openet`

OpenET eksporti uchun maska morfologik "tozalanadi":

```python
fmask_unmasked = fmask.unmask(0)                     # SLC-off gap muammosi uchun
fmask_despeckled = (fmask_unmasked
    .focal_mean(1.5, 'square', 'pixels').gt(1/3.0)   # ≤3 pikselli "dog'"larni olib tashlash
    .updateMask(fmask.mask()))
fmask_smoothed = fmask_despeckled.focal_max(7.5, 'square', 'pixels')   # bulutni kengaytirish (dilate)
fmask_smoothed = fmask_smoothed.focal_mode(7.5, 'square', 'pixels')    # yaqin bulutlarni birlashtirish
```

| Bosqich | Operatsiya | Kernel |
|---|---|---|
| Despeckle | `focal_mean > 1/3` | 3×3 kvadrat (r=1.5 px) |
| Dilate | `focal_max` | 15×15 (r=7.5 px ≈ 225 m) |
| Merge | `focal_mode` | 15×15 |

`mask` xususiyati: `cloud_mask_openet.eq(0).uint8()` → **1 = yaroqli piksel**. `calculate()` da `et_fraction` so'ralsa, chiqish shu maska bilan `updateMask` qilinadi.

> 💡 **Nega `unmask(0)`?** Landsat 7 SLC-off chiziqlarida EE masklangan piksellarni focal operatsiyada e'tiborsiz qoldiradi va kichik klasterlar "omon qoladi". Avval 0 bilan to'ldirib, keyin asl maskani qaytarish shu "bug"ni yopadi.

### 3.3 `simpleCloudScore`

TOA tasvirdan `ee.Algorithms.Landsat.simpleCloudScore(toa).select('cloud')` olinadi (0–100). Agar mos TOA topilmasa (`toa_coll_size_check == 1`), qiymat **0** ga tenglashtiriladi. Bu ball keyinchalik pixel selection'da ishlatiladi.

---

## 4. TOA tasvirni topish va "fallback"

```python
scene_id = input_image.get('LANDSAT_SCENE_ID')
coll2 = L5_TOA.merge(L7_RT_TOA).merge(L8_RT_TOA).merge(L9_TOA)
matched = coll2.filter(ee.Filter.eq('LANDSAT_SCENE_ID', scene_id)).first()
```

`set_fallback_toa_image` — agar `matched` `null` bo'lsa, shu WRS **path/row** dan ixtiyoriy TOA olinadi va `toa_coll_size_check = 1` bayrog'i qo'yiladi. Bu server-side "if/else" ning klassik EE hiylasi: `FeatureCollection([coll_image, toa_image]).size() < 2` → TOA yo'q.

---

## 5. C2 LST correction (default: `_C2_LST_CORRECT = True`)

USGS C2 `ST_B10` o'z emissivity'sini ishlatadi. OpenET Allen & Kilic (2022) usulida **ASTER GED** asosida emissivity'ni qayta hisoblaydi.

### 5.1 Emissivity — `landsat_c2_sr_emissivity_correct`

**1-qadam. ASTER → Landsat ekvivalent emissivity** (Malakar et al., 2018, Eq. 4):

$$\varepsilon_{GED} = c_{13}\,\varepsilon_{13} + c_{14}\,\varepsilon_{14} + c$$

| Sputnik | c13 | c14 | c |
|---|---|---|---|
| L4 | 0.3222 | 0.6498 | 0.0272 |
| L5 | −0.0723 | 1.0521 | 0.0195 |
| L7 | 0.2147 | 0.7789 | 0.0058 |
| L8 | 0.6820 | 0.2578 | 0.0584 |
| L9 | 0.7689 | 0.1843 | 0.0457 |

**2-qadam. ASTER vegetation fraction:**

$$f_{c,ASTER} = \mathrm{clamp}\!\left(\frac{NDVI_{ASTER} - 0.15}{0.65},\,0,\,1\right)$$

**3-qadam. Bare soil emissivity** (vegetatsiya ulushini "ayirib tashlash"):

$$\varepsilon_{soil} = \frac{\varepsilon_{GED} - 0.9798\,f_{c,ASTER}}{1 - f_{c,ASTER}}$$

- agar $f_{c,ASTER} > 0.8$ → $\varepsilon_{soil} = 0.97$ (maxraj noturg'un)
- NoData → `unmask(0.97)` (**gap-filling**)
- `resample('bilinear')` (0.1° GED katakchalarini silliqlash)

**4-qadam. Landsat emissivity** (joriy NDVI bilan):

$$f_{c} = \mathrm{clamp}\!\left(\frac{NDVI - 0.15}{0.65},0,1\right),\qquad \varepsilon_{LS} = (1-f_c)\,\varepsilon_{soil} + 0.99\,f_c$$

### 5.2 LST — `landsat_c2_sr_lst_correct`

**Yuzadan chiqqan radiance** (atmosfera korreksiyasi C2 ning `ST_URAD`, `ST_ATRAN`, `ST_DRAD` bandlari bilan):

$$R_c = \frac{L_{TOA} - L_{\uparrow}}{\tau} - (1-\varepsilon_{LS})\,L_{\downarrow}$$

bu yerda $L_{TOA} = DN \cdot M_L + A_L$ (Level-1 tasvirdan), $L_\uparrow = ST\_URAD\times 0.001$, $\tau = ST\_ATRAN \times 0.0001$, $L_\downarrow = ST\_DRAD \times 0.001$.

**Plank inversiyasi:**

$$T_s = \frac{K_2}{\ln\!\left(\dfrac{\varepsilon_{LS}\,K_1}{R_c} + 1\right)}$$

| Sputnik | K1 | K2 |
|---|---|---|
| L4/L5 | 607.76 | 1260.56 |
| L7 | 666.09 | 1282.71 |
| L8 | 774.8853 | 1321.0789 |
| L9 | 799.0284 | 1329.0284 |

```python
return (ls_em.multiply(k1).divide(rc).add(1.0).log().pow(-1)
        .multiply(k2).rename('lst'))
```

> 🔧 `c2_lst_correct=False` berilsa, to'g'ridan-to'g'ri USGS `ST_B*` ishlatiladi: `lst = sr_image.select('thermal')`.

---

## 6. Legacy: METRIC'ning o'z atmosfera korreksiyasi (`surface_reflectance.py`)

> ⚠️ C2 SR yo'lida **ishlatilmaydi** — `surface_reflectance` tayyor holda `cls(...)` ga beriladi. Lekin `EEFluxFlat` va eski Collection 1 oqimi uchun kodda saqlangan. Ilmiy tushunish uchun foydali.

### 6.1 Keng polosali transmissivity (Allen et al., 2007, Eq. 12–13)

Atmosfera bosimi (FAO-56):

$$P = 101.3\left(\frac{293 - 0.0065\,z}{293}\right)^{5.26}\quad [kPa]$$

Precipitable water: $W = 0.14\,e_a\,P + 2.1$

$$\tau_{in,b} = C_1 \exp\!\left[\frac{C_2\,P}{K_t\cos\theta_{hor}} - \frac{C_3 W + C_4}{\cos\theta_{hor}}\right] + C_5$$

$$\tau_{out,b} = C_1 \exp\!\left[\frac{C_2\,P}{K_t\cos\eta} - \frac{C_3 W + C_4}{\cos\eta}\right] + C_5,\quad \eta\approx 0\ (nadir)$$

$C_1..C_5,\ C_b$ — har bir band uchun tasvir xususiyatlaridan (`img.get('c1')` ...), $K_t = 1$ (toza havo).

### 6.2 Surface reflectance (flat, Eq. 11, 14)

$$\rho_{s,b} = \frac{\rho_{t,b} - C_b\,(1 - \tau_{in,b})}{\tau_{in,b}\,\tau_{out,b}}$$

### 6.3 Mountain versiya (`calculate_surface_reflectance_mm_general`)

Diffuse va beam transmittansni ajratadi:

$$\tau_{diff} = \min\!\left(\max\!\left(\frac{a_{1b} - a_{2b}\,\tau_{in}}{1-a_{2b}},\,0.001\right),\,\tau_{in}\right),\qquad \tau_{beam} = \max(\tau_{in} - \tau_{diff},\,0.001)$$

$a_{1b} = [0.7,0.7,0.7,0.68,0.68,0.68,0.68]$, $a_{2b} = [0.74,0.74,0.74,0.76,0.76,0.76,0.76]$

Sky-view factor (slope $s$ gradusda): $f_{sky} = 0.75 + 0.25\cos s - 0.5\,s/180$

Terrain reflectance: $\rho_{terr} = \rho_{nadir}\,(1 + 0.007\,\arctan(\tfrac{\tan s}{1+\tan s})\cdot \max(0, -\cos|\psi - \psi_{sun}|))$

$$\rho_s = \frac{L^*\cos s / \tau_{out}}{\cos\theta_{mtn}\cos s\,\tau_{beam} + \cos\theta_{flat}\,\tau_{diff}\,f_{sky} + \rho_{terr}\cos\theta_{flat}\,\tau_{in}\,(1-f_{sky})}$$

bu yerda $L^* = \max\!\left(\dfrac{\pi L}{d_r\,ESUN} - C_b(1-\tau_{in})\cos\theta_{flat},\ 0.3\dfrac{\pi L}{d_r\,ESUN}\right)$, $d_r = 1 + 0.033\cos(2\pi\,DOY/365)$.

---

## 7. CRS / NoData eslatmalari

| Masala | Kodda qanday hal qilingan |
|---|---|
| **CRS** | Landsat native UTM (masalan EPSG:326xx) saqlanadi; ASTER GED `EPSG:4326` da 0.1° to'rga "snap" qilinib clip qilinadi, so'ng `bilinear` resample. Hisob-kitob EE tomonidan chiqish proyeksiyasida bajariladi. |
| **NoData (QA_PIXEL)** | Core maska `updateMask(QA_PIXEL.mask())` — tasvir chegarasidan tashqari piksellar masklangan qoladi. |
| **SLC-off gap** | `unmask(0)` → focal → `updateMask(fmask.mask())` |
| **Emissivity gap** | `unmask(0.97)` |
| **TOA yo'q** | fallback TOA + `cloud score = 0` |
