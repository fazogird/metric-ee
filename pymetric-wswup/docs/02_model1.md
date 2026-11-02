# 02 — Model 1: yuza xususiyatlari (pymetric, WSWUP)

> **Manba:** `code/metric_functions/metric_model1_func.py` (orkestrator), `code/support/et_numpy.py`, `code/support/et_common.py`

---

## 1. Feynman tushuntirish

Model 1 — "tibbiy ko'rik". Kalibratsiyadan oldin har piksel uchun yuzaning "o'lchamlari" olinadi: quyoshga nisbatan burchagi (cos θ), atmosfera o'tkazuvchanligi (τ), yer yuzasidagi reflectance, albedo, yashillik (NDVI/SAVI), LAI, emissivity va nihoyat haqiqiy yuza temperaturasi $T_s$. Barchasi alohida `.img` rasterga yoziladi, Model 2 ularni o'qiydi.

Hisoblash bloklar bo'yicha bajariladi (`drigo.block_gen`, `block_size`). Har bir mahsulot faqat kerak bo'lsa hisoblanadi: `calc_dict` / `save_dict` bog'liqlik zanjiri, masalan `ts_dem → ts → rc → ts_bt, em_nb → lai → savi → refl_toa`.

---

## 2. cos θ (quyosh tushish burchagi)

| `cos_theta_model` | Formula | Funksiya |
|---|---|---|
| `SOLAR` | $\sin(\beta_{MTL})$ — butun sahna uchun bitta son | `et_common.cos_theta_solar_func` |
| **`CENTROID`** (default) | sahna markazidagi $\cos\theta = \sin\delta\sin\varphi_c + \cos\delta\cos\varphi_c\cos\omega$ | `et_common.cos_theta_centroid_func` |
| `SPATIAL` | xuddi shu, har piksel lat/lon bilan | `et_numpy.cos_theta_spatial_func` |
| `MOUNTAIN` | Duffie–Beckman (qiyalik, aspect), $/\cos s$, min 0.1 | `et_numpy.cos_theta_mountain_func` |

Yordamchi formulalar (`et_common`):

$$\delta = 0.409\sin\!\left(\frac{2\pi J}{365} - 1.39\right),\quad b = \frac{2\pi(J - 81)}{364},\quad S_c = 0.1645\sin2b - 0.1255\cos b - 0.025\sin b$$

$$t_{solar} = t_{UTC} + \frac{24\,\lambda_{rad}}{2\pi} + S_c - 12,\qquad \omega = \mathrm{wrap}\!\left(\frac{2\pi}{24}t_{solar},\ -\pi,\ \pi\right)$$

MOUNTAIN ($\gamma = aspect - \pi$, $s$ — slope, radian):

$$\cos\theta_{rel} = \sin\delta\sin\varphi\cos s - \sin\delta\cos\varphi\sin s\cos\gamma + \cos\delta\cos\varphi\cos s\cos\omega + \cos\delta\sin\varphi\sin s\cos\gamma\cos\omega + \cos\delta\sin\gamma\sin s\sin\omega$$

$$\cos\theta = \max(\cos\theta_{rel}/\cos s,\ 0.1)$$

