# 01 — Kirish ma'lumotlari, radiatsiya va g'adir-budurlik (pyMETRIC, Nieto)

> **Manba:** `pyMETRIC/PyMETRIC.py` (`process_local_image`, `run_METRIC`) + pyTSEB (`meteo_utils`, `net_radiation`, `resistances`)

---

## 1. Feynman tushuntirish

Bu modelda yuza "ikki qavatli uy" deb qaraladi: **barglar qatlami** (canopy) va uning ostidagi **tuproq**. Quyosh nuri barglardan o'tadi, bir qismi qaytadi, bir qismi tuproqqa yetadi. Campbell modeli shu "nur yo'li"ni ko'rinadigan (VIS) va yaqin infraqizil (NIR) diapazonlarda alohida hisoblaydi. Shuning uchun bu yerda albedo tayyor kirim emas — u spektral xususiyatlardan **chiqariladi**:

$$\alpha = 1 - \frac{S_n}{S_{dn}}$$

---

## 2. Quyosh burchaklari — `met.calc_sun_angles(lat, lon, stdlon, doy, time)`

$$\delta = 0.409\sin\!\left(\frac{2\pi J}{365} - 1.39\right)$$

Vaqt tenglamasi (daqiqa):

$$EOT = 0.258\cos\delta - 7.416\sin\delta - 3.648\cos2\delta - 9.228\sin2\delta$$

$$t_{solar} = t - \left(-\frac{EOT}{60} + \frac{\lambda_{std} - \lambda}{15}\right),\qquad \omega = 15(t_{solar} - 12)\ [°]$$

$$\sin\beta = \cos\omega\cos\delta\cos\varphi + \sin\delta\sin\varphi,\qquad SZA = 90° - \beta$$

> ⚠️ `time` — `stdlon` meridianidagi **standart vaqt** (UTC emas). Landsat `SCENE_CENTER_TIME` UTC da beriladi. O'zbekiston uchun: `stdlon = 75`, `time = UTC + 5`. Agar `stdlon=0` qo'ysangiz, `time` ni UTC da bering.

---

## 3. Atmosfera bosimi va uzun to'lqinli nurlanish

