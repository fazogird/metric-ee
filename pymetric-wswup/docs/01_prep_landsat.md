# 01 — Landsat sahnasini tayyorlash (pymetric, WSWUP)

> **Manba:** `code/support/et_image.py`, `code/prep_functions/landsat_prep_scene_func.py`, `code/support/et_numpy.py` (TOA/BT/Fmask funksiyalari)

---

## 1. Feynman tushuntirish

Landsat Level-1 fayli "xom" DN (raqamli son, 0–255 yoki 0–65535) beradi. Uni fizik birlikka (reflectance 0–1, temperatura K) o'tkazish uchun **MTL** metafaylidagi kalibratsiya koeffitsientlari kerak. `et_image.Image` klassi MTL'ni o'qiydi va har bir sputnik uchun to'g'ri koeffitsientlarni tanlaydi — bu sahnaning "pasporti".

---

## 2. `et_image.Image` — sahna pasporti

### 2.1 Qo'llab-quvvatlanadigan sensorlar

| Prefix | Tur | Termal band | Optik bandlar (TOA/SUR tartib) |
|---|---|---|---|
| LT04 | Landsat4 | 6 | 1, 2, 3, 4, 5, 7 |
| LT05 | Landsat5 | 6 | 1, 2, 3, 4, 5, 7 |
| LE07 | Landsat7 | 6 (`VCID_1`) | 1, 2, 3, 4, 5, 7 |
| LC08 | Landsat8 | 10 | 2, 3, 4, 5, 6, 7 |

> ⚠️ Faqat **Collection 1** papka nomi va **Landsat 4–8**. Landsat 9 va Collection 2 qo'llab-quvvatlanmaydi. USGS Collection 1 ni 2022-yil oxirida tarqatishdan to'xtatgan ([09](09_kuzatuvlar.md)).

### 2.2 Tasumi (2008) at-surface koeffitsientlari

L4/5/7 (band 1, 2, 3, 4, 5, 7):

| | b1 | b2 | b3 | b4 | b5 | b7 |
|---|---|---|---|---|---|---|
| $C_1$ | 0.987 | 2.319 | 0.951 | 0.375 | 0.234 | 0.365 |
| $C_2$ | −0.000710 | −0.000164 | −0.000329 | −0.000479 | −0.001012 | −0.000966 |
| $C_3$ | 0.000036 | 0.000105 | 0.00028 | 0.005018 | 0.004336 | 0.004296 |
| $C_4$ | 0.0880 | 0.0437 | 0.0875 | 0.1355 | 0.0560 | 0.0155 |
| $C_5$ | 0.0789 | −1.2697 | 0.1014 | 0.6621 | 0.7757 | 0.639 |
| $C_b$ | 0.640 | 0.31 | 0.286 | 0.189 | 0.274 | −0.186 |
| $w_b$ (albedo) | 0.254 | 0.149 | 0.147 | 0.311 | 0.103 | 0.036 |

L8 (band 2, 3, 4, 5, 6, 7):

| | b2 | b3 | b4 | b5 | b6 | b7 |
|---|---|---|---|---|---|---|
| $C_1$ | 0.987 | 2.148 | 0.942 | 0.248 | 0.260 | 0.315 |
| $C_2$ | −0.000727 | −0.000199 | −0.000261 | −0.000410 | −0.001084 | −0.000975 |
| $C_3$ | 0.000037 | 0.000058 | 0.000406 | 0.000563 | 0.000675 | 0.004012 |
| $C_4$ | 0.0869 | 0.0464 | 0.0928 | 0.2256 | 0.0632 | 0.0116 |
| $C_5$ | 0.0788 | −1.0962 | 0.1125 | 0.7991 | 0.7549 | 0.6906 |
| $C_b$, $w_b$ | L4/5/7 bilan bir xil | | | | | |

### 2.3 Termal konstantalar va ESUN

| Sensor | $K_1$ | $K_2$ | ESUN (b1, b2, b3, b4, b5, b7) W/m²/µm |
|---|---|---|---|
| L4 | 671.62 | 1284.30 | 1983, 1795, 1539, 1028, 219.8, 83.49 |
| L5 | 607.76 | 1260.56 | 1983, 1796, 1536, 1031, 220, 83.44 |
| L7 | 666.09 | 1282.71 | 1997, 1812, 1533, 1039, 230.8, 84.9 |
| L8 | MTL'dan | MTL'dan | — (`REFLECTANCE_MULT/ADD` ishlatiladi) |

### 2.4 `process_mtl`

