# 09 — Sensible Heat Flux ($H$), dT kalibratsiyasi va Monin–Obukhov iteratsiyasi

> **Manba fayllar:** `gridded_dT.py` (kalibratsiya: $a$, $b$), `sensible_heat_flux.py` (pikselli $H$ va suv bug'lanishi)

Bu — METRIC ning **yuragi**. "Internal calibration" g'oyasi aynan shu yerda.

---

## 1. Feynman tushuntirish: "Ikki termometrli tarozi"

$H$ — yuzadan havoga ketayotgan issiqlik:

$$H = \rho_a c_p \frac{dT}{r_{ah}}$$

Muammo: $dT = T_{0.1m} - T_{2m}$ (yuza yaqinidagi havo harorati farqi) ni **kosmosdan o'lchab bo'lmaydi**. Bastiaanssen (SEBAL) va Allen (METRIC) ajoyib hiyla topishgan:

> Ikki "etalon" piksel olaylik:
> - 🥶 **Cold** — yaxshi sug'orilgan beda: $ET = 1.05\cdot ET_r$ deb bilamiz → $H_{cold} = R_n - G - LE_{cold}$
> - 🔥 **Hot** — quruq yalang'och dala: $ET \approx 0$ (yoki soil water balance bergan kichik qiymat) → $H_{hot} = R_n - G - LE_{hot}$
>
> Ikki nuqtadan $H \to dT$ ni teskari hisoblaymiz va **chiziqli bog'lanish** quramiz:
> $$dT = a\cdot T_{s,dem} + b$$
> Endi har qanday piksel uchun $T_s$ ma'lum → $dT$ ma'lum → $H$ ma'lum!

Bu tarozi kabi: ikki ma'lum og'irlik bilan shkalani kalibrlaymiz, keyin istalgan narsani o'lchaymiz. Atmosfera xatolari (NLDAS $T_a$, emissivity, ...) $a$, $b$ ichiga "yutiladi".

---

## 2. Kalibratsiya — `calculate_gridded_dt`

### 2.1 Kirish: hot/cold kandidatlar

`self._hot_candidates`, `self._cold_candidates` — [10_pixel_selection.md](10_pixel_selection.md) dan. Har biriga qo'shimcha xususiyatlar sample qilinadi (`get_extra_data`):

```python
necessary_bands = self.net_radiation.addBands([self._rextra, self.instant_reference_etr]) \
    .select([0, 1, 2], ['net_radiation', 'rextra', 'instant_etr'])
```

Kandidatlar `zip` qilinib **bloklar** hosil bo'ladi: `[(cold_0, hot_0), (cold_1, hot_1), ...]`.

### 2.2 Har bir blok uchun energiya balansi

| Kattalik | Formula |
|---|---|
| Zom (ekin deb faraz) | $Z_{om} = 0.018\,LAI$; $LAI < 0.2778 \Rightarrow 0.005$ |
| Latent heat | $LE = K_c\cdot ET_{r,inst}\cdot\lambda/3600$, $\lambda = (2.501 - 0.002361(T_s-273))\times10^6$ |
| Soil heat flux | $G = (0.1 + 0.17e^{-0.55LAI})R_n$ |
| Sensible heat | $H = R_n - G - LE$ |

$K_c$ — hot/cold piksel ETrF (`kc` xususiyati), $ET_{r,inst}$ — mm/soat.

### 2.3 Iteratsiya (11 marta, `ee.List.iterate`)

**Boshlang'ich:** $\psi = 0$ (neytral), $\rho_a = \dfrac{1000\,P(z)}{1.01\cdot 293\cdot 287}$

Har iteratsiyada:

$$u_* = \frac{k\,u_{200}}{\ln(200/Z_{om}) - \psi_{200}}\qquad(\text{Eq. 38})$$

$$r_{ah} = \frac{\ln(z_2/z_1) - \psi_{z2} + \psi_{z1}}{k\,u_*} + r_{extra},\quad z_1 = 0.1,\ z_2 = 2\ \mathrm{m}\qquad(\text{Eq. 39})$$

$$dT = \frac{H\,r_{ah}}{\rho_a c_p},\quad c_p = 1004\qquad(\text{Eq. 46})$$

$$a = \frac{dT_{hot} - dT_{cold}}{T_{s,dem}^{hot} - T_{s,dem}^{cold}},\qquad b = dT_{cold} - a\,T_{s,dem}^{cold}\qquad(\text{Eq. 50, 51})$$

**Monin–Obukhov uzunligi** (Eq. 40):

$$L = -\frac{\rho_a c_p u_*^3 T_s}{k\,g\,H},\quad H = 0 \Rightarrow L = -1000;\quad L > 0 \Rightarrow L = \max(L, 2)$$

**Stabillik tuzatishlari** ($x_z = (1 - 16z/L)^{0.25}$):

| | Beqaror ($L<0$) | Barqaror ($L>0$) |
|---|---|---|
| $\psi_m(200)$ | $2\ln\frac{1+x_{200}}{2} + \ln\frac{1+x_{200}^2}{2} - 2\arctan x_{200} + \frac{\pi}{2}$ | $-5\cdot 2/L$ |
| $\psi_h(2)$ | $2\ln\frac{1+x_2^2}{2}$ | $-5\cdot 2/L$ |
| $\psi_h(0.1)$ | $2\ln\frac{1+x_{0.1}^2}{2}$ | $-5\cdot 0.1/L$ |

> 📝 Barqaror holatda $\psi_m(200)$ uchun $-5\cdot\mathbf{2}/L$ (z=2 m, z=200 emas!) ishlatiladi — Allen et al. (2007) Eq. 41 ga muvofiq: 200 m da barqaror qatlam yo'q deb faraz, "blending height" kontseptsiyasi.

**Damping (so'ndirish):** har bir $\psi$ oldingi qiymat bilan o'rtachalanadi: $\psi^{(n)} \leftarrow (\psi^{(n-1)} + \psi^{new})/2$ — tebranishning oldini oladi.

**Zichlik yangilanishi:** $\rho_a = \dfrac{1000\,P}{1.01\,(T_s - dT)\,287}$

### 2.4 ⚠️ Haqiqiy natija: **bitta blok**

```python
a_single_block = ee.Image.constant(a_b_values.first().get('a'))
b_single_block = ee.Image.constant(a_b_values.first().get('b'))
...
single_block = a_single_block.addBands([b_single_block, h_hot, h_cold])
# a = ee.Algorithms.If(a_b_bool, a_single_block, a)   ← hisoblanadi, lekin...
return single_block                                    ← ...har doim single_block qaytadi!
```

Kod `robustLinearRegression(longitude, latitude → a)` bilan **fazoviy taqsimlangan** $a(\lambda,\varphi)$, $b(\lambda,\varphi)$ quradi (nomi "gridded dT" shundan), lekin **yakunda faqat birinchi blokning konstant $a$, $b$ qaytariladi**. Demak eeMETRIC amalda **sahna bo'yicha bitta dT funksiyasi** ishlatadi. Fazoviy o'zgaruvchanlik o'rniga **spatial delapsing** ([11](11_lapsed_surface_regions.md)) ishlatiladi.

Chiqish bandlari: `a`, `b`, `h_hot`, `h_cold`.

---

## 3. Pikselli H — `calculate_sensible_heat_flux`

### 3.1 Qaysi temperatura? (`ts_model`)

| `ts_model` | $T_{s,del}$ | Default |
|---|---|---|
| `tall_vegetation` | `_surface_temperature_dem_tall_veg` (delapsed + canopy unmixing) | ✅ |
| `min_albedo` | `ts_dem_latlon_alb_adj` | |
| `default` | `ts_dem_latlon` | |

### 3.2 dT va uning chegaralari (Allen et al., 2014, Eq. 15.4–15.6)

$$dT = a\,T_{s,del} + b$$

"Dry" chegarasi (ETrF = 0 ga ekstrapolyatsiya):

$$T_{dry} = T_{hot} + K_{c,hot}\frac{T_{hot} - T_{cold}}{K_{c,cold} - K_{c,hot}},\qquad T_{thr} = T_{dry} + 2$$

| Holat | dT |
|---|---|
| $T_{s,del} > T_{thr}$ (juda issiq) | $(aT_{thr} + b) + \frac{a}{8}(T_{s,del} - T_{thr})$ — qiyalik 8 marta kamayadi |
| $T_{s,del} < T_{cold} - 2$ (juda sovuq) | $b + a(T_{cold} - 2) + \frac{a}{8}(T_{s,del} - (T_{cold} - 2))$ |

> 🧠 **Nega $a/8$?** Ekstremal piksellarda chiziqli ekstrapolyatsiya fizik ma'nosiz $H$ beradi (masalan asfalt yoki muz). Qiyalikni "yumshatish" — $H$ ning portlab ketishini to'xtatadi.

### 3.3 Iteratsiya (9 marta)

Kalibratsiyadagi kabi, lekin endi **har piksel uchun**:

- $Z_{om}$ = `_zom_adj` (tog' + albedo tuzatilgan, [08](08_momentum_roughness.md))
- $u_{200}$ = `_wind_speed_200_adj` (tog' tuzatilgan, min 5 m/s)
- $T_s$ (L formulasida) = `_surface_temperature_tall_veg` (delapse qilinmagan!)

$$L = \frac{u_*^3\,T_s\,r_{ah}}{-k\,g\,dT}$$

> Bu $L = -\rho c_p u_*^3 T/(kgH)$ ning $H = \rho c_p dT/r_{ah}$ qo'yilgan ko'rinishi.

### 3.4 Tog'da "buoyancy" tuzatish (`cpsi` = 1.0)

Shamolga qaragan qiyalik (windward):

$$w_r^+ = \max\!\big(\sin^{1.5}s\cdot|\cos(\psi - \psi_w)|\cos(\psi - \psi_w),\ 0\big)$$

($slope > 5° \land \sigma_z > 30 \land 0.1 < RE < 0.95$ bo'lganda)

$L_{avg} = (L_{final} + L_{iter})/2$; keyin yakuniy $\psi$:

| Holat | Formula |
|---|---|
| $L<0$, $s \le 5°$ | standart beqaror $\psi$ |
| $L<0$, $s > 5°$ | $\psi\cdot(1 + C_\psi w_r^+)$ — beqarorlik kuchayadi |
| $L>0$, $s \le 5°$ | $-5z/L$ |
| $L>0$, $s > 5°$ | $\min\big(-5z/L\cdot(1 - C_\psi w_r^+),\ -0.5z/L\big)$ |

Va yana damping: $\psi \leftarrow (\psi + \psi_{iter})/2$.

### 3.5 Yakuniy H (Allen et al., 2007, Eq. 28)

$$r_{ah} = \frac{\ln(2/0.1) - \psi_{z2} + \psi_{z1}}{k\,u_*} + r_{extra}$$

$$\rho_a = \frac{3.486\,P}{1.01\,(T_s - dT)}\quad[\mathrm{kg/m^3}]$$

$$\boxed{H = \frac{\rho_a\,c_p\,dT}{r_{ah}\cos s}}$$

> $1/\cos s$ — qiya yuzaning haqiqiy maydoni uchun (Rn ham $\cos\theta_{mtn}$ orqali shunday normalizatsiya qilingan). $3.486 \approx 1000/R$, $R = 287$ J/kg/K (FAO-56 dagi standart konstanta; kPa → Pa), $1.01$ — virtual temperatura tuzatishi.

---

## 4. Ochiq suvdan aerodinamik bug'lanish (Allen et al., 2014, Ch. 10)

Suv uchun METRIC energiya balansi o'rniga to'g'ridan-to'g'ri Dalton tipidagi formula ishlatadi.

$$Z_{om,w} = \max(2.4\times10^{-7}u_{200}^{2.55},\ 5\times10^{-5})$$

$$r_{a,w} = \frac{[\ln(200/Z_{om,w}) - 0.3\psi_{200}]\,[\ln(2/Z_{om,w}) - 0.3\psi_2]}{k^2\,u_{200}}\qquad(\text{Eq. 10.12})$$

To'yingan bug' bosimi (Tetens, Kelvinda; Eq. 10.4a):

$$e^\circ(T_s) = \begin{cases}0.6108\exp\dfrac{17.27(T_s - 273.15)}{T_s - 35.85}, & T_s \ge 275\\[2mm] 0.6108\exp\dfrac{22.46(T_s - 273.15)}{T_s - 0.53}, & T_s < 275\ (\text{muz})\end{cases}$$

$$E_{aero} = \frac{3600\,\rho_a\,(q_s - q_a)}{r_{a,w}}\quad[\mathrm{mm/h}],\qquad q = \frac{0.622\,e}{P - 0.378\,e}\qquad(\text{Eq. 10.11})$$

Bu `_evapor_water` → G hisobida ([07](07_soil_heat_flux.md#5-suv-va-qor-uchun-aerodinamik-g-residual)) ishlatiladi.

> Flat versiyada $\psi$ lar 0.3 ga ko'paytirilmaydi va $u_{200}$ tog' tuzatilmagan.

---

## 5. Flat versiya — `calculate_sensible_heat_flux_flat`

Farqlar:

| | Mountain (default) | Flat |
|---|---|---|
| Zom | `_zom_adj` | `aerodynamic_roughness` |
| u200 | `_wind_speed_200_adj` | `_wind_speed_200` |
| L dagi T | `_surface_temperature_tall_veg` | `surface_temperature` |
| Buoyancy (cpsi) | ✅ | ❌ |
| $H$ | $/\cos s$ | yo'q |
| `ts_model` | `tall_vegetation` | `default` |

---

## 6. Konstantalar jadvali

| Belgi | Qiymat | Ma'no |
|---|---|---|
| $k$ | 0.41 | von Kármán |
| $g$ | 9.81 m/s² | gravitatsiya |
| $c_p$ | 1004 J/kg/K | havo issiqlik sig'imi |
| $z_1, z_2$ | 0.1, 2.0 m | dT o'lchov balandliklari |
| $z_3$ | 200 m | blending height |
| $L_{min}$ (stable) | 2.0 m | |
| iteratsiyalar | 11 (kalibr.), 9 (piksel) | |