| Kattalik | Formula | Funksiya |
|---|---|---|
| Bosim (agar `p` yo'q) | $p = 1013.25\,(1 - 2.225577\times10^{-5}z)^{5.25588}$ [mb] | `met.calc_pressure` |
| Atmosfera emissivity | $\varepsilon_a = 1.24\,(e_a/T_a)^{1/7}$ (Brutsaert, 1975; $e_a$ mb) | `rad.calc_emiss_atm` |
| $L_{dn}$ (agar yo'q) | $L_{dn} = \varepsilon_a\,\sigma T_a^4$ | `met.calc_stephan_boltzmann` |

---

## 4. Diffuz / to'g'ri nur — `rad.calc_difuse_ratio(S_dn, SZA, p)` (Weiss & Norman, 1985)

1. Clear-sky potensial VIS va NIR nurlar ($R_{dir,vis}, R_{dif,vis}, R_{dir,nir}, R_{dif,nir}$), quyosh konstantasi 1320 W/m².
2. $f_{clear} = \min(S_{dn}/(pot_{vis} + pot_{nir}),\ 1)$
3. $f_{vis} = pot_{vis}/(pot_{vis} + pot_{nir})$, $f_{nir} = 1 - f_{vis}$
4. To'g'ri nur ulushi (Eq. 11–12):

$$dir_{vis} = \frac{R_{dir,vis}}{pot_{vis}}\left[1 - \left(\frac{0.9 - \min(f_{clear},0.9)}{0.7}\right)^{2/3}\right],\qquad dir_{nir} = \frac{R_{dir,nir}}{pot_{nir}}\left[1 - \left(\frac{0.88 - \min(f_{clear},0.88)}{0.68}\right)^{2/3}\right]$$

5. $Skyl = (1 - dir_{vis})f_{vis} + (1 - dir_{nir})f_{nir}$

$$S_{dn,dir} = S_{dn}(1 - Skyl),\qquad S_{dn,dif} = S_{dn}\cdot Skyl$$

---

## 5. Sof qisqa to'lqin $S_n$

### 5.1 Yalang'och tuproq ($LAI = 0$)

$$\rho_{soil} = f_{vis}\rho_{vis,S} + f_{nir}\rho_{nir,S},\qquad S_n = (1 - \rho_{soil})(S_{dir} + S_{dif})$$

$z_{0M} = $ `z0_soil`, $d_0 = 0$.

### 5.2 O'simlik ($LAI > 0$) — `rad.calc_Sn_Campbell` (Campbell & Norman, 1998, 15-bob)

Har bir diapazon uchun barg yutuvchanligi $a = 1 - \rho_{leaf} - \tau_{leaf}$:

| Kattalik | Formula (C&N Eq.) |
|---|---|
| Chuqur canopy qaytarishi | $\rho_{cpy} = \dfrac{1 - \sqrt a}{1 + \sqrt a}$ (15.7) |
| Beam so'nish koeffitsienti | $K_{be}(\theta, x_{LAD})$ (15.4), sferik: $K_{be} = 0.5/\cos\theta$ |
| Beam qaytarish | $\rho_b = \dfrac{2K_{be}\rho_{cpy}}{K_{be} + 1}$ (15.8) |
| O'tkazish / albedo (tuproq ustidagi) | $\tau = \dfrac{(\rho^2 - 1)e^{-\sqrt a K L}}{(\rho\rho_s - 1) + \rho(\rho - \rho_s)e^{-2\sqrt a KL}}$ (15.11), $\alpha = \dfrac{\rho + F}{1 + \rho F}$, $F = \dfrac{\rho - \rho_s}{\rho\rho_s - 1}e^{-2\sqrt aKL}$ (15.9) |
| Diffuz | xuddi shunday, $K_d = -\ln\tau_d/LAI$ (yarim sharga integral) |

Natija: $S_{n,C}$ (barg) + $S_{n,S}$ (tuproq) → $S_n = S_{n,C} + S_{n,S}$ (`R_ns1`).

$$\alpha = 1 - \frac{S_n}{S_{dn}}\qquad(\text{endmember qidiruvi uchun})$$

---

## 6. Yuza emissivity

$$\varepsilon = VI\cdot\varepsilon_C + (1 - VI)\,\varepsilon_S$$

```python
out_data['emiss'] = in_data['VI']*in_data['emis_C'] + (1 - in_data['VI'])*in_data['emis_S']
```

> ⚠️ Bu yerda `VI` **vegetatsiya ulushi** ($f_c$, 0..1) sifatida ishlatiladi. Kirimga xom NDVI berilsa (masalan suvda −0.3), ε ning qiymati fizik chegaradan chiqib ketadi. Shu sababli VI ni $[0, 1]$ ga normallashtirib bering (masalan $(NDVI - NDVI_{soil})/(NDVI_{veg} - NDVI_{soil})$).

---

## 7. G'adir-budurlik — `res.calc_roughness(LAI, h_C, w_C, landcover, f_c)` (Schaudt & Dickinson, 2000)

### 7.1 Ekin / o'tloq / savanna / crop mosaic (IGBP 12, 10, 9, 14)

$$z_{0M} = h_C/8,\qquad d_0 = 0.65\,h_C$$

### 7.2 O'rmon va butazor — Raupach (1994) + Lindroth tuzatishi

Frontal maydon indeksi: igna bargli $\lambda = \frac{2}{\pi}f_cw_C$, keng bargli va butazor $\lambda = f_cw_C$. Agar `f_c` berilmasa: $f_c = 1 - e^{-0.5LAI}$ (igna/buta) yoki $1 - e^{-LAI}$ (keng barg).

$$\frac{z_{0M}}{h} = \begin{cases} \dfrac{0.0537}{\lambda^{0.51}}(1 - e^{-10.9\lambda^{0.874}}) + 0.00368, & \lambda > 0.152\\ 5.86\,e^{-10.9\lambda^{1.12}}\lambda^{1.33} + 0.00086, & \lambda \le 0.152\end{cases}$$

$$\frac{d_0}{h} = 1 - \frac{1 - e^{-\sqrt{15\lambda}}}{\sqrt{15\lambda}}$$

Lindroth: $f_z = 0.3299LAI^{1.5} + 2.1713$ ($LAI \ge 0.8775$: $1.6771e^{-0.1717LAI} + 1$), $f_d = 1 - 0.3991e^{-0.1779LAI}$.

### 7.3 Suv, shahar, qor, barren

$z_{0M} = 0.01$, $d_0 = 0$.

> Issiqlik g'adir-budurligi: $z_{0H} = z_{0M}/e^{kB}$, `kB = 0` → $z_{0H} = z_{0M}$ (`res.calc_z_0H`).

---

## 8. Datum (adiabatik) temperaturalar

Namli-adiabatik lapse rate (`met.calc_lapse_rate_moist`, AMS glossary), $r = 0.622e_a/(p - e_a)$:

$$\Gamma_w = g\,\frac{R_dT^2 + \lambda rT}{c_pR_dT^2 + \lambda^2r\varepsilon}\quad[\mathrm{K/m}]$$

$$T_{R,datum} = T_R + \Gamma_w\cdot z,\qquad T_{A,datum} = T_A + \Gamma_w\cdot z$$

> 🧠 Datum — **dengiz sathi** ($z = 0$), sahna o'rtachasi emas. Tog'li hududda (masalan 2000 m) tuzatish ≈ +10 K bo'ladi. Endmember tanlash va dT shu "dengiz sathiga tushirilgan" temperaturada qilinadi.

---

## 9. Soil heat flux variantlari

| `G_form` | Formula | Qayerda |
|---|---|---|
| 0 | $G = G_{const}$ | `tseb.calc_G` |
| 1 | $G = r\,R_n$ | `tseb.calc_G_ratio` |
| 2 | $G = R_n\cdot A\cos\!\left(\frac{2\pi(t - 12 + \phi)}{B}\right)$ (Santanello & Friedl, 2003) | `tseb.calc_G_time_diff` |
| 4 | $G = 0.04R_n$ (tall guruh) / $0.10R_n$ (short guruh) | `run_METRIC` |
| 5 | $G/R_n = (T_s - 273.15)(0.0038 + 0.0074\alpha)(1 - 0.98\,VI^4)$ (Bastiaanssen; Allen 2007 Eq. 26) | `run_METRIC`, `METRIC.calc_G_Allen` |

> Namunaviy konfiguratsiyada `G_form=4`.

---

## 10. CRS / NoData

| Masala | Xatti-harakat |
|---|---|
| CRS | `T_R1` ning `GetProjection()`/`GetGeoTransform()` chiqishga ko'chiriladi. **Qayta proyeksiya yo'q** — barcha rasterlar bir xil grid, CRS va o'lchamda bo'lishi **shart** (GDAL buni tekshirmaydi). |
| `lat`, `lon` | Gradusda **alohida raster yoki son** sifatida beriladi (proyeksiyadan hisoblanmaydi). UTM rasterda piksel-darajadagi lat/lon kerak bo'lsa, oldindan `gdalwarp`/`pyproj` bilan yarating. |
| NoData | `VI` yoki `T_R1` NaN bo'lsa mask = 0. GeoTIFF NoData qiymati (masalan −9999) **avtomatik NaN ga aylantirilmaydi** — kirimni oldindan NaN qiling. |
| Chiqish | Float32, NoData = NaN |
