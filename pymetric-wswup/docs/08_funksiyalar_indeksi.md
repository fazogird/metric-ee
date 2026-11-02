# 08 — Funksiyalar indeksi (pymetric, WSWUP)

> Avtomatik generatsiya: `ast` bilan `code/**/*.py`. Manba: [WSWUP/pymetric@c3a47fb](https://github.com/WSWUP/pymetric/tree/c3a47fb0d5f98dd8746f557038b6291350ea0916) (yuklangan zip bilan bir xil).
> Qator raqami — GitHub permalink. Tavsif: o'zbekcha (ma'lum funksiyalar) yoki docstringning birinchi qatori (*kursiv*, inglizcha).
> Jami: **205** ta funksiya/metod (23 modul, `code/` papkasi). `tools/` skriptlari — [07](07_tools_weather.md).

## `code/support/et_numpy.py` — Fizik formulalar

Batafsil: [02_model1.md](02_model1.md), [04_model2.md](04_model2.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `cos_theta_spatial_func` | [14](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L14) | Piksel lat/lon bo'yicha cos θ (🐛 argument tartibi) |
| 2 | `cos_theta_mountain_func` | [37](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L37) | Qiyalikdagi cos θ / cos s, min 0.1 (🐛 argument tartibi) |
| 3 | `l457_refl_toa_func` | [164](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L164) | L4/5/7 DN → TOA (ko'p band) |
| 4 | `l457_refl_toa_band_func` | [208](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L208) | L4/5/7 DN → TOA (bitta band) |
| 5 | `l457_ts_bt_band_func` | [246](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L246) | L4/5/7 DN → BT |
| 6 | `l8_refl_toa_band_func` | [278](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L278) | L8 DN → TOA ($M_\rho DN + A_\rho$)/cos θ |
| 7 | `l8_ts_bt_band_func` | [308](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L308) | L8 DN → BT |
| 8 | `bqa_fmask_func` | [335](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L335) | C1 BQA → Fmask (0/1/2/3/4) |
| 9 | `tau_broadband_func` | [379](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L379) | $\tau_B + \tau_D$ |
| 10 | `tau_direct_func` | [405](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L405) | $\tau_B$ (Tasumi 2008) |
| 11 | `tau_diffuse_func` | [446](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L446) | $0.35 - 0.36\tau_B$ |
| 12 | `tau_narrowband_func` | [479](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L479) | Band $\tau$ ($C_1..C_5$) |
| 13 | `refl_sur_tasumi_func` | [528](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L528) | Tasumi at-surface reflectance |
| 14 | `albedo_sur_func` | [592](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L592) | $\sum w_b\rho_b$ |
| 15 | `ndi_func` | [616](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L616) | Normalized difference / SAVI |
| 16 | `savi_lai_func` | [650](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L650) | $\mathrm{clip}(11SAVI^3, 0, 6)$ |
| 17 | `ndvi_lai_func` | [673](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L673) | $\mathrm{clip}(7NDVI^3, 0, 6)$ |
| 18 | `ratio_func` | [693](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L693) | $a/b$ |
| 19 | `evi_func` | [709](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L709) | EVI |
| 20 | `tc_bright_func` | [736](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L736) | Tasseled cap brightness |
| 21 | `tc_green_func` | [767](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L767) | Tasseled cap greenness |
| 22 | `tc_wet_func` | [792](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L792) | Tasseled cap wetness |
| 23 | `etstar_func` | [819](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L819) | ET* (EVI kvadratik) |
| 24 | `etstar_etg_func` | [862](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L862) | $ET^*(ET_o - P)$ |
| 25 | `etstar_et_func` | [882](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L882) | $ET^*(ET_o - P) + P$ |
| 26 | `em_nb_func` | [902](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L902) | $0.97 + LAI/300$ |
| 27 | `em_0_func` | [944](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L944) | $0.95 + LAI/100$ |
| 28 | `rc_func` | [985](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L985) | Korreksiyalangan termal radiance |
| 29 | `ts_func` | [1028](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1028) | $K_2/\ln(\varepsilon K_1/R_c + 1)$ |
| 30 | `ts_bt_func` | [1069](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1069) | Radiance → BT |
| 31 | `thermal_rad_func` | [1108](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1108) | BT → radiance |
| 32 | `ts_lapsed_func` | [1146](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1146) | $T - \Gamma(z - z_d)/1000$ |
| 33 | `ts_delapsed_func` | [1178](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1178) | $T + \Gamma(z - z_d)/1000$ |
| 34 | `rl_in_func` | [1210](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1210) | $0.85(-\ln\tau)^{0.09}\sigma T^4$ |
| 35 | `rl_out_func` | [1250](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1250) | $\varepsilon_0\sigma T^4 + (1-\varepsilon_0)R_{L\downarrow}$ |
| 36 | `rs_in_func` | [1287](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1287) | $G_{sc}d_r\tau\cos\theta$ |
| 37 | `rs_out_func` | [1320](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1320) | $\alpha R_{s\downarrow}$ |
| 38 | `rn_func` | [1351](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1351) | $R_n$ |
| 39 | `rn_24_func` | [1388](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1388) | Slob $R_{n,24}$ (cs = 110) |
| 40 | `g_ag_func` | [1447](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1447) | METRIC G (Tasumi 2003) |
| 41 | `g_sebal_func` | [1499](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1499) | SEBAL G/Rn (⚠️ nisbat) |
| 42 | `zom_func` | [1541](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1541) | NLCD → Zom (JSON: son / perrier / LAI) |
| 43 | `perrier_zom_func` | [1588](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1588) | Perrier Zom |
| 44 | `le_calibration_func` | [1631](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1631) | $ET_rK_c\lambda/3600$ |
| 45 | `dt_calibration_func` | [1660](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1660) | $Hr_{ah}/(1004\rho)$ |
| 46 | `l_calibration_func` | [1691](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1691) | L (H dan) |
| 47 | `h_func` | [1727](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1727) | $1004\rho dT/r_{ah}$ |
| 48 | `u_star_func` | [1762](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1762) | $ku_{200}/(\ln(200/Z_{om}) - \psi_{200})$ |
| 49 | `rah_func` | [1808](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1808) | $(\ln(z_2/z_1) - \psi_2 + \psi_1)/(ku_*)$ |
| 50 | `density_func` | [1847](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1847) | $1000P/(1.01\cdot287(T_s - dT))$ |
| 51 | `x_func` | [1887](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1887) | $(1 - 16z/L)^{1/4}$ |
| 52 | `psi_func` | [1924](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L1924) | Paulson ψ (barqaror: $-5z/L$) |
| 53 | `dt_func` | [2008](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L2008) | $aT_{s,dem} + b$ |
| 54 | `l_func` | [2043](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L2043) | L (dT dan) |
| 55 | `le_func` | [2086](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L2086) | $R_n - G - H$ |
| 56 | `ef_func` | [2120](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L2120) | $LE/(R_n - G)$ |
| 57 | `heat_vaporization_func` | [2160](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L2160) | λ [J/kg] |
| 58 | `et_inst_func` | [2192](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L2192) | $3600LE/\lambda$ [mm/h] |
| 59 | `etrf_func` | [2224](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L2224) | $ET_{inst}/ET_r$ |
| 60 | `et_24_func` | [2249](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_numpy.py#L2249) | $ET_rF\cdot ET_{r,24}$ |

## `code/support/et_common.py` — Quyosh, atmosfera, SWB, RefET o'qish

Batafsil: [02_model1.md](02_model1.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `landsat_folder_split` | [23](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L23) | Landsat papka nomini bo'laklash |
| 2 | `landsat_id_split` | [64](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L64) | Landsat ID ni bo'laklash |
| 3 | `band_dict_to_array` | [90](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L90) | Band lug'ati → massiv |
| 4 | `landsat_band_image_dict` | [108](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L108) | Band → fayl lug'ati |
| 5 | `doy_range_func` | [141](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L141) | Interpolyatsiya DOY oralig'i |
| 6 | `read_refet_instantaneous_func` | [206](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L206) | Stansiya CSV: overpass soati qiymatlari |
| 7 | `read_refet_daily_func` | [419](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L419) | Stansiya CSV: kunlik ETr/ETo |
| 8 | `read_nvet_daily_func` | [511](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L511) | NVET kunlik |
| 9 | `read_csv_etr_daily_func` | [575](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L575) | CSV kunlik ETr |
| 10 | `fixed_etr_data_func` | [649](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L649) | Konstanta ETr |
| 11 | `u_star_station_func` | [666](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L666) | $ku/\ln(z_w/z_0)$ |
| 12 | `u3_func` | [685](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L685) | $u_*\ln(200/z_0)/k$ |
| 13 | `saturation_vapor_pressure_func` | [702](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L702) | $e^\circ(T)$ kPa |
| 14 | `doy_fraction_func` | [729](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L729) | $2\pi J/365$ |
| 15 | `delta_func` | [744](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L744) | Deklinatsiya |
| 16 | `air_pressure_func` | [759](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L759) | $P(z)$ kPa |
| 17 | `precipitable_water_func` | [785](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L785) | $0.14e_aP + 2.1$ |
| 18 | `dr_func` | [814](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L814) | $1 + 0.033\cos(2\pi J/365)$ |
| 19 | `ee_dr_func` | [836](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L836) | EE versiyasi $d_r$ |
| 20 | `seasonal_correction_func` | [852](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L852) | $S_c$ [soat] |
| 21 | `solar_time_rad_func` | [869](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L869) | $t + 24\lambda/2\pi + S_c - 12$ (signatura: lon, time, sc) |
| 22 | `omega_func` | [899](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L899) | Soat burchagi, wrap(−π, π) |
| 23 | `wrap_func` | [921](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L921) | Qiymatni oraliqqa o'rash |
| 24 | `omega_sunset_func` | [941](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L941) | $\arccos(-\tan\varphi\tan\delta)$ |
| 25 | `ra_daily_func` | [959](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L959) | Kunlik $R_a$ (MJ/m²/d) |
| 26 | `cos_theta_solar_func` | [989](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L989) | $\sin\beta$ |
| 27 | `cos_theta_centroid_func` | [994](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L994) | Sahna markazidagi cos θ |
| 28 | `cell_value_set` | [1038](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L1038) | Raster qiymati cold/hot nuqtada |
| 29 | `raster_swb_func` | [1074](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L1074) | Raster SWB (Ke) |
| 30 | `clip_project_raster_func` | [1298](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L1298) | Kesish + qayta proyeksiya |
| 31 | `point_swb_func` | [1342](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L1342) | Nuqtadagi SWB (Ke) |
| 32 | `array_swb_func` | [1605](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L1605) | Kunlik stack bo'yicha SWB |
| 33 | `daily_swb_func` | [1684](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_common.py#L1684) | Bir kunlik SWB qadam |

## `code/support/et_image.py` — Landsat sahna klassi

Batafsil: [01_prep_landsat.md](01_prep_landsat.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `Image.__init__` | [27](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_image.py#L27) | Sensor turi, koeffitsientlar, MTL, CRS |
| 2 | `Image.read_mtl` | [256](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_image.py#L256) | MTL faylini o'qish |
| 3 | `Image.process_mtl` | [379](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_image.py#L379) | acq_time, doy, dr, cos θ, EPSG |
| 4 | `Image.set_folder_paths` | [431](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_image.py#L431) | Sahna pastki papkalari |
| 5 | `Image.set_raster_paths` | [450](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_image.py#L450) | Raster yo'llari (.img) |
| 6 | `Image.convert_solar_time` | [516](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/et_image.py#L516) | Lokal vaqt (🐛 sin daraja bilan; ishlatilmaydi) |

## `code/support/python_common.py` — Python yordamchilari

Batafsil: [00_arxitektura.md](00_arxitektura.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `arg_valid_file` | [25](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L25) | *Argparse specific function for testing if file exists* |
| 2 | `build_file_list` | [37](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L37) | *Return a list of files in a folder matching a regular expression* |
| 3 | `call_mp` | [49](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L49) | *Pool multiprocessing friendly subprocess call function* |
| 4 | `call_sp` | [58](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L58) | *Parameters* |
| 5 | `count_digits_func` | [93](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L93) | *Return the number of digits in a number* |
| 6 | `date_range` | [98](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L98) | *Yield datetimes within a date range* |
| 7 | `extract_targz_mp` | [104](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L104) | *Pool multiprocessing friendly tar.gz extract function* |
| 8 | `extract_targz_func` | [113](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L113) | — |
| 9 | `extract_hdfgz_mp` | [128](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L128) | *Pool multiprocessing friendly hdf extract function* |
| 10 | `extract_hdfgz_func` | [137](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L137) | — |
| 11 | `isfloat` | [149](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L149) | *Test if an object is a float* |
| 12 | `doy2month` | [158](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L158) | *Return the month for a given day of year and year* |
| 13 | `list_flatten` | [164](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L164) | *Return a flattened copy of a nested list* |
| 14 | `month_range_func` | [169](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L169) | *Return a list of months for a given day of year range* |
| 15 | `month2doy` | [176](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L176) | *Return a list of the day of years in a month* |
| 16 | `open_ini` | [183](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L183) | *Open config file* |
| 17 | `parse_int_set` | [210](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L210) | *Return list of numbers given a string of ranges* |
| 18 | `read_param` | [243](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L243) | — |
| 19 | `remove_file` | [287](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L287) | *Remove a feature/raster and all of its anciallary files* |
| 20 | `shuffle` | [294](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L294) | *Return a randomly shuffled copy of a list* |
| 21 | `valid_date` | [301](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L301) | *Check that a date string is ISO format (YYYY-MM-DD)* |
| 22 | `url_download` | [330](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L330) | *Download file from a URL using requests module* |
| 23 | `ftp_download` | [346](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/support/python_common.py#L346) | — |

## `code/prep_functions/landsat_prep_scene_func.py` — Sahna tayyorlash

Batafsil: [01_prep_landsat.md](01_prep_landsat.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `main` | [27](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/prep_functions/landsat_prep_scene_func.py#L27) | Asosiy funksiya |
| 2 | `common_area_func` | [1023](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/prep_functions/landsat_prep_scene_func.py#L1023) | Barcha bandlar ≠ 0 maskasi |
| 3 | `hourly_interpolate_func` | [1036](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/prep_functions/landsat_prep_scene_func.py#L1036) | Ikki soat orasida chiziqli interpolyatsiya |
| 4 | `arg_parse` | [1069](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/prep_functions/landsat_prep_scene_func.py#L1069) | CLI argumentlari |

## `code/metric_functions/metric_model1_func.py` — Model 1 orkestrator

Batafsil: [02_model1.md](02_model1.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `metric_model1` | [28](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/metric_model1_func.py#L28) | Model 1 asosiy funksiya |
| 2 | `arg_parse` | [1074](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/metric_model1_func.py#L1074) | CLI argumentlari |

## `code/metric_functions/pixel_rating_func.py` — Pixel rating

Batafsil: [03_pixel_rating_points.md](03_pixel_rating_points.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `pixel_rating` | [25](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/pixel_rating_func.py#L25) | Pixel rating asosiy funksiya |
| 2 | `nlcd_rating` | [707](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/pixel_rating_func.py#L707) | NLCD → reyting |
| 3 | `arg_parse` | [753](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/pixel_rating_func.py#L753) | CLI argumentlari |

## `code/metric_functions/pixel_points_func.py` — Pixel points

Batafsil: [03_pixel_rating_points.md](03_pixel_rating_points.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `pixel_points` | [23](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/pixel_points_func.py#L23) | Cold/hot nuqtalarni shapefile'ga |
| 2 | `get_random_point_in_raster` | [164](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/pixel_points_func.py#L164) | Klasterdan tasodifiy nuqta |
| 3 | `arg_parse` | [304](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/pixel_points_func.py#L304) | CLI argumentlari |

## `code/metric_functions/metric_model2_func.py` — Model 2 orkestrator

Batafsil: [04_model2.md](04_model2.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `metric_model2` | [27](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/metric_model2_func.py#L27) | Model 2 asosiy funksiya |
| 2 | `arg_parse` | [1742](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/metric_model2_func.py#L1742) | CLI argumentlari |

## `code/metric_functions/auto_calibration_func.py` — Avtokalibratsiya

Batafsil: [05_auto_calibration_monte_carlo.md](05_auto_calibration_monte_carlo.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `etrf_fractions` | [31](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L31) | Tail size (empirik CDF) |
| 2 | `sap_float` | [80](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L80) | Score at percentile |
| 3 | `pos_float` | [101](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L101) | Percentile of score |
| 4 | `calibration_params` | [117](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L117) | ETrF statistikalari |
| 5 | `check_calibration` | [181](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L181) | ±0.5% tekshiruv |
| 6 | `kc_calibration_adjust` | [209](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L209) | Kc chiziqli tuzatish |
| 7 | `remove_histograms` | [270](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L270) | Eski gistogrammalarni o'chirish |
| 8 | `calc_histogram_bins` | [304](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L304) | Bin chegaralari |
| 9 | `save_etrf_histograms` | [330](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L330) | ETrF gistogramma |
| 10 | `save_ndvi_histograms` | [425](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L425) | NDVI gistogramma |
| 11 | `build_pixel_points` | [469](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L469) | Target Kc ga eng yaqin nuqta → shapefile |
| 12 | `get_target_point_in_array` | [520](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L520) | $\arg\min\lvert x - target\rvert$ |
| 13 | `hot_kc_swb_adjust` | [543](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L543) | Hot Kc = clamp(Ke, 0.1, 1.05) |
| 14 | `arg_parse` | [627](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/auto_calibration_func.py#L627) | CLI argumentlari |

## `code/metric_functions/monte_carlo_func.py` — Monte Carlo

Batafsil: [05_auto_calibration_monte_carlo.md](05_auto_calibration_monte_carlo.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `monte_carlo` | [32](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/monte_carlo_func.py#L32) | Monte Carlo tsikli |
| 2 | `arg_parse` | [450](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/metric_functions/monte_carlo_func.py#L450) | CLI argumentlari |

## `code/interp_functions/interpolate_support.py` — Interpolyatsiya yordamchilari

Batafsil: [06_interpolation.md](06_interpolation.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `landsat_dt_func` | [27](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L27) | ID → sana |
| 2 | `daterange_func` | [34](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L34) | Sana generatori |
| 3 | `tile_wkt_func` | [42](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L42) | WRS-2 tile geometriyasi |
| 4 | `clip_project_raster_func` | [99](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L99) | Kesish + qayta proyeksiya |
| 5 | `mosaic_func` | [114](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L114) | first / last / mean mozaika |
| 6 | `load_etrf_func` | [152](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L152) | Tile'larni yuklab nanmean |
| 7 | `spatial_fill_func` | [348](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L348) | Bo'sh (stub) |
| 8 | `end_fill_func` | [380](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L380) | Yil chekkalarini to'ldirish |
| 9 | `temporal_fill_func` | [448](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L448) | Bulutli bo'shliqlarni to'ldirish |
| 10 | `interpolate_func` | [543](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L543) | Kunlik interpolyatsiya |
| 11 | `block_interpolate_func` | [755](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L755) | Blok interpolyatsiya (MP) |
| 12 | `block_interpolate_worker` | [832](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L832) | MP worker |
| 13 | `load_year_array_func` | [847](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L847) | Yillik ETr/PPT stack |
| 14 | `swb_adjust_fc` | [939](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L939) | fc (ishlatilmaydi) |
| 15 | `unknown_proj_osr` | [945](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_support.py#L945) | Proyeksiyani aniqlash |

## `code/interp_functions/interpolate_rasters_func.py` — Raster interpolyatsiya

Batafsil: [06_interpolation.md](06_interpolation.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `metric_interpolate` | [42](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_rasters_func.py#L42) | Interpolyatsiya asosiy funksiya |
| 2 | `block_worker` | [1572](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_rasters_func.py#L1572) | MP worker |
| 3 | `block_func` | [1584](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_rasters_func.py#L1584) | Bitta blokni hisoblash |
| 4 | `arg_parse` | [2072](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_rasters_func.py#L2072) | CLI argumentlari |

## `code/interp_functions/interpolate_tables_func.py` — Jadval (zona) interpolyatsiya

Batafsil: [06_interpolation.md](06_interpolation.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `metric_interpolate` | [46](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_tables_func.py#L46) | Interpolyatsiya asosiy funksiya |
| 2 | `block_worker` | [1341](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_tables_func.py#L1341) | MP worker |
| 3 | `block_func` | [1354](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_tables_func.py#L1354) | Bitta blokni hisoblash |
| 4 | `arg_parse` | [1719](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/interp_functions/interpolate_tables_func.py#L1719) | CLI argumentlari |

## `code/local/landsat_prep_path_row.py` — CLI: path/row tayyorlash

Batafsil: [00_arxitektura.md](00_arxitektura.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `main` | [38](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_path_row.py#L38) | Asosiy funksiya |
| 2 | `gcs_to_utm_dict` | [808](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_path_row.py#L808) | *Return a dictionary of Landsat path/row GCS extents projected to UTM* |
| 3 | `path_row_wkt_func` | [863](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_path_row.py#L863) | *Return a dictionary of Landsat path/rows and their geometries* |
| 4 | `feature_path_geom_union` | [882](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_path_row.py#L882) | *Union geometries of all feature in shapefile* |
| 5 | `mosaic_tiles_mp` | [902](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_path_row.py#L902) | *Pool multiprocessing friendly mosaic/project/clip function* |
| 6 | `remap_mask_mp` | [937](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_path_row.py#L937) | *Remap the input raster to all 1's and return a mask raster* |
| 7 | `remap_mask_func` | [954](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_path_row.py#L954) | *Remap the input raster to all 1's and return a mask raster* |
| 8 | `landsat_files_check` | [983](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_path_row.py#L983) | *Check if Landsat folder needs to be rebuilt from tar.gz* |
| 9 | `folder_check` | [1031](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_path_row.py#L1031) | — |
| 10 | `file_check` | [1040](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_path_row.py#L1040) | — |
| 11 | `arg_parse` | [1049](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_path_row.py#L1049) | CLI argumentlari |

## `code/local/landsat_prep_ini.py` — CLI: INI tayyorlash

Batafsil: [00_arxitektura.md](00_arxitektura.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `main` | [22](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_ini.py#L22) | Asosiy funksiya |
| 2 | `path_row_wkt_func` | [684](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_ini.py#L684) | *Return a dictionary of Landsat path/rows and their geometries* |
| 3 | `folder_check` | [716](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_ini.py#L716) | — |
| 4 | `file_check` | [725](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_ini.py#L725) | — |
| 5 | `arg_parse` | [734](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_ini.py#L734) | CLI argumentlari |

## `code/local/landsat_prep_scene.py` — CLI: sahna tayyorlash

Batafsil: [00_arxitektura.md](00_arxitektura.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `main` | [19](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_scene.py#L19) | Asosiy funksiya |
| 2 | `arg_parse` | [162](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_prep_scene.py#L162) | CLI argumentlari |

## `code/local/metric_model1.py` — CLI: Model 1

Batafsil: [00_arxitektura.md](00_arxitektura.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `main` | [19](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/metric_model1.py#L19) | Asosiy funksiya |
| 2 | `arg_parse` | [181](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/metric_model1.py#L181) | CLI argumentlari |

## `code/local/metric_pixel_rating.py` — CLI: pixel rating

Batafsil: [00_arxitektura.md](00_arxitektura.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `main` | [19](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/metric_pixel_rating.py#L19) | Asosiy funksiya |
| 2 | `arg_parse` | [176](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/metric_pixel_rating.py#L176) | CLI argumentlari |

## `code/local/metric_pixel_points.py` — CLI: pixel points

Batafsil: [00_arxitektura.md](00_arxitektura.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `main` | [19](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/metric_pixel_points.py#L19) | Asosiy funksiya |
| 2 | `arg_parse` | [179](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/metric_pixel_points.py#L179) | CLI argumentlari |

## `code/local/metric_model2.py` — CLI: Model 2

Batafsil: [00_arxitektura.md](00_arxitektura.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `main` | [19](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/metric_model2.py#L19) | Asosiy funksiya |
| 2 | `arg_parse` | [181](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/metric_model2.py#L181) | CLI argumentlari |

## `code/local/metric_monte_carlo.py` — CLI: Monte Carlo

Batafsil: [00_arxitektura.md](00_arxitektura.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `main` | [20](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/metric_monte_carlo.py#L20) | Asosiy funksiya |
| 2 | `arg_parse` | [264](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/metric_monte_carlo.py#L264) | CLI argumentlari |

## `code/local/landsat_interpolate.py` — CLI: interpolyatsiya

Batafsil: [00_arxitektura.md](00_arxitektura.md)

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `main` | [18](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_interpolate.py#L18) | Asosiy funksiya |
| 2 | `arg_parse` | [185](https://github.com/WSWUP/pymetric/blob/c3a47fb0d5f98dd8746f557038b6291350ea0916/code/local/landsat_interpolate.py#L185) | CLI argumentlari |

