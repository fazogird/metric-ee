# 14 — Funksiyalar indeksi (to'liq ro'yxat)

> Avtomatik generatsiya: `ast` bilan `openet/eemetric/*.py` dan. Manba commit: [`7c83a7d`](https://github.com/Open-ET/openet-eemetric/tree/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7).
> Qator raqami GitHub permalink. `EEFlux` klassi xususiyatlari — [00_arxitektura.md](00_arxitektura.md).
> Jami: **213** ta funksiya/metod (21 modul, `eeflux.py` dan tashqari).

## `surface_reflectance.py` — Atmosfera korreksiyasi (legacy METRIC)

Batafsil: [01_preprocessing_landsat.md](01_preprocessing_landsat.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `calculate_radiance` | [11](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_reflectance.py#L11) | DN → kalibrlangan radiance (`ee.Algorithms.Landsat.calibratedRadiance`) |
| 2 | `calculate_surface_reflectance_mm` | [16](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_reflectance.py#L16) | Mountain SR wrapper (self dan argumentlar) |
| 3 | `calculate_surface_reflectance_mm_general` | [27](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_reflectance.py#L27) | Tog'li SR: τ_in/τ_out, beam/diffuse, terrain reflectance |
| 4 | `calculate_toa_reflectance_mm` | [141](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_reflectance.py#L141) | SR → TOA teskari (wrapper) |
| 5 | `calculate_TOA_reflectance_mm_general` | [146](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_reflectance.py#L146) | $\rho_t = \rho_s\tau_{out}\tau_{in} + C_b(1-\tau_{in})$ |
| 6 | `calculate_toa_reflectance` | [197](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_reflectance.py#L197) | L1 → TOA (`Landsat.TOA`), bandlarni qayta nomlash + umumiy maska |
| 7 | `calculate_surface_reflectance` | [231](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_reflectance.py#L231) | Flat SR (Allen 2007 Eq. 11–14), `EEFluxFlat` uchun |

## `surface_albedo.py` — Albedo

Batafsil: [02_albedo_ndvi_lai.md](02_albedo_ndvi_lai.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `calculate_albedo_tall_veg_adj` | [10](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_albedo.py#L10) | Tall veg + ag albedo tuzatishi (α_min=0.18) |
| 2 | `calculate_albedo_adj` | [69](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_albedo.py#L69) | $\Delta\alpha = \alpha' - \alpha$ |
| 3 | `calculate_surface_albedo` | [76](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_albedo.py#L76) | $\alpha = \sum w_b\rho_b$ (Tasumi) |

## `vegetation_indices.py` — Vegetatsiya indekslari

Batafsil: [02_albedo_ndvi_lai.md](02_albedo_ndvi_lai.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `calculate_ndvi` | [9](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/vegetation_indices.py#L9) | NDVI, clamp(−1,1) (mask emas!) |
| 2 | `calculate_ndwi` | [39](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/vegetation_indices.py#L39) | NDWI (swir1, green) |
| 3 | `calculate_lai` | [54](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/vegetation_indices.py#L54) | $LAI = \min(10\,NDVI^{3.5}, 6)$ |
| 4 | `calculate_percent_residue` | [72](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/vegetation_indices.py#L72) | Qoldiq % (Aggarwala 1991) |
| 5 | `calculate_tall_veg_id` | [96](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/vegetation_indices.py#L96) | O'rmon (41–43) + tall crops flagi |

## `snow_water_flag_calculation.py` — Qor/suv flagi

Batafsil: [02_albedo_ndvi_lai.md](02_albedo_ndvi_lai.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `calculate_snow_water_flag` | [11](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/snow_water_flag_calculation.py#L11) | 0 quruqlik / 1 qor / 2 suv |

## `surface_temperature.py` — LST va lapse

Batafsil: [03_surface_temperature.md](03_surface_temperature.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `calculate_lst_adj_multiplier` | [11](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L11) | $m = 2/(K_{c,cold}-K_{c,hot})$ |
| 2 | `calculate_lst_tall_veg_adj_low_albedo` | [22](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L22) | Tall-veg LST + low-albedo tuzatish |
| 3 | `calculate_lst_dem_tall_veg_adj_low_albedo` | [34](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L34) | Delapsed tall-veg LST + low-albedo (H uchun default) |
| 4 | `calculate_lst_dem_adj_low_albedo` | [47](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L47) | `ts_dem_latlon` + low-albedo (`ts_model=min_albedo`) |
| 5 | `calculate_lst_tall_veg_adj_low_albedo_general` | [61](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L61) | $T + \Delta\alpha\,m\,(T_{hot}-T_{cold})$ |
| 6 | `calculate_lst_dem_tall_vegetation` | [79](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L79) | Tall-veg LST + total lapse |
| 7 | `calculate_t_shade_offset` | [90](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L90) | $(T_{cold}-T_{wb})/k_{sh}$ |
| 8 | `calculate_t_sunlit_offset` | [98](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L98) | $(T_{hot}-T_{cold})/k_{sun}$ |
| 9 | `calculate_t_wet_bulb` | [105](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L105) | Ho'l termometr T (°C) $e_{wet}$ dan |
| 10 | `calculate_vapor_pressure_wet_bulb` | [116](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L116) | $e_{wet} = \sqrt{e_a e^\circ}$ |
| 11 | `calculate_lst_tall_vegetation` | [124](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L124) | Canopy unmixing (wrapper) |
| 12 | `calculate_lst_tall_vegetation_general` | [156](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L156) | Clumping, soya/quyosh ulushlari, $T_c$ |
| 13 | `calculate_lst_terrain` | [234](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L234) | Terrain LST (wrapper) |
| 14 | `calculate_lst_terrain_general` | [242](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L242) | $T - 10\cos\phi$ (aspect vs quyosh) |
| 15 | `calc_mountain_toggle` | [269](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L269) | $z_{max}-z_{min} > 1000$ m |
| 16 | `find_elev_for_lapse_rate_change` | [291](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L291) | Tik qiyaliklar (>10°) intervalMean(20,40) balandligi |
| 17 | `calculate_lapse_general` | [330](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L330) | Ikki qismli lapse (flat / mountain) |
| 18 | `calculate_std_lapse` | [389](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L389) | Standart lapse (wrapper) |
| 19 | `calculate_surface_temperature` | [406](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L406) | Legacy LST: ε_NB, R_c, Plank |
| 20 | `calculate_surface_temperature_dem` | [472](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/surface_temperature.py#L472) | $T_s + \Delta T_{std}$ |

## `weather.py` — Ob-havo

Batafsil: [04_weather_reference_et.md](04_weather_reference_et.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `weather_interpolation` | [15](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/weather.py#L15) | Overpass vaqtiga chiziqli vaqt interpolyatsiyasi (±12 soat) |
| 2 | `calculate_overpass_cfsv2_weather` | [84](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/weather.py#L84) | CFSv2 overpass ob-havo |
| 3 | `calculate_overpass_nldas_weather` | [123](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/weather.py#L123) | NLDAS overpass ob-havo |
| 4 | `calculate_overpass_global_weather` | [151](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/weather.py#L151) | NLDAS (+CFSv2 fallback) kompozit |
| 5 | `calculate_daily_weather_series_composite` | [215](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/weather.py#L215) | 10+1 kunlik seriya |
| 6 | `calculate_daily_weather_cimis` | [254](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/weather.py#L254) | Spatial CIMIS kunlik (−300 sentinel) |
| 7 | `calculate_daily_weather_gridmet` | [328](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/weather.py#L328) | gridMET kunlik |
| 8 | `calculate_daily_weather_cfsv2` | [360](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/weather.py#L360) | CFSv2 kunlik (quyosh kuni bo'yicha) |
| 9 | `calculate_daily_weather_composite` | [436](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/weather.py#L436) | CIMIS → gridMET → CFSv2 kompozit + ETr(×0.85)/ETo |

## `asce_et_reference_products.py` — ASCE reference ET

Batafsil: [04_weather_reference_et.md](04_weather_reference_et.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `net_radiation_daily` | [14](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/asce_et_reference_products.py#L14) | ASCE kunlik $R_n$ (Eq. 15–18) |
| 2 | `rso_daily` | [53](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/asce_et_reference_products.py#L53) | $R_{so} = (0.75 + 2\cdot10^{-5}z)R_a$ |
| 3 | `ra_daily` | [72](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/asce_et_reference_products.py#L72) | Kunlik $R_a$ (Eq. 21–27) |
| 4 | `asce_hourly_et` | [127](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/asce_et_reference_products.py#L127) | ASCE soatlik PM (ETr/ETo) |
| 5 | `asce_daily_et` | [378](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/asce_et_reference_products.py#L378) | ASCE kunlik PM (ETr/ETo) |
| 6 | `instant_refet` | [509](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/asce_et_reference_products.py#L509) | Overpass soatlik ETr/ETo (clear-sky Rs) |

## `common_products.py` — Umumiy mahsulotlar

Batafsil: [05_common_products.md](05_common_products.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `get_solar_day_start_end` | [17](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L17) | Quyosh kuni boshi/oxiri (UTC) |
| 2 | `calculate_solar_time_difference` | [64](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L64) | $12\lambda/\pi + S_c$ |
| 3 | `calculate_solar_time` | [78](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L78) | UTC → quyosh vaqti |
| 4 | `calculate_scene_solar_day_start_end` | [86](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L86) | Sahna centroid bo'yicha quyosh kuni |
| 5 | `calculate_cos_theta_flat` | [100](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L100) | $\cos\theta_{hor}$ |
| 6 | `calculate_cos_theta_flat_daily` | [140](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L140) | Kunlik o'rtacha $\cos\theta$ |
| 7 | `calculate_cos_theta_mountain` | [151](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L151) | Qiyalikdagi $\cos\theta$ / cos(s), min 0.1 |
| 8 | `calculate_ea` | [188](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L188) | $e_a = Pq/(0.622+0.378q)$ |
| 9 | `calculate_datum` | [215](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L215) | Sahna o'rtacha balandligi (int) |
| 10 | `calculate_dem` | [241](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L241) | SRTM → GMTED → GTOPO tanlash, 20 km bufer |
| 11 | `calculate_slope` | [292](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L292) | `ee.Terrain.slope` (gradus) |
| 12 | `calculate_aspect` | [303](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L303) | `ee.Terrain.aspect` |
| 13 | `calculate_doy` | [313](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L313) | Yil kuni (1..366) |
| 14 | `merge_nlcd_crop_type_layers` | [330](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L330) | NLCD + CDL birlashtirish, tall crops / grapes flaglari |
| 15 | `calculate_land_use_usa` | [485](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L485) | Annual NLCD + crop type (USA) |
| 16 | `calculate_land_use_usa_mode` | [517](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L517) | NLCD 120 m mode |
| 17 | `calculate_land_use_global` | [551](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L551) | ESA WorldCover → NLCD |
| 18 | `calculate_land_use_combined` | [567](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L567) | Arktika (MODIS) + ESA + USA ierarxiyasi |
| 19 | `calculate_land_use_combined_mode` | [604](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L604) | Xuddi shu, USA qismi 120 m mode |
| 20 | `get_qa_bits` | [641](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L641) | Bit maska ajratish |
| 21 | `landsat_fmask` | [654](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L654) | C1 BQA cloud/shadow (legacy) |
| 22 | `calculate_cloud_mask` | [666](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L666) | simpleCloudScore + BQA, 5 px bufer (pixel selection uchun) |
| 23 | `calculate_u200` | [730](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L730) | $u_{200}$ log profil, sahna o'rtachasi |
| 24 | `calculate_u200_adj` | [768](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L768) | Tog' shamoli: cho'qqi kuchaytirish + leeward kamaytirish |
| 25 | `calculate_relative_humidity` | [834](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L834) | RH = e_a/e°(T_s) |
| 26 | `calculate_air_pressure` | [865](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L865) | $P(z)$ FAO-56 |
| 27 | `filter_std_elev_product` | [885](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L885) | OpenET σ_z asset |
| 28 | `filter_rel_elev_product` | [891](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L891) | OpenET RE asset |
| 29 | `calculate_elevation_std` | [897](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L897) | σ_z (1500 m doira) |
| 30 | `calculate_relative_elevation` | [906](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L906) | RE (1500 m doira) |
| 31 | `calculate_wind_aspect` | [923](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L923) | Shamol yo'nalishi atan2(−v,−u) |
| 32 | `calculate_broad_band_emissivity` | [940](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L940) | $\varepsilon_0 = 0.95 + 0.01LAI$ |
| 33 | `calculate_quality_mask` | [966](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L966) | cloud ∨ ETrF>1.3 maskasi |
| 34 | `calculate_soil_wilting_point` | [979](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L979) | θ_WP (STATSGO + global) |
| 35 | `calculate_soil_field_capacity` | [995](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/common_products.py#L995) | θ_FC (STATSGO + global) |

## `net_radiation.py` — Net radiation

Batafsil: [06_net_radiation.md](06_net_radiation.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `radiation_adjustment_coefficient` | [15](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L15) | $C_{rad}$ wrapper |
| 2 | `radiation_adjustment_coefficient_general` | [24](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L24) | $C_{rad} = \frac{R_{so,i}^f}{R_{so,i}}\frac{R_{so,24}}{R_{so,24}^f}\le1.5$ |
| 3 | `calculate_daily_extraterr_radiation` | [41](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L41) | Qiyalikda $R_{a,24}$ (48 yarim soat) |
| 4 | `calculate_instant_rso` | [126](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L126) | Tog'li instant $R_{so}$ (beam+diffuse+terrain) |
| 5 | `calculate_instant_rso_flat` | [170](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L170) | Tekis instant $R_{so}$ |
| 6 | `calculate_daily_rso` | [192](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L192) | Tog'li kunlik $R_{so}$ |
| 7 | `calculate_daily_rso_flat` | [247](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L247) | Tekis kunlik $R_{so}$ |
| 8 | `calculate_direct_transmissivity` | [285](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L285) | $\tau_B$ (Allen 2014 Eq. 18) |
| 9 | `calculate_diffuse_transmissivity` | [299](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L299) | $\tau_D$ (Eq. 19) |
| 10 | `calculate_rso_products` | [312](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L312) | Barcha Rso + C_rad (legacy) |
| 11 | `calculate_net_radiation_mountain` | [403](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L403) | Default $R_n$ (tog') |
| 12 | `calculate_net_radiation` | [475](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L475) | Flat $R_n$ → (RLin, RLout, Rn) |
| 13 | `calculate_radiation_lw_incoming_flat` | [547](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L547) | $R_{L\downarrow}$ flat |
| 14 | `calculate_radiation_lw_incoming_mountain` | [559](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L559) | $R_{L\downarrow}$ tog' |
| 15 | `calculate_radiation_lw_outgoing` | [585](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/net_radiation.py#L585) | $R_{L\uparrow}=\varepsilon\sigma T^4$ |

## `soil_heat_flux.py` — Soil heat flux

Batafsil: [07_soil_heat_flux.md](07_soil_heat_flux.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `calculate_soil_heat_flux` | [14](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/soil_heat_flux.py#L14) | Default G (tog', 1.5cos s muzlagan) |
| 2 | `calculate_soil_heat_flux_flat` | [200](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/soil_heat_flux.py#L200) | Flat G |

## `momentum_roughness.py` — Zom

Batafsil: [08_momentum_roughness.md](08_momentum_roughness.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `calculate_zom_adj_general` | [11](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/momentum_roughness.py#L11) | Zom: qor, albedo, relyef σ_z tuzatishi |
| 2 | `calculate_zom_adj` | [39](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/momentum_roughness.py#L39) | Wrapper (czom_adj=0.5) |
| 3 | `calculate_zom` | [54](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/momentum_roughness.py#L54) | Lookup + LAI (ekin) + Perrier (daraxt) + 5×5 silliqlash |
| 4 | `calculate_zom_with_water` | [138](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/momentum_roughness.py#L138) | Suv uchun Zom(u200) |
| 5 | `calculate_extra_aerodynamic_resistance` | [159](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/momentum_roughness.py#L159) | $r_{extra}$ (amalda 0 — bug) |

## `gridded_dT.py` — dT kalibratsiyasi

Batafsil: [09_sensible_heat_flux.md](09_sensible_heat_flux.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `psi_momentum_traditional` | [11](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/gridded_dT.py#L11) | ψ_m (Paulson) — ishlatilmaydi |
| 2 | `psi_momentum_new` | [30](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/gridded_dT.py#L30) | ψ_m (tezkor variant) — ishlatilmaydi |
| 3 | `psi_momentum_piecewise` | [49](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/gridded_dT.py#L49) | ψ_m bo'lakli — ishlatilmaydi |
| 4 | `psi_heat_traditional` | [77](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/gridded_dT.py#L77) | ψ_h (Paulson) — ishlatilmaydi |
| 5 | `psi_heat_new` | [92](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/gridded_dT.py#L92) | ψ_h (tezkor) — ishlatilmaydi |
| 6 | `calculate_gridded_dt` | [111](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/gridded_dT.py#L111) | Hot/cold → a, b (11 iteratsiya); amalda 1 blok |

## `sensible_heat_flux.py` — Sensible heat flux

Batafsil: [09_sensible_heat_flux.md](09_sensible_heat_flux.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `calculate_sensible_heat_flux` | [15](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/sensible_heat_flux.py#L15) | Default H (tog', 9 iteratsiya) + E_aero suv |
| 2 | `calculate_sensible_heat_flux_flat` | [405](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/sensible_heat_flux.py#L405) | Flat H |

## `automated_pixel_selection.py` — Hot/cold tanlash

Batafsil: [10_pixel_selection.md](10_pixel_selection.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `lazy_property` | [22](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L22) | Lazy property dekoratori |
| 2 | `PixelSelection.__init__` | [45](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L45) | model, land_use_mode, mesh, min_pix=20 |
| 3 | `PixelSelection.select_method` | [54](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L54) | dynamic/static dispetcher |
| 4 | `PixelSelection.preset_ratings` | [62](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L62) | LU va slope reytinglari |
| 5 | `PixelSelection.ndvi_percentile_weights` | [103](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L103) | NDVI persentil og'irliklari |
| 6 | `PixelSelection.alfalfa_albedo` | [135](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L135) | $\alpha_{alf}(\beta)$ |
| 7 | `PixelSelection.hot_cold_ag_blocks` | [151](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L151) | `hot_cold_LU_mask` natijasi |
| 8 | `PixelSelection.has_sufficient_hot_ag_pix` | [162](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L162) | Hot Ag ≥ 20 |
| 9 | `PixelSelection.has_sufficient_cold_ag_pix` | [176](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L176) | Cold Ag ≥ 20 |
| 10 | `PixelSelection.landcheck_cold` | [190](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L190) | Cold LU maska (bug: neq.Or) |
| 11 | `PixelSelection.landcheck_hot` | [203](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L203) | Hot LU maska (bug: neq.Or) |
| 12 | `PixelSelection.has_spatially_lapsed_temperature` | [216](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L216) | regress_success |
| 13 | `PixelSelection.filter_mesh_for_` | [223](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L223) | Bo'sh stub |
| 14 | `PixelSelection.select_pixels` | [227](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L227) | Bo'sh stub |
| 15 | `PixelSelection.calibration_rating` | [231](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L231) | Sifat Q ∈ [0,1] |
| 16 | `create_mesh` | [266](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L266) | 16×16 = 256 blok |
| 17 | `create_mesh_static` | [333](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L333) | 4×4 = 16 blok |
| 18 | `rational_function` | [382](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L382) | $1/\vert x-x_0\vert $ |
| 19 | `detectEdges` | [397](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L397) | $\vert \sigma_{3\times3}(NDVI) - 1\vert $ |
| 20 | `set_cold_ndvi_mask_ranges` | [414](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L414) | Cold NDVI oynasi (top95–100, adaptiv) |
| 21 | `assign_cold_reducer_weights` | [474](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L474) | Cold edge reyting va T og'irligi |
| 22 | `count_filter_min_cold_blocks` | [516](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L516) | Bloklarni count ≥ mean/4 yoki ≥100 |
| 23 | `weight_ideal_cold_temps` | [564](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L564) | Count bo'yicha p5/p10 og'irlash |
| 24 | `create_aoi_around_top_cold_block` | [599](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L599) | Ishlatilmaydi (TODO delete) |
| 25 | `calc_new_cold_alb_target` | [644](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L644) | Cold albedo target va reyting |
| 26 | `calc_new_cold_ndvi_target` | [702](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L702) | Cold NDVI target va reyting |
| 27 | `get_ideal_cold_temperature` | [739](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L739) | Ideal cold T + cold reyting |
| 28 | `set_hot_ndvi_mask_ranges` | [923](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L923) | Hot NDVI oynasi (bot2–10, adaptiv) |
| 29 | `assign_hot_reducer_weights` | [1001](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1001) | Hot edge, OM, slope, LU og'irliklari |
| 30 | `count_filter_min_hot_blocks` | [1075](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1075) | Hot bloklar filtri |
| 31 | `weight_ideal_hot_temps` | [1126](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1126) | Count bo'yicha p85–p99 og'irlash |
| 32 | `calc_new_hot_alb_target` | [1167](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1167) | Hot albedo target (~0.20) va reyting |
| 33 | `get_ideal_hot_temperature` | [1266](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1266) | Ideal hot T + hot reyting (bug: slope_mask) |
| 34 | `get_temperature_rating` | [1456](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1456) | $10\sqrt{\mathrm{clamp}(0.2/\vert T-T^*\vert )}$ |
| 35 | `get_temperature_rating_static` | [1477](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1477) | Static versiya (weight=1) |
| 36 | `get_soil_moisture_rating` | [1498](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1498) | P/ETr reytingi — ishlatilmaydi, argument xatosi |
| 37 | `prepareRatingParams` | [1525](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1525) | Static reyting bandlari |
| 38 | `calculate_hot_rating` | [1620](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1620) | Static hot reyting |
| 39 | `calculate_cold_rating` | [1660](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1660) | Static cold reyting |
| 40 | `generateRatingsStatic` | [1700](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1700) | Static reytinglar orkestratori |
| 41 | `calculate_kc` | [1767](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1767) | $K_c = f_c + (1-f_c)K_e$ |
| 42 | `get_pixels_for_blocks` | [1784](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1784) | Blokdagi max reytingli piksel (legacy) |
| 43 | `calculate_hot_pixel_etrf` | [1827](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1827) | $K_{c,hot} = f_c$ (dynamic) |
| 44 | `calculate_hot_pixel_etrf_static` | [1857](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1857) | $f_c + (1-f_c)K_e$ (nam sahna) |
| 45 | `calculate_cold_pixel_etrf` | [1888](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1888) | $\mathrm{clamp}((NDVI-0.15)/0.65, 0.11, 1)$ |
| 46 | `get_max_rated_pixels` | [1896](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1896) | AOI dan global max reytingli piksel |
| 47 | `calc_mesh_all` | [1949](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1949) | Mesh flag (hot+cold) — ishlatilmaydi |
| 48 | `calc_mesh_cold` | [1987](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L1987) | Cold mesh filtri |
| 49 | `calc_mesh_hot` | [2025](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L2025) | Hot mesh filtri |
| 50 | `hot_cold_LU_mask` | [2064](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L2064) | Ag piksellar sanog'i va bloklar |
| 51 | `calculate_top_bot_ndvi` | [2183](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L2183) | Og'irlangan NDVI persentillari |
| 52 | `get_ideal_temperatures` | [2247](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L2247) | Static: top reyting → T persentili |
| 53 | `select_pixels_static_ratings` | [2276](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L2276) | Static tanlash |
| 54 | `adjust_cold_temp_rating` | [2398](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L2398) | O'chirilgan (testlash kerak) |
| 55 | `select_pixels_dynamic_ratings` | [2425](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L2425) | Dynamic tanlash (default) |
| 56 | `extract_calibration_params` | [2550](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L2550) | Hot/cold nuqtada lai, Ts, Ts_dem, z, kc |
| 57 | `calibration_parameters_for_export` | [2590](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L2590) | Eksport uchun qo'shimcha (Rn, G, H, ...) |
| 58 | `etrf_stats_calculation` | [2644](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/automated_pixel_selection.py#L2644) | Ag ETrF statistikasi (o'chirilgan) |

## `lapsed_surface_regions.py` — Spatial delapsing

Batafsil: [11_lapsed_surface_regions.md](11_lapsed_surface_regions.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `count_filter_blocks` | [12](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/lapsed_surface_regions.py#L12) | Full cover Ag/o'rmon bloklar sanog'i |
| 2 | `filter_ag_or_forest_blocks` | [75](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/lapsed_surface_regions.py#L75) | Ag yetarli → o'rmonni chiqarish |
| 3 | `get_full_cover_temperatures` | [128](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/lapsed_surface_regions.py#L128) | Bloklarda full cover $T_{s,dem}$ p10/p50 |
| 4 | `filter_ag_blocks` | [221](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/lapsed_surface_regions.py#L221) | Outlier bloklarni filtrlash |
| 5 | `set_fallback_datum_block` | [272](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/lapsed_surface_regions.py#L272) | Blok yo'q → butun sahna |
| 6 | `find_datum_block` | [297](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/lapsed_surface_regions.py#L297) | Datum blok (sort bug) |
| 7 | `calculate_ag_areas_and_full_cover_distances` | [316](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/lapsed_surface_regions.py#L316) | Masofa va balandlik statistikasi (UTM) |
| 8 | `calc_regression_checks` | [356](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/lapsed_surface_regions.py#L356) | 4 ta sifat tekshiruvi |
| 9 | `calculate_lapsed_surface_min_max` | [443](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/lapsed_surface_regions.py#L443) | Sirt min/max (water_mask) |
| 10 | `calculate_lapsed_surface` | [469](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/lapsed_surface_regions.py#L469) | Asosiy: regressiya + 8 tekshiruv |
| 11 | `set_spatial_regress_coeffs` | [726](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/lapsed_surface_regions.py#L726) | Eksport xususiyatlari |

## `etrf_et24.py` — ETrF va ET24

Batafsil: [12_etrf_et24_soil_water_balance.md](12_etrf_et24_soil_water_balance.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `calculate_et_instant` | [14](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/etrf_et24.py#L14) | $3600(R_n-G-H)/\lambda$ |
| 2 | `calculate_etrf` | [36](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/etrf_et24.py#L36) | $ET_{inst}/ET_{r,inst}^{cold}$ |
| 3 | `calculate_evaporative_fraction` | [66](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/etrf_et24.py#L66) | EF = LE/(Rn−G) |
| 4 | `daylight_hours` | [77](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/etrf_et24.py#L77) | N (soat) |
| 5 | `calculate_rn_slob` | [95](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/etrf_et24.py#L95) | Slob kunlik $R_n$ |
| 6 | `calculate_et_ef` | [233](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/etrf_et24.py#L233) | EF asosidagi ET24 + stress |
| 7 | `evap_aerodynamic` | [291](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/etrf_et24.py#L291) | Suv/qor kunlik aerodinamik E |
| 8 | `calculate_etrf_et24` | [418](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/etrf_et24.py#L418) | Yakuniy ETrF24 va ET24 |

## `soil_water_balance.py` — Soil water balance

Batafsil: [12_etrf_et24_soil_water_balance.md](12_etrf_et24_soil_water_balance.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `daily_precip_etr` | [13](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/soil_water_balance.py#L13) | P, ETr, P_next seriyasi (Join) |
| 2 | `calculate_soil_water_balance` | [66](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/soil_water_balance.py#L66) | FAO-56 + skin layer → $K_e$ |

## `stretch.py` — Manual stretch

Batafsil: [12_etrf_et24_soil_water_balance.md](12_etrf_et24_soil_water_balance.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `eeflux_manual` | [22](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/stretch.py#L22) | $ETrF + Adj_L(1-ETrF) + Adj_H ETrF$ |
| 2 | `eta_stretched` | [44](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/stretch.py#L44) | $ETrF'\cdot ET_{r,24}$ |
| 3 | `etof_stretched` | [56](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/stretch.py#L56) | $ET_a'/ET_{o,24}$ |

## `collection.py` — Collection

Batafsil: [13_collection_interpolation.md](13_collection_interpolation.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `lazy_property` | [18](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/collection.py#L18) | Lazy property dekoratori |
| 2 | `Collection.__init__` | [36](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/collection.py#L36) | Validatsiya, sputnik sana filtrlari |
| 3 | `Collection._build` | [209](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/collection.py#L209) | Kolleksiya filtrlash + model map |
| 4 | `Collection.overpass` | [312](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/collection.py#L312) | Sahna-darajasidagi natijalar |
| 5 | `Collection.interpolate` | [340](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/collection.py#L340) | Kunlik/oylik/yillik/custom interpolyatsiya |
| 6 | `Collection.get_image_ids` | [708](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/collection.py#L708) | Tasvir ID lar ro'yxati |

## `interpolate.py` — Interpolyatsiya

Batafsil: [13_collection_interpolation.md](13_collection_interpolation.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `from_scene_et_fraction` | [14](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/interpolate.py#L14) | Tayyor ETf sahnalaridan interpolyatsiya |

## `openet_utils.py` — Utilitalar

Batafsil: [00_arxitektura.md](00_arxitektura.md)

| # | Funksiya | Qator | Vazifa / formula |
|---|---|---|---|
| 1 | `getinfo` | [9](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/openet_utils.py#L9) | Exponential back-off `getInfo` |
| 2 | `constant_image_value` | [33](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/openet_utils.py#L33) | Konstant tasvir qiymati (test) |
| 3 | `point_image_value` | [40](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/openet_utils.py#L40) | Nuqtadagi qiymat (test) |
| 4 | `point_coll_value` | [47](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/openet_utils.py#L47) | Nuqtada kolleksiya → dict |
| 5 | `date_0utc` | [67](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/openet_utils.py#L67) | 0 UTC sana |
| 6 | `is_number` | [82](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/openet_utils.py#L82) | Son tekshiruvi |
| 7 | `millis` | [90](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/openet_utils.py#L90) | datetime → ms |
| 8 | `valid_date` | [105](https://github.com/Open-ET/openet-eemetric/blob/7c83a7d058b2a0cd37cc4bc251762f9b7150d4d7/openet/eemetric/openet_utils.py#L105) | Sana formati tekshiruvi |

