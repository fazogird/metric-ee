# 11 — Spatial delapsing (lat/lon bo'yicha temperatura trendi)

> **Manba fayl:** `lapsed_surface_regions.py` (muallif: Peter ReVelle, 2019)
> **Ishlatilishi:** `EEFlux.spatial_lapse_props`, `_spatial_lapse`, `_total_lapse`, `ts_dem_latlon`, `spatial_regression_coeffs`

---

## 1. Feynman tushuntirish: "Qiyshiq pol"

Landsat sahnasi 185 × 180 km. Bu masofada **havo massasi** ham o'zgaradi: shimolda salqinroq, dengiz/ko'l yaqinida namroq, cho'l chekkasida issiqroq. Natijada bir xil sug'orilgan bedaning $T_s$ i sahnaning bir chetida 300 K, boshqasida 304 K bo'lishi mumkin — **ET farqi bo'lmasa ham**.

Balandlik bo'yicha delapsing ([03](03_surface_temperature.md)) — vertikal tuzatish. Spatial delapsing — **gorizontal** tuzatish: "pol qiyshiq" — uni tekislaymiz.

G'oya:
1. Har 16×16 blokda **to'liq qoplangan** (NDVI > 0.8) ekin/o'rmon piksellari temperaturasini topamiz — ular deyarli bir xil ETrF ga ega, demak temperatura farqi = havo massasi farqi.
2. $T_{fc} = c_1\lambda + c_2\varphi + c_3$ tekislikni moslaymiz (robust regression).
3. Har piksel temperaturasidan tekislik og'ishini ayiramiz.

---

## 2. Algoritm qadamlari

### 2.1 Land use soddalashtirish

```python
remapped = landuse.remap([...], [...])   # 41/42/43 → 41 (o'rmon), 81/82 → 81 (Ag), qolgani → 0
```

### 2.2 Bloklarni sanash — `count_filter_blocks`

Har blokda (scale 120 m) count:

| Band | Shart |
|---|---|
| `ag` | NDVI > 0.8 ∧ Ag |
| `forest` | NDVI > 0.8 ∧ o'rmon |
| `ag_areas` | NDVI ≥ 0.2 ∧ Ag (faol ekin maydoni) |

O'rmon bloklari: count ≥ max/10 yoki ≥ 20.

### 2.3 Ag yoki o'rmon? — `filter_ag_or_forest_blocks`

$$\text{ag\_block\_check} = (\sum ag > 1)\ \land\ (N_{ag\_area\ blocks} > 10)$$

Ag yetarli bo'lsa o'rmon bloklari chiqariladi. `high_block_check` = Ag bloklar > 40 yoki o'rmon bloklar > 40.

### 2.4 Full cover temperaturalari — `get_full_cover_temperatures`

Maskalar:

| Mask | Ag rejim | O'rmon/aralash |
|---|---|---|
| NDVI | 0.80 < NDVI < 0.85 (`high_block_check` → > 0.80) | > 0.80 |
| Albedo | 0.18 < α < 0.25 | α > 0.10 |
| Slope | < 5° | < 5° |
| $T_s$ | > 275 K | > 275 K |
| Bulut | `bqa_mask == 0` | |

Og'irlik: $w_{slope} = \mathrm{clamp}(2\cdot\frac{1}{|s - 0.01|},\ 0.01,\ 1)$

Reduktor: `percentile([10, 50]).combine(mean)` → `ts_dem10`, `ts_dem` (median), `elev` (mean), `splitWeights()`.

