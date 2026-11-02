# 04 — Model 2: energiya balansi, kalibratsiya va ETrF (pymetric, WSWUP)

> **Manba:** `code/metric_functions/metric_model2_func.py` (1830 qator), `code/support/et_numpy.py`, `code/support/et_common.py`

---

## 1. Feynman tushuntirish

Model 2 ikki qismdan iborat:

1. **Ikki nuqtali kalibratsiya** (`cold.shp`, `hot.shp`): har nuqtada Model 1 rasterlaridan qiymatlar o'qiladi, $R_n$ va $G$ hisoblanadi, $LE = K_c\cdot ET_r\cdot\lambda$ belgilanadi. $H = R_n - G - LE$ dan Monin–Obukhov iteratsiyasi bilan $dT$ topiladi. Natija — $a$, $b$ koeffitsientlari.
2. **Rasterni hisoblash** (bloklar bo'yicha): har piksel uchun $dT = a\,T_{s,dem} + b$, so'ng 6 marta stabillik iteratsiyasi → $H$ → $LE$ → $ET_{inst}$ → $ET_rF$ → $ET_{24}$.

---

## 2. Kalibratsiya nuqtalarini tekshirish

| Tekshiruv | Shart | Natija |
|---|---|---|
| Temperatura farqi | $\lvert T_{cold} - T_{hot}\rvert < 4$ K (`ts_diff_threshold`) | ❌ "cannot be accurately calibrated" |
| Tartib | $T_{cold} > T_{hot}$ | ❌ |
| Kc | `kc_cold <= kc_hot` | ❌ |
| Override | `ts_cold_override_flag` / `ts_hot_override_flag` | $T_{s,dem}$ ni qo'lda belgilash, $T_s$ qayta lapse qilinadi |

---

## 3. Shamol: stansiyadan 200 m ga

$$u_{*,st} = \frac{k\,u_{mod}}{\ln(z_w/z_{0,st})},\qquad u_{200} = \frac{u_{*,st}\ln(200/z_{0,st})}{k}$$

| Parametr | Default |
|---|---|
| $z_w$ = `wind_speed_height` | 2.0 m |
| $z_{0,st}$ = `station_roughness` | 0.015 m |
| $u_{mod}$ | $u + $ `additional_wind_speed` (NLDAS / REFET) yoki $u$ (MANUAL) |

> NLDAS rejimida $u$, $e_a$, $ET_r$, $ET_{r,24}$ **cold piksel joyidagi** qiymat sifatida olinadi. Ya'ni ular butun sahna uchun bitta son (`cell_value_set(...)[0]`).

---

## 4. Radiatsiya balansi (kalibratsiya va raster uchun bir xil)

| Kattalik | Formula | Funksiya |
|---|---|---|
| $R_{s\downarrow}$ | $G_{sc}\,d_r\,\tau\cos\theta$, $G_{sc} = 1367$ | `rs_in_func` |
| $R_{s\uparrow}$ | $\alpha R_{s\downarrow}$ | `rs_out_func` |
| $T_{cold}^{lap}$ | cold pikselning $T_s$ i har piksel balandligiga lapse: $T_{s,cold} - \Gamma(z - z_d)/1000$ | `ts_lapsed_func` |
| $R_{L\downarrow}$ | $0.85(-\ln\tau)^{0.09}\,\sigma\,(T_{cold}^{lap})^4$ | `rl_in_func` (`rl_in_coef1/2`) |
| $R_{L\uparrow}$ | $\varepsilon_0\sigma T_s^4 + (1 - \varepsilon_0)R_{L\downarrow}$ (chiqgan + qaytgan) | `rl_out_func` |
| $R_n$ | $R_{s\downarrow} - R_{s\uparrow} + R_{L\downarrow} - R_{L\uparrow}$ | `rn_func` |
| $R_{n,24}$ (Slob) | $(1 - \alpha)R_{s,24} - 110\,R_{s,24}/R_{a,24}$ | `rn_24_func` (`cs = 110`) |

$\sigma = 5.67\times10^{-8}$. $R_{a,24}$ — `et_common.ra_daily_func` (FAO-56, MJ/m²/d).

> ⚠️ `rn_24_func` ga instant $R_{s\downarrow}$ beriladi (`rs_in=rs_in_array`), kunlik emas. Kod `rn_24` faqat ixtiyoriy chiqish (`save_rn_24_raster_flag`), ET24 da ishlatilmaydi.

---

## 5. Soil heat flux

### 5.1 METRIC (default) — `g_ag_func` (Tasumi 2003)

$$G = \begin{cases}(0.05 + 0.18e^{-0.521LAI})\,R_n, & LAI \ge 0.5\\ 1.80\,(T_s - 273.16) + 0.084\,R_n, & LAI < 0.5\end{cases}$$

### 5.2 SEBAL — `g_sebal_func` (Bastiaanssen 2000)

$$\frac{G}{R_n} = T_s\,(0.0038 + 0.0074\alpha)(1 - 0.98NDVI^4)$$

> ⚠️ Funksiya **nisbat** ($G/R_n$) qaytaradi va $T_s$ ni Kelvinda qabul qiladi. SEBAL formulasida esa $T_s$ °C da bo'ladi va natija $R_n$ ga ko'paytirilishi kerak. Model 2 bu qiymatni to'g'ridan-to'g'ri $G$ sifatida ishlatadi, natijada G ≈ 1–2 W/m² chiqadi ([09](09_kuzatuvlar.md) #2). Default METRIC rejimiga ta'sir qilmaydi.

### 5.3 Maxsus yuzalar (raster bosqichida)

| Flag | Default | Shart | $G$ |
|---|---|---|---|
| `use_g_water_flag` | True | $NDVI \le 0 \land T_s < \overline{T_{s,dem}^{hot,cold}}$ | $0.5R_n$ |
| `use_g_snow_flag` | False | $\alpha > 0.35 \land T_s < 277$ | $0.5R_n$ |
| `use_g_wetland_flag` | False | NLCD 90/95 $\land NDVI \le 0.5$ | $-51 + 0.41R_n$ |

---

## 6. Momentum roughness — `zom_func`

JSON jadvali (`zom_remap_path`) NLCD → qiymat / `"perrier"` / `"LAI"`:

| `misc/zom_nlcd_default.json` | 11 | 12 | 21 | 22/23 | 24 | 31/32 | 41–43 | 51/52 | 71 | 72 | 81/82 | 90/94 | 95 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $Z_{om}$ (m) | 0.0002 | 0.0004 | 0.1 | 0.55 | 1.1 | 0.00035 | perrier | 0.4 | 0.019 | 0.04 | LAI | 0.1 | 0.03 |

(`misc/zom_nlcd_metric.json` — muqobil jadval: 11 → 0.0005, 31 → 0.1, 90 → 0.4, ...)

| Rejim | Formula |
|---|---|
| `"LAI"` (va jadvalda yo'q klasslar) | $Z_{om} = \max(0.018LAI,\ 0.005)$ |
| `"perrier"` — `perrier_zom_func` | $Z_{om} = \max\!\big((1 - e^{-0.6LAI})e^{-0.6LAI}\cdot2.5LAI,\ 0.005\big)$ |
| son | konstanta |

$LAI$ NaN → $Z_{om}$ NaN.

---

## 7. Monin–Obukhov funksiyalari

$z_1 = 0.1$, $z_2 = 2.0$, $z_3 = 200$ m (`z_flt_dict`).

| Funksiya | Formula |
|---|---|
| `u_star_func(u3, z3, zom, psi_z3, wind_coef=1)` | $u_* = \dfrac{k\,u_{200}}{\ln(200/Z_{om}) - \psi_{200}}$ |
| `rah_func(z, psi_z2, psi_z1, u*)` | $r_{ah} = \dfrac{\ln(z_2/z_1) - \psi_2 + \psi_1}{k\,u_*}$ |
| `density_func(elev, ts, dt)` | $\rho = \dfrac{1000\cdot P(z)}{1.01\cdot287\,(T_s - dT)}$ |
| `dt_calibration_func(h, rah, rho)` | $dT = H r_{ah}/(1004\rho)$ |
| `l_calibration_func(h, rho, u*, ts)` | $L = -1004\rho u_*^3T_s/(0.41\cdot9.81H)$, $H = 0 \Rightarrow -1000$ |
| `l_func(dt, u*, ts, rah)` (raster) | $L = -u_*^3T_sr_{ah}/(0.41\cdot9.81\,dT)$, $dT = 0 \Rightarrow -1000$ |
| `x_func(L, z)` | $x = (1 - 16z/L)^{1/4}$, $L > 0 \Rightarrow 0$ |
| `psi_func(L, z_index, z)` | beqaror: $\psi_{200} = 2\ln\frac{1+x}{2} + \ln\frac{1+x^2}{2} - 2\arctan x + \frac{\pi}{2}$; $\psi_{2,0.1} = 2\ln\frac{1+x^2}{2}$. Barqaror: $\psi_{200} = -5\cdot2/L$, $\psi_z = -5z/L$ |
| `h_func(rho, dt, rah)` | $H = 1004\rho\,dT/r_{ah}$ |

> Damping (o'rtachalash) **yo'q**: har iteratsiyada $\psi$ to'g'ridan-to'g'ri yangilanadi.

---

## 8. Kalibratsiya iteratsiyasi (2 piksel)

```python
LE = etr * kc * (2.501 - 2.361e-3*(Ts - 273)) * 2500/9     # le_calibration_func, W/m2
H  = Rn - G - LE
a, b = 1, -1000;  psi = 0;  dT = Ts - 293
for it in range(stabil_pixel_iter_max):                      # MANUAL: 20, AUTO/AUTO2: 100
    u*   = u_star_func(u200, 200, zom, psi[3])
    rah  = rah_func(z, psi[2], psi[1], u*)
    rho  = density_func(elev, Ts, dT)
    dT   = H * rah / (1004 * rho)
    a    = (dT_hot - dT_cold) / (Ts_dem_hot - Ts_dem_cold)
    b    = dT_cold - a * Ts_dem_cold
    L    = l_calibration_func(H, rho, u*, Ts)
    psi  = {1: psi_func(L,1,0.1), 2: psi_func(L,2,2), 3: psi_func(L,3,200)}
    if AUTO and |a-a_old|<0.001 and |b-b_old|<0.001: break
```

$\lambda/3600$: $(2.501 - 0.002361(T_s - 273))\cdot10^6/3600 = (\dots)\cdot2500/9$ ✔️

| `stability_pixel_mode` | Xatti-harakat |
|---|---|
| `MANUAL` | `stability_pixel_iters` (20) marta, konvergensiya tekshiruvisiz |
| `AUTO` | ≤ 100 iteratsiya, tolerans 0.001 |
| **`AUTO2`** (template default) | AUTO + yaqinlashmasa `additional_wind_speed` ni 0, 0.5, …, 2.0 m/s qilib qayta urinadi |

Xato holatlari: $a$ yoki $b$ NaN; $\lvert a\rvert > 100$ yoki $\lvert b\rvert > 10000$ ("not converging").

---

## 9. Raster bosqichi

```python
dT  = a * Ts_dem + b                                         # dt_func
psi = 0;  L = 0
for it in range(stability_raster_iters):                    # MANUAL: 6, AUTO: 10
    u*  = u_star_func(u200, 200, zom, psi_z3)
    rah = rah_func(z, psi_z2, psi_z1, u*)
    L   = l_func(dT, u*, Ts, rah)
    psi_z3, psi_z2, psi_z1 = psi_func(L,3,200), psi_func(L,2,2), psi_func(L,1,0.1)
u*  = u_star_func(...);  rah = rah_func(...)
rho = density_func(elev, Ts, dT)
H   = 1004 * rho * dT / rah                                  # h_func
LE  = Rn - G - H                                             # le_func
```

### 9.1 ET

| Kattalik | Formula | Funksiya |
|---|---|---|
| $\lambda$ | $(2.501 - 0.00236(T_s - 273.15))\times10^6$ | `heat_vaporization_func` |
| $ET_{inst}$ | $3600\,LE/\lambda$ [mm/h] | `et_inst_func` |
| $ET_rF$ | $ET_{inst}/ET_r$ ($ET_r$ — cold nuqtadagi soatlik qiymat) | `etrf_func` |
| $ET_{24}$ | $ET_rF\cdot ET_{r,24}$ | `et_24_func` |
| EF (o'chirilgan) | $LE/(R_n - G)$ | `ef_func` |

Chiqishlar (default `save_etrf_raster_flag = True`): `ETRF/et_rf.img`. Ixtiyoriy: `rn`, `rn_24`, `g`, `g_water/snow/wetland`, `zom`, `dt`, `h`, `psi_z1/2/3`, `l_stabil`, `rah`, `u_star`, `le`, `et_inst`, `et_24`.

> 🧠 Chegaralash (clamp) **yo'q**: ETrF manfiy yoki > 1.3 bo'lishi mumkin. Cheklash keyin interpolyatsiyada (`low_etrf_limit`, `high_etrf_limit`) qilinadi ([06](06_interpolation.md)).

> ⚠️ $H$ qiyalik bo'yicha tuzatilmaydi, $u_{200}$ va $ET_r$ sahna uchun konstanta, spatial delapsing yo'q.
