# 09 — Kod kuzatuvlari (pymetric, WSWUP)

> Statik tahlil asosida. Kod ishga tushirilmagan: GDAL, `drigo` va Collection 1 ma'lumotlari yo'q edi. Qator raqamlari — `c3a47fb` commit (yuklangan zip bilan bir xil).

## 1. Potensial buglar

| # | Joy | Kod | Muammo | Ta'sir |
|---|---|---|---|---|
| 1 | `support/et_numpy.py:31, 57` | `et_common.solar_time_rad_func(time, lon, sc)` | Signatura `(lon, time, sc)`: $t_{solar} = time + lon\cdot24/2\pi + S_c - 12$. Argumentlar almashgani uchun soat ×3.82, uzunlik esa ko'paytirilmaydi | `cos_theta_model = SPATIAL / MOUNTAIN` da cos θ **noto'g'ri**. Default `CENTROID` to'g'ri (`et_common.py:1015`) |
| 2 | `metric_functions/metric_model2_func.py:1024, 1027` | `g_array = et_numpy.g_sebal_func(ts, albedo, ndvi)` | Funksiya $G/R_n$ **nisbat**ini qaytaradi va $T_s$ ni Kelvinda oladi. SEBAL formulasida $T_s$ °C da va natija $\times R_n$ bo'lishi kerak | `g_model_type = SEBAL` da G noto'g'ri: masalan $T_s$ = 300 K, α = 0.2, NDVI = 0.5 → funksiya ≈ 1.6 qaytaradi va u **1.6 W/m²** sifatida ishlatiladi (to'g'ri qiymat ≈ $0.14R_n$ ≈ 80 W/m²) |
| 3 | 37 joy (masalan `metric_model1_func.py:647`) | `np.bool`, `np.int`, `np.float` | NumPy ≥ 1.24 da olib tashlangan | `AttributeError` — **zamonaviy muhitda ishlamaydi** |
| 4 | `interp_functions/interpolate_tables_func.py:987` | `DataFrame.append(...)` | pandas ≥ 2.0 da olib tashlangan | `--tables` rejimi xato beradi |
| 5 | `metric_functions/monte_carlo_func.py:188, 194` | `eval('{' + kc_cold_doy_dict + '}')` | INI satri Python kodi sifatida bajariladi | Ishonchsiz INI → ixtiyoriy kod bajarilishi (xavfsizlik). `ast.literal_eval` xavfsizroq |
| 6 | `interp_functions/interpolate_rasters_func.py:1786–1793` | `ke_array = ...; del ke_array` | SWB ($K_e$) hisoblanadi, lekin ETrF ga **qo'llanmaydi** | `swb_adjust_flag = True` faqat vaqt sarflaydi |
| 7 | `metric_functions/metric_model2_func.py:91–95` | `Ts_correction_flag`, `K_value`, `dense_veg_min_albedo` | O'qiladi, hech qayerda ishlatilmaydi | "Recently added" tuzatish hali ulanmagan |
| 8 | `support/et_image.py:555` | `math.sin(2 * b)`, `b` gradusda | `math.sin` radian kutadi | `convert_solar_time` noto'g'ri EOT beradi (hozircha chaqirilmaydi) |
| 9 | `metric_functions/metric_model1_func.py:781, 784` | `if save_dict['ndwi_toa']:` hisoblash, `if calc_dict[...]:` saqlash | Shartlar almashgan | `save_ndwi_toa=False`, `calc=True` bo'lsa `NameError`; NDWI pixel rating uchun kerak |
| 10 | `metric_functions/metric_model2_func.py:1002, 1394` | `ts_lapsed_func(ts_array[0], elev, datum)` | Cold pikselning **delapse qilinmagan** $T_s$ i datumdan lapse qilinadi. To'g'risi $T_{s,dem}^{cold}$ dan boshlash | $R_{L\downarrow}$ da $\Gamma(z_{cold} - z_d)/1000$ siljish (cold piksel datumga yaqin bo'lsa kichik) |
| 11 | `metric_functions/metric_model2_func.py:1495–1496` | `ts_array < mean(ts_dem_point_array)` | Delapse qilinmagan $T_s$ delapse qilingan $T_{s,dem}$ o'rtachasi bilan solishtiriladi | Tog'li sahnada suv G maskasi siljiydi |
| 12 | `metric_functions/metric_model2_func.py:1429` | `rn_24_func(rs_in=rs_in_array)` | Slob formulasiga kunlik emas, **instant** $R_{s\downarrow}$ beriladi | `rn_24` rasteri noto'g'ri (ET24 da ishlatilmaydi) |
| 13 | `metric_functions/pixel_rating_func.py` (Ts bin tsikli) | `(ts > P_i) & (ts <= P_{i+1})` | $T_s = P_0$ (eng sovuq) piksel hech qaysi binga tushmaydi → cold **va** hot reytingi 1 qoladi | Eng sovuq piksel hot nomzod sifatida ham yuqori ball oladi |
| 14 | `metric_functions/pixel_rating_func.py:150` | `"Using default ts_bins_count = 4"` | Kod 10 o'rnatadi | Log xabari noto'g'ri |
| 15 | `metric_functions/monte_carlo_func.py:124–125` | `swb_spinup_days=5`, `swb_min_spinup_days=30` | Min > umumiy | INI berilmasa SWB spin-up mantiqsiz |
| 16 | `metric_functions/metric_model2_func.py` (~401, 409) | `'...' + '...{}'.format(x)` | `.format` faqat ikkinchi satrga qo'llanadi | Xato xabarida qiymat ko'rinmaydi |

## 2. Eskirgan qismlar (2026 holatiga ko'ra)

| Masala | Holat | Yechim |
|---|---|---|
| **Landsat Collection 1** | USGS C1 ni 2022–2023 da tarqatishdan to'xtatgan. `et_image` faqat C1 nomlarini va L4–L8 ni taniydi (`prefix_list`, :59) | C2 L1 uchun: regex, MTL kalitlari (`REFLECTANCE_MULT_BAND_*`, `QA_PIXEL` bitlari), L9 (`LC09`) qo'shish |
| **C1 BQA** | `bqa_fmask_func` C1 bit tartibi | C2 `QA_PIXEL`: bit 3 cloud, 4 shadow, 5 snow, 8–9 cloud conf. |
| **NumPy / pandas API** | #3, #4 | `np.bool → bool`, `DataFrame.append → pd.concat` |
| `future==0.16.0` | Python 2 moslik paketi | Olib tashlash |
| `download_nlcd.py` | faqat 2006/2011 | Annual NLCD |
| `python3` branch (2023) | NLDAS/gridMET tools tuzatishlari | `master` dan yangiroq ([WSWUP/pymetric `python3`](https://github.com/WSWUP/pymetric/tree/python3)) |

## 3. Dizayn xususiyatlari (bug emas)

| Mavzu | Tafsilot |
|---|---|
| **Yarim avtomatik** | Rasmiy oqimda hot/cold ArcGIS'da qo'lda tuzatiladi; Monte Carlo — muqobil |
| **Sahna-konstanta ob-havo** | $u$, $e_a$ (tau dan tashqari), $ET_r$, $ET_{r,24}$ — cold nuqtadagi qiymat |
| **TOA asosidagi indekslar** | LAI, emissivity, G va Zom default **TOA** NDVI/SAVI dan |
| **Paulson ψ, damping yo'q** | Kalibratsiya: 20/100 iteratsiya; raster: 6 |
| **Clamp yo'q** | ETrF manfiy / >1.3 bo'lishi mumkin; cheklash interpolyatsiyada |
| **Qiyalik** | `MOUNTAIN` cos θ dan tashqari tog' tuzatishlari (H, Rso, shamol) yo'q |
| **Funksional arxitektura** | `et_numpy` sof funksiyalar — test va qayta ishlatish uchun qulay |

## 4. CRS / NoData xulosasi

| Bosqich | CRS | NoData |
|---|---|---|
| Sahna (Model 1/2) | EPSG:326xx (MTL UTM_ZONE), 30 m, snap (15, 15) | `common_area ∧ fmask` → NaN; `.img` NoData |
| Tashqi rasterlar | `drigo.raster_to_array(mask_extent)` bilan sahna gridiga | DEM `-9999` → NaN |
| Kalibratsiya nuqtalari | shapefile, sahna UTM | nuqta NaN bo'lsa → xato |
| Interpolyatsiya | `study_area_proj` + `cellsize` + `snap` | `count < 2` → NaN; chekkalar konstanta |
| ETr/PPT | bilinear qayta proyeksiya | `etr_mask`, `ppt_mask` |

## 5. 🇺🇿 Ishga tushirish uchun minimal tavsiyalar

1. Python 3.8–3.10 + NumPy < 1.24 + pandas < 2.0 + GDAL 3.x (conda) — yoki #3, #4 ni tuzatish.
2. Landsat C2 L1 → `et_image` ni moslashtirish (yoki C2 dan C1-uslubidagi papka strukturasini yasash).
3. `weather_data_source = MANUAL` bilan bitta sahnada sinov: `ea` (kPa), `wind_speed` (m/s, 2 m), `etr` (mm/h), `etr_24hr` (mm/d) — ERA5-Land dan.
4. Land cover — NLCD kodlariga remap (ESA WorldCover: 40 → 82, 10 → 43, 80 → 11, ...), `zom_remap` JSON ni mahalliy qiymatlarga moslash.
5. `cos_theta_model = CENTROID` qoldiring (#1 tufayli).
6. `datum` — sahna o'rtacha balandligi (masalan Farg'ona vodiysi ~450 m); `lapse_rate = 6.5`.
7. Kalibratsiya nuqtalarini qo'lda tekshiring: $\Delta T > 4$ K, cold — to'liq qoplangan paxta yoki beda, hot — shudgor.