> Kirish temperatura — `surface_temperature_dem` (faqat balandlik bo'yicha delapse qilingan, std lapse).

### 2.5 Outlier filtrlash — `filter_ag_blocks`

- Full cover bloklar: `ag > mean(ag)/10` yoki `ag ≥ 10` yoki `forest > 0`
- Ag maydon bloklari (`ag_elev_blocks`): `ag_areas > mean/10`

### 2.6 Fallback va datum blok

- Blok topilmasa → butun sahna = 1 blok, `elev = datum` (`set_fallback_datum_block`).
- **Datum blok** (`find_datum_block`): o'rtacha balandlikdan past bloklar ichidan birinchisi.

> 🐛 `full_cover_temps.sort('elev', False)` natijasi o'zgaruvchiga yozilmagan → saralash **ta'sir qilmaydi**; datum blok = filtrlangan kolleksiyaning ixtiyoriy birinchi elementi.

### 2.7 Blok qiymatlari — `set_block_values`

$$T_{block} = \begin{cases} p_{10}(T_{s,dem}), & \text{high\_block\_check} \\ p_{50}(T_{s,dem}), & \text{aks holda}\end{cases}$$

+ blok centroid'ining `longitude`, `latitude`, `constant = 1`.

### 2.8 Regressiya

```python
regress_coeffs = full_cover_temps.reduceColumns(
    ee.Reducer.robustLinearRegression(3, 1), ['longitude', 'latitude', 'constant', 'ts_dem'])
```

$$T_{fc}(\lambda,\varphi) = c_\lambda\,\lambda + c_\varphi\,\varphi + c_0\qquad(\lambda,\varphi\ \text{— gradus, WGS84})$$

**Spatial lapse:**

$$\Delta T_{sp}(\lambda,\varphi) = T_{fc}(\lambda,\varphi) - T_{fc}(\lambda_d,\varphi_d)$$

($\lambda_d,\varphi_d$ — datum blok centroid'i, `reduceRegion(first)` bilan).

$$T_{s,dem,latlon} = T_{s,dem} - \Delta T_{sp}$$

Eksport uchun ishorasi teskari: `spatial_lapse = -ΔT_sp` → `_total_lapse = std_lapse + spatial_lapse` ([03](03_surface_temperature.md#34-standart-va-umumiy-lapse--eefluxpy)).

---

## 3. Sifat tekshiruvlari (regression checks)

Agar **birortasi** True bo'lsa → $\Delta T_{sp} = 0$, `regress_success = 0`:

| # | Tekshiruv | Shart | Ma'no |
|---|---|---|---|
| 1 | `regress_failed` | residual + $c_\lambda$ = 0 | Regressiya ishlamadi |
| 2 | `elev_diff_check` | $(2\sigma_{z,ag}) - (\sigma_{z,fc} + \bar z_{fc} - z_{fc,min}) > 500$ ∧ tog' | Full cover bloklar Ag balandlik diapazonini qoplamaydi |
| 3 | `tot_dist_check` | $d_{fc,max}/d_{ag,max} < 0.75$ ∨ $d_{fc,max} < 50$ km | Bloklar sahna bo'ylab yetarli tarqalmagan |
| 4 | `min_variance_check` | $\sigma_{T,fc} < 1$ K ∧ $\Delta z_{fc} > 1000$ ∧ tog' | Trend yo'q, overfitting xavfi |
| 5 | `block_counts_check` | $N < 10$ (bulut ≤ 50%) yoki $N < 5$ (bulut > 50%) | Erkinlik darajasi kam |
| 6 | `high_residuals` | residual > 3 | Shovqinli |
| 7 | `lat_lon_total_check` | $\vert c_\lambda\vert  + \vert c_\varphi\vert  > 10$ K/° | Fizik ma'nosiz qiyalik |
| 8 | `lapsed_cold_range_diff_check` | sirt max − blok max > 4 ∨ sirt min − blok min < −4 | Ekstrapolyatsiya haddan ziyod |

Masofalar: `datum_block.distance(block, maxError=1000, proj=Ts_crs)` — **Landsat UTM proyeksiyasida** (metr).

> 🌍 **CRS eslatma:** regressiya koordinatalari **gradus** (`pixelLonLat`), masofalar esa **UTM metr**. $c_\lambda$, $c_\varphi$ birligi — K/gradus. O'zbekiston kengligida (~41°) 1° uzunlik ≈ 84 km, 1° kenglik ≈ 111 km — demak koeffitsientlar anizotrop. Kod buni hisobga olmaydi (kichik sahna uchun yetarli yaqinlashish).

`calculate_lapsed_surface_min_max` — sirt min/max ni `projects/openet/assets/features/water_mask` (AQSh!) bilan suvni chiqarib hisoblaydi, scale = 8 × 120 = 960 m.

> ⚠️ AQShdan tashqarida `water_mask` asseti qamrovsiz bo'lishi mumkin → `combine({..0..})` fallback ishlaydi → 8-tekshiruv buzilishi mumkin. Lokal ishlatishda bu maskani JRC GSW bilan almashtirish tavsiya etiladi.

---

## 4. Chiqish lug'ati (`spatial_lapse_props`)

| Kalit | Tavsif |
|---|---|
| `lapsed_surface` | $T_{fc}(\lambda,\varphi)$ tasviri |
| `ts_dem_latlon` | Spatial delapsed temperatura |
| `regress_coeffs` | `{coefficients: [[cλ],[cφ],[c0]], residuals: [...]}` |
| `block_counts` | Regressiyadagi bloklar soni |
| `full_cover_temps` | Bloklar FC |
| `regress_success` | 1 = qo'llandi, 0 = rad etildi |
| `spatial_lapse` | $-\Delta T_{sp}$ (0 agar rad) |
| `spatial_lapse_raw` | $-\Delta T_{sp}$ (tekshiruvsiz) |
| `ag_elev_diff` | $2\sigma_{z,ag}$ — hot piksel tanlashda ishlatiladi |
| `cold_ts_dem_stats` | sd/min/mean/max + sirt min/max |

`set_spatial_regress_coeffs` → eksport xususiyatlari: `lon_coeff`, `lat_coeff`, `const_coeff`, `regress_resid`, `regress_blocks`, `SPATIAL_DELAPSING`.

---

## 5. Pixel selection bilan bog'liqlik

- `ts_dem_latlon` = hot/cold tanlashda asosiy temperatura
- `spatially_lapsed` flag → hot temperatura uchun sahna persentili yoki blok-og'irlangan o'rtacha tanlash ([10](10_pixel_selection.md#43--hot-piksel--get_ideal_hot_temperature))
- `ag_elev_diff ≥ 1000 m` → blok-og'irlangan usul