| Atribut | Formula |
|---|---|
| `acq_time` | overpass vaqti, **UTC soat** (o'nlik) |
| `acq_doy` | yil kuni |
| `dr` | $1 + 0.033\cos(2\pi J/365)$ |
| `cos_theta_solar` | $\sin(\text{SUN\_ELEVATION})$ |
| `epsg` | $32600 + \text{UTM\_ZONE}$ |

---

## 3. TOA reflectance va brightness temperature (`et_numpy`)

### 3.1 L4/5/7 — `l457_refl_toa_band_func`

$$L = (DN - Q_{min})\frac{L_{max} - L_{min}}{Q_{max} - Q_{min}} + L_{min},\qquad \rho_{TOA} = \mathrm{clip}\!\left(\frac{\pi L}{d_r\,ESUN\,\cos\theta},\ 10^{-4},\ 1\right)$$

### 3.2 L8 — `l8_refl_toa_band_func`

$$\rho_{TOA} = \mathrm{clip}\!\left(\frac{M_\rho DN + A_\rho}{\cos\theta},\ 10^{-4},\ 1\right)$$

### 3.3 Brightness temperature — `ts_bt_func`

$$T_{BT} = \frac{K_2}{\ln(K_1/L + 1)},\qquad L \le 0 \Rightarrow \text{NaN}$$

Teskari: `thermal_rad_func` — $L = K_1/(\exp(K_2/T_{BT}) - 1)$ (Model 1 da BT dan radiance qayta tiklanadi).

---

## 4. Fmask (Collection 1 BQA) — `bqa_fmask_func`

| Bit(lar) | Shart | Klass |
|---|---|---|
| 0 | fill ≥ 1 | 0 (NoData) |
| 4 & (5–6) | cloud ∧ confidence ≥ 2 | 4 (bulut) |
| 11–12 | cirrus confidence ≥ 3 | 4 |
| 7–8 | shadow confidence ≥ 3 | 2 (soya) |
| 9–10 | snow confidence ≥ 3 | 3 (qor) |
| — | qolgani | 1 (toza) |

### 4.1 Morfologik ishlov (`landsat_prep_scene_func.main`)

Mask: `fmask ∈ {2, 3, 4}`. Struktura — `generate_binary_structure(2, 2)` (8-bog'lanish):

| Flag | Amal | Default |
|---|---|---|
| `fmask_smooth_flag` | dilate → erode → erode → dilate (`fmask_smooth_cells`) | False |
| `fmask_erode_flag` | erode | False |
| `fmask_buffer_flag` | dilate (bufer) | False |
| `edge_smooth_flag` (L5, L7) | `common_area` chekkasini erode → dilate | |
| `cloud_mask_flag` | `<folder_id>_mask.shp` poligoni rasterlanadi (qo'lda bulut maskasi) | |

`common_area_func`: barcha bandlar ≠ 0 bo'lgan piksellar (L7 SLC-off chiziqlari ham chiqariladi).

---

## 5. Ob-havo rasterlarini overpass vaqtiga moslash

NLDAS soatlik rasterlari (ea, wind, ETr, Tair) overpass'dan oldingi va keyingi soat orasida chiziqli interpolyatsiya qilinadi — `hourly_interpolate_func`:

$$X(t) = X_{prev} + (X_{next} - X_{prev})\cdot\frac{t - t_{prev}}{t_{next} - t_{prev}}$$

| Chiqish (SUPPORT) | Manba | Birlik |
|---|---|---|
| `ea_metric.img` | `metric_ea_input_folder` (NLDAS) | kPa |
| `wind_metric.img` | NLDAS wind | m/s |
| `etr_metric.img` | NLDAS hourly ETr (`refet.Hourly`) | mm/h |
| `etr_24hr_metric.img` | kunlik ETr (`metric_daily_re`) | mm/d |
| `tair_metric.img` | NLDAS Tair | |
| `ke` (ixtiyoriy) | `et_common.raster_swb_func` (AWC + kunlik ETr, PPT) | — |

`rounding_digits` — chiqish qiymatlarini yaxlitlash.

---

## 6. CRS / NoData

| Masala | Xatti-harakat |
|---|---|
| CRS | MTL `UTM_ZONE` → EPSG:326xx; 30 m; snap (15, 15). **Janubiy yarim shar uchun** ham 326xx (USGS L1 shimoliy UTM ishlatadi, manfiy northing) — mos. |
| Tashqi rasterlar (DEM, NLCD, NLDAS) | `drigo.raster_to_array(..., mask_extent)` — Landsat grid'iga kesib, qayta proyeksiyalanadi |
| NoData | `common_area` dan tashqari → `block_nodata_mask` → NaN; `ts_bt_func` da $L \le 0$ → NaN |
| Format | `.img` (HFA), Float32 |
