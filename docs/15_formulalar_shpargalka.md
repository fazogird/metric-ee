# 15 — Formulalar shpargalkasi (barcha asosiy tenglamalar bir joyda)

> Har bir qator → kod joyi → batafsil hujjat. Birliklar: T [K] (agar °C deyilmagan bo'lsa), radiatsiya [W/m²], ET [mm].

---

## A. Preprocessing

| # | Kattalik | Formula | Kod | Hujjat |
|---|---|---|---|---|
| A1 | SR | $\rho = 2.75\times10^{-5}DN - 0.2$ | `eeflux.from_landsat_c2_sr` | [01](01_preprocessing_landsat.md) |
| A2 | ST (USGS) | $T = 0.00341802\,DN + 149$ | ″ | [01](01_preprocessing_landsat.md) |
| A3 | ASTER→LS ε | $\varepsilon_{GED} = c_{13}\varepsilon_{13} + c_{14}\varepsilon_{14} + c$ | core `landsat_c2_sr_emissivity_correct` | [01](01_preprocessing_landsat.md) |
| A4 | fc | $f_c = \mathrm{clamp}((NDVI - 0.15)/0.65, 0, 1)$ | ″ | [01](01_preprocessing_landsat.md) |
| A5 | Soil ε | $\varepsilon_s = (\varepsilon_{GED} - 0.9798f_c^A)/(1 - f_c^A)$ | ″ | [01](01_preprocessing_landsat.md) |
| A6 | Landsat ε | $\varepsilon = (1-f_c)\varepsilon_s + 0.99f_c$ | ″ | [01](01_preprocessing_landsat.md) |
| A7 | Surface radiance | $R_c = (L - L_\uparrow)/\tau - (1-\varepsilon)L_\downarrow$ | core `landsat_c2_sr_lst_correct` | [01](01_preprocessing_landsat.md) |
| A8 | LST | $T_s = K_2/\ln(\varepsilon K_1/R_c + 1)$ | ″ | [01](01_preprocessing_landsat.md) |

## B. Yuza xususiyatlari

| # | Kattalik | Formula | Hujjat |
|---|---|---|---|
| B1 | Albedo | $\alpha = 0.2545\rho_B + 0.1486\rho_G + 0.148\rho_R + 0.31\rho_{NIR} + 0.1025\rho_{S1} + 0.0364\rho_{S2}$ | [02](02_albedo_ndvi_lai.md) |
| B2 | Tall veg α | $\min(\max(0.12, (1 + (2-2\cos\theta)NDVI/0.8)\alpha), \max(0.23, \alpha))$ | [02](02_albedo_ndvi_lai.md) |
| B3 | Ag α (α<0.18) | $\alpha + (0.18 - \alpha)\,\mathrm{clamp}((NDVI-0.45)/0.25, 0, 1)$ | [02](02_albedo_ndvi_lai.md) |
| B4 | NDVI | $\mathrm{clamp}((\rho_{NIR}-\rho_R)/(\rho_{NIR}+\rho_R), -1, 1)$ | [02](02_albedo_ndvi_lai.md) |
| B5 | LAI | $\min(10\max(NDVI,0)^{3.5}, 6)$ | [02](02_albedo_ndvi_lai.md) |
| B6 | NDSI | $(\rho_G - \rho_{S1})/(\rho_G + \rho_{S1})$ | [02](02_albedo_ndvi_lai.md) |
| B7 | Residue % | $788.4\rho_{S1} - 711.5\rho_{S2} - 39.16$ | [02](02_albedo_ndvi_lai.md) |
| B8 | ε₀ (broadband) | $0.95 + 0.01LAI$ ($LAI>3$: 0.98; suv/qor: 0.985) | [05](05_common_products.md) |
| B9 | ε_NB (legacy) | $0.97 + 0.0033LAI$ | [03](03_surface_temperature.md) |

## C. Atmosfera va quyosh

| # | Kattalik | Formula | Hujjat |
|---|---|---|---|
| C1 | Bosim | $P = 101.3((293.15 - 0.0065z)/293.15)^{5.26}$ | [05](05_common_products.md) |
| C2 | $e_a$ | $Pq/(0.622 + 0.378q)$ | [05](05_common_products.md) |
| C3 | $e^\circ$ | $0.6108\exp(17.27T/(T+237.3))$, T °C | [04](04_weather_reference_et.md) |
| C4 | δ | $0.409\sin(2\pi J/365 - 1.39)$ | [05](05_common_products.md) |
| C5 | $d_r$ | $1 + 0.033\cos(2\pi J/365)$ | [06](06_net_radiation.md) |
| C6 | $S_c$ | $0.1645\sin2b - 0.1255\cos b - 0.025\sin b$, $b = 2\pi(J-81)/364$ | [05](05_common_products.md) |
| C7 | ω | $\frac{\pi}{12}(t_{UTC} + 12\lambda/\pi + S_c - 12)$ | [05](05_common_products.md) |
| C8 | cos θ (flat) | $\sin\delta\sin\varphi + \cos\delta\cos\varphi\cos\omega$ | [05](05_common_products.md) |
| C9 | cos θ (mtn) | Duffie–Beckman 5 hadli, $/\cos s$, min 0.1 | [05](05_common_products.md) |
| C10 | $\tau_B$ | $0.98\exp[-0.00146P/(K_t\cos\theta) - 0.075(W/\cos\theta)^{0.4}]$, $W = 0.14e_aP + 2.1$ | [06](06_net_radiation.md) |
| C11 | $\tau_D$ | $0.35 - 0.36\tau_B$ ($\tau_B\ge0.15$), aks holda $0.18 + 0.82\tau_B$ | [06](06_net_radiation.md) |
| C12 | $u_{200}$ | $u_{10}\ln(200/Z_{om})/\ln(10/Z_{om})$, sahna o'rtachasi, H uchun ≥ 5 | [05](05_common_products.md) |

## D. Temperatura delapsing

| # | Kattalik | Formula | Hujjat |
|---|---|---|---|
| D1 | Lapse (flat) | $\Delta T = \Gamma_f(z - z_d)/1000$ | [03](03_surface_temperature.md) |
| D2 | Lapse (2 qism) | $\Gamma_f(z_L - z_d) + \Gamma_m(z - z_L)$, /1000 | [03](03_surface_temperature.md) |
| D3 | Spatial | $T_{fc} = c_\lambda\lambda + c_\varphi\varphi + c_0$; $\Delta T_{sp} = T_{fc} - T_{fc}(datum)$ | [11](11_lapsed_surface_regions.md) |
| D4 | Ts_dem_latlon | $T_s + \Delta T_{std} - \Delta T_{sp}$ | [03](03_surface_temperature.md) |
| D5 | Canopy T | $(T_s - f_{sh}(T_c - \Delta_{sh}) - f_{sun}(T_c + \Delta_{sun}))/f_{veg}$ | [03](03_surface_temperature.md) |
| D6 | Low-α T | $T + \Delta\alpha\cdot\frac{2}{K_{cc}-K_{ch}}(T_{hot}-T_{cold})$ | [03](03_surface_temperature.md) |

## E. Radiatsiya balansi

| # | Kattalik | Formula | Hujjat |
|---|---|---|---|
| E1 | $R_{so,inst}$ (mtn) | $\tau_BG_{sc}d_r\cos\theta_m + \tau_DG_{sc}d_r\cos\theta_h f_{sky} + R_{so}^f 0.2(1-f_{sky})$ | [06](06_net_radiation.md) |
| E2 | $f_{sky}$ | $0.75 + 0.25\cos s - 0.5s/\pi$ | [06](06_net_radiation.md) |
| E3 | $\varepsilon_a$ | $0.85(-\ln\tau_{sw})^{0.09}$ | [06](06_net_radiation.md) |
| E4 | $R_{L\downarrow}$ | $\varepsilon_a\sigma T_{cold}^4 f_{sky} + \varepsilon_0\sigma T_{terr}^4(1-f_{sky})$ | [06](06_net_radiation.md) |
| E5 | $R_n$ | $(1-\alpha')R_{so} + R_{L\downarrow} - \varepsilon_0\sigma T_s^4 - (1-\varepsilon_0)R_{L\downarrow}$ | [06](06_net_radiation.md) |
| E6 | $C_{rad}$ | $\min(\frac{R_{so,i}^f}{R_{so,i}}\cdot\frac{R_{so,24}}{R_{so,24}^f}, 1.5)$ | [06](06_net_radiation.md) |
| E7 | $R_{n,24}$ (Slob) | $\frac{24(1-\alpha')R_{so,24}}{12 + 0.5N} - R_{nl}k_{mtn}$ | [12](12_etrf_et24_soil_water_balance.md) |

## F. Soil heat flux

| # | Yuza | Formula | Hujjat |
|---|---|---|---|
| F1 | Quruqlik | $(0.1 + 0.17e^{-0.55LAI})R_n\cdot M_{om}$ | [07](07_soil_heat_flux.md) |
| F2 | Suv | $(-1.25 + 0.0217J - 5.87\cdot10^{-5}J^2)R_n$ → keyin residual | [07](07_soil_heat_flux.md) |
| F3 | Qor | $0.5R_n$ → keyin residual | [07](07_soil_heat_flux.md) |
| F4 | Wetland | $\mathrm{clamp}((0.05 + 0.6e^{-0.8LAI})R_n, 0.05R_n, 0.41R_n - 51)$ | [07](07_soil_heat_flux.md) |
| F5 | Issiq | $G - 5(T_{s,dem} - T_{thr})$ | [07](07_soil_heat_flux.md) |
| F6 | Suv/qor residual | $R_n - H - E_{aero}\lambda/3600$ | [07](07_soil_heat_flux.md) |

## G. Aerodinamika

| # | Kattalik | Formula | Hujjat |
|---|---|---|---|
| G1 | Zom (ekin) | $0.018\max(LAI, 0.2778)$ | [08](08_momentum_roughness.md) |
| G2 | Zom (Perrier) | $(1 - e^{-aL/2})e^{-aL/2}\cdot mL$, $a = 1.2$ | [08](08_momentum_roughness.md) |
| G3 | Zom (suv) | $\max(2.4\cdot10^{-7}u_{200}^{2.55}, 5\cdot10^{-5})$ | [08](08_momentum_roughness.md) |
| G4 | Zom (tog') | $Z + C\cdot3\sin^3(\frac{\pi}{2}\frac{\sigma_z}{200})(Z/7 + 0.3)$ | [08](08_momentum_roughness.md) |
| G5 | $u_*$ | $k u_{200}/(\ln(200/Z_{om}) - \psi_{200})$ | [09](09_sensible_heat_flux.md) |
| G6 | $r_{ah}$ | $(\ln(2/0.1) - \psi_2 + \psi_{0.1})/(ku_*) + r_{extra}$ | [09](09_sensible_heat_flux.md) |
| G7 | L | $-\rho c_p u_*^3T_s/(kgH)$ | [09](09_sensible_heat_flux.md) |
| G8 | ψ (beqaror) | Paulson: $x = (1-16z/L)^{1/4}$ | [09](09_sensible_heat_flux.md) |
| G9 | ψ (barqaror) | $-5z/L$ ($\psi_{200}$ uchun $z = 2$) | [09](09_sensible_heat_flux.md) |

## H. Kalibratsiya va H

| # | Kattalik | Formula | Hujjat |
|---|---|---|---|
| H1 | $K_{c,cold}$ | $\mathrm{clamp}((NDVI - 0.15)/0.65, 0.11, 1)$ | [10](10_pixel_selection.md) |
| H2 | $K_{c,hot}$ | $\mathrm{clamp}((NDVI - 0.15)/0.65, 0.05, 0.95)$ | [10](10_pixel_selection.md) |
| H3 | $LE$ (hot/cold) | $K_c\cdot ET_{r,inst}\cdot\lambda/3600$ | [09](09_sensible_heat_flux.md) |
| H4 | $H$ (hot/cold) | $R_n - (0.1 + 0.17e^{-0.55LAI})R_n - LE$ | [09](09_sensible_heat_flux.md) |
| H5 | dT | $Hr_{ah}/(\rho c_p)$ | [09](09_sensible_heat_flux.md) |
| H6 | a, b | $a = \Delta dT/\Delta T_{s,dem}$, $b = dT_c - aT_c$ | [09](09_sensible_heat_flux.md) |
| H7 | $T_{dry}$ | $T_h + K_{ch}(T_h - T_c)/(K_{cc} - K_{ch})$ | [09](09_sensible_heat_flux.md) |
| H8 | dT (ekstr.) | qiyalik $a/8$ ($T > T_{dry}+2$ yoki $T < T_c - 2$) | [09](09_sensible_heat_flux.md) |
| H9 | $\rho_a$ | $3.486P/(1.01(T_s - dT))$ | [09](09_sensible_heat_flux.md) |
| H10 | **H** | $\rho_a c_p\,dT/(r_{ah}\cos s)$ | [09](09_sensible_heat_flux.md) |
| H11 | $\alpha_{alf}$ | $0.03 + 0.001343\beta + 0.3281e^{-0.0188\beta}$ | [10](10_pixel_selection.md) |
| H12 | Reyting | $\mathrm{clamp}(c/\vert x - x_0\vert , 0, 1)$ | [10](10_pixel_selection.md) |
| H13 | Q | $r_hr_c[\Delta T>4][0.01<a<1]$ | [10](10_pixel_selection.md) |

## I. ET

| # | Kattalik | Formula | Hujjat |
|---|---|---|---|
| I1 | λ | $(2.501 - 0.00236(T_s - 273.15))\times10^6$ | [12](12_etrf_et24_soil_water_balance.md) |
| I2 | $ET_{inst}$ | $3600(R_n - G - H)/\lambda$ [mm/h] | [12](12_etrf_et24_soil_water_balance.md) |
| I3 | $ET_rF_{inst}$ | $ET_{inst}/ET_{r,inst}^{cold}\times C_{rad}$ | [12](12_etrf_et24_soil_water_balance.md) |
| I4 | $ET_{24}$ (ag) | $ET_rF_{inst}\cdot ET_{r,24}$ | [12](12_etrf_et24_soil_water_balance.md) |
| I5 | $ET_{24}^{EF}$ (non-ag) | $ET_{inst}\frac{0.5N + 12}{R_n - G}(R_{n,24} - 0.5G)\cdot k_s$ | [12](12_etrf_et24_soil_water_balance.md) |
| I6 | $E_{aero}$ (suv) | $3600\rho_a(q_s - q_a)/r_{a,w}$ [mm/h] | [09](09_sensible_heat_flux.md) |
| I7 | **EToF** | $\min(ET_rF, 2\vert 1.3)\cdot ET_{r,inst}/ET_{o,inst}$ | [12](12_etrf_et24_soil_water_balance.md) |
| I8 | **ET** | $EToF\times ET_o$ | [12](12_etrf_et24_soil_water_balance.md) |
| I9 | Interpolyatsiya | $V(t) = V_p + \frac{t - t_p}{t_n - t_p}(V_n - V_p)$ | [13](13_collection_interpolation.md) |
| I10 | Oylik EToF | $\sum ET_d/\sum ET_{o,d}$ | [13](13_collection_interpolation.md) |

## J. Reference ET (ASCE)

| # | Kattalik | Formula | Hujjat |
|---|---|---|---|
| J1 | Kunlik PM | $\frac{0.408\Delta R_n + \gamma\frac{C_n}{T+273}u_2(e_s - e_a)}{\Delta + \gamma(1 + C_du_2)}$; ETr: 1600/0.38, ETo: 900/0.34 | [04](04_weather_reference_et.md) |
| J2 | Soatlik PM | ETr: $C_n$=66, $C_d$=0.25/1.7; ETo: 37, 0.24/0.96 | [04](04_weather_reference_et.md) |
| J3 | $u_2$ | $u_z\cdot4.87/\ln(67.8z_w - 5.42)$ | [04](04_weather_reference_et.md) |
| J4 | ETr reduksiya | gridMET/CFSv2 ETr × **0.85**; instant ETr, ETo × 0.85 | [04](04_weather_reference_et.md) |

## K. Soil water balance

| # | Kattalik | Formula | Hujjat |
|---|---|---|---|
| K1 | TEW | $1000(\theta_{FC} - 0.5\theta_{WP})Z_e$ | [12](12_etrf_et24_soil_water_balance.md) |
| K2 | REW | $\min(0.8 + 54.4(\theta_{FC} - \theta_{WP}), TEW)$ | [12](12_etrf_et24_soil_water_balance.md) |
| K3 | $K_r$ | $(TEW - D_e)/(TEW - REW)$ | [12](12_etrf_et24_soil_water_balance.md) |
| K4 | $f_t$ | $(REW - D_{REW})/(K_{e,max}ET_r)$ | [12](12_etrf_et24_soil_water_balance.md) |
| K5 | $K_e$ | $(f_t + (1 - f_t)K_r)K_{e,max}$ | [12](12_etrf_et24_soil_water_balance.md) |

## Konstantalar

| Belgi | Qiymat |
|---|---|
| $G_{sc}$ | 1367 W/m² (yoki 4.92 MJ/m²/h ASCE da) |
| σ | 5.67×10⁻⁸ W/m²/K⁴ |
| k | 0.41 |
| g | 9.81 m/s² |
| $c_p$ | 1004 J/kg/K |
| R | 287 J/kg/K |
| ε (q) | 0.622 |