> 🐛 `cos_theta_spatial_func` va `cos_theta_mountain_func` `solar_time_rad_func(time, lon, sc)` ni chaqiradi, lekin signatura `(lon, time, sc)`. Natijada vaqt va uzunlik **almashib ketadi**. Default `CENTROID` to'g'ri chaqiradi ([09](09_kuzatuvlar.md) #1). Lat/lon rasterlari **radian**da bo'lishi kerak.

---

## 3. Atmosfera

| Kattalik | Formula | Funksiya |
|---|---|---|
| Bosim | $P = 101.3\left(\frac{293.15 - 0.0065z}{293.15}\right)^{5.26}$ kPa (`pair_model`: DEM yoki DATUM) | `air_pressure_func` |
| Precipitable water | $W = 0.14\,e_aP + 2.1$ | `precipitable_water_func` |
| $e_a$ | NLDAS raster / REFET / MANUAL | |

### 3.1 Broadband transmissivity — `tau_broadband_func`

$$\tau_B = 0.98\exp\!\left[\frac{-0.00146P}{K_t\cos\theta} - 0.075\left(\frac{W}{\cos\theta}\right)^{0.4}\right],\qquad \tau_D = 0.35 - 0.36\tau_B$$

$$\tau_{sw} = \tau_B + \tau_D$$

> Izoh (kodda): *"Model differs from formulas in METRIC manual"* — $\tau_B < 0.15$ uchun $0.18 + 0.82\tau_B$ shakli R. Allen tavsiyasiga ko'ra qo'llanmaydi. $K_t$ = `kt` (default 1.0).

### 3.2 Narrowband transmissivity (Tasumi et al., 2008) — `tau_narrowband_func`

$$\tau_{b} = C_1\exp\!\left[\frac{C_2P/K_t - (C_3W + C_4)}{\cos\theta}\right] + C_5$$

`tau_in` — $\cos\theta$ bilan, `tau_out` — $\cos\theta = 1$ (nadir).

---

## 4. At-surface reflectance va albedo

### 4.1 Tasumi SR — `refl_sur_tasumi_func`

$$\rho_{s,b} = \mathrm{clip}\!\left(\frac{\rho_{t,b} - C_b(1 - \tau_{in,b})}{\tau_{in,b}\,\tau_{out,b}},\ 10^{-4},\ 1\right)$$

`refl_sur_model_type = LEDAPS` bo'lsa tayyor LEDAPS SR o'qiladi.

### 4.2 Albedo — `albedo_sur_func`

$$\alpha = \sum_b w_b\,\rho_{s,b},\qquad w = [0.254, 0.149, 0.147, 0.311, 0.103, 0.036]$$

---

## 5. Vegetatsiya indekslari

`ndi_func(a, b, l)`: $\dfrac{(1 + l)(a - b)}{l + a + b}$ — $l = 0$ da normalized difference, $l > 0$ da SAVI.

| Indeks | Bandlar (TOA/SUR tartibida) | Formula |
|---|---|---|
| NDVI | 4 (NIR), 3 (Red) | $(\rho_4 - \rho_3)/(\rho_4 + \rho_3)$ |
| NDWI | 5 (SWIR1), 2 (Green) | $(\rho_5 - \rho_2)/(\rho_5 + \rho_2)$ |
| SAVI | 4, 3, $l$ = `savi_l` = **0.1** | $1.1(\rho_4 - \rho_3)/(0.1 + \rho_4 + \rho_3)$ |
| EVI | blue, red, nir | $2.5(\rho_N - \rho_R)/(\rho_N + 6\rho_R - 7.5\rho_B + 1)$ |

**LAI:**

| Funksiya | Formula |
|---|---|
| `savi_lai_func` (default) | $LAI = \mathrm{clip}(11\,SAVI^3,\ 0,\ 6)$ (Allen 2007) |
| `ndvi_lai_func` | $LAI = \mathrm{clip}(7\,NDVI^3,\ 0,\ 6)$ |

> Default: indekslar va LAI **TOA** reflectance'dan (`lai_toa_veg_index_type = SAVI`, `em_refl_type = TOA`).

Qo'shimcha (Model 1 da ishlatilmaydi): Tasseled Cap brightness/greenness/wetness (TOA va SUR koeffitsientlari), ET* ($ET^* = \max(c_0 + c_1EVI + c_2EVI^2, 0)$, $c = [-0.1955, 2.9042, -1.5916]$), $ET_g = ET^*(ET_o - P)$.

---

## 6. Emissivity

$water$ — NDVI (default), threshold = 0:

| Funksiya | Formula | Suv ($NDVI < 0$) | $NDVI > 0 \land LAI > 3$ |
|---|---|---|---|
| `em_nb_func` | $0.97 + LAI/300$ | 0.99 | 0.98 |
| `em_0_func` | $0.95 + LAI/100$ | 0.985 ($\le 0$) | 0.98 |

---

## 7. Yuza temperaturasi

### 7.1 Korreksiyalangan radiance — `rc_func` (Allen 2007, Eq. 21)

$$R_c = \frac{L - R_p}{\tau_{NB}} - (1 - \varepsilon_{NB})R_{sky}$$

Defaultlar: $R_p$ = `rp` = 0.91, $\tau_{NB}$ = `tnb` = 0.866, $R_{sky}$ = `rsky` = 1.32.

$L$ — `thermal_rad_func(ts_bt, K1, K2)` (BT rasteridan teskari hisoblanadi).

### 7.2 $T_s$ — `ts_func` (Eq. 20)

$$T_s = \frac{K_2}{\ln(\varepsilon_{NB}K_1/R_c + 1)}$$

### 7.3 Delapse — `ts_delapsed_func`

$$T_{s,dem} = T_s + \Gamma\,\frac{z - z_{datum}}{1000},\qquad \Gamma = 6.5\ \mathrm{K/km}$$

Teskarisi `ts_lapsed_func`: $T_s = T_{s,dem} - \Gamma(z - z_{datum})/1000$.

---

## 8. Model 1 chiqishlari (default `save_*_flag`)

| Raster | Default saqlanadi |
|---|---|
| `cos_theta`, `albedo_at_sur`, `ndvi_toa`, `ndwi_toa`, `lai_toa`, `ts` | ✅ |
| `refl_sur_tasumi`, `tau`, `savi`, `em_nb`, `em_0`, `rc`, `ts_dem`, `dem`, `landuse`, `slope/aspect/lat/lon` | ixtiyoriy |

`remove_refl_toa_flag`, `remove_refl_sur_flag`, `remove_ts_bt_flag` — oraliq rasterlarni o'chirish (disk tejash).
