# 06 — Kod kuzatuvlari (pyMETRIC, Nieto)

> Statik tahlil asosida. Model to'liq ishga tushirilmagan (GDAL va pyTSEB o'rnatilmagan). #2 formulalarni qayta yozib, raqamli tekshirildi. #9 zip ichidagi namunaviy natijadan olindi.

## 1. Potensial buglar

| # | Joy | Kod | Muammo | Ta'sir |
|---|---|---|---|---|
| 1 | `METRIC.py:245, 299` | `if use_METRIC_resistance is True:` | Config'dan `int(1)` keladi, `1 is True` → **False**. Shu sababli config orqali doim Kustas–Norman rejimi tanlanadi | `use_METRIC_resistance` sozlamasi amalda ishlamaydi |
| 1b | `METRIC.py:299–312` | `R_A[i], _, _ = tseb.calc_resistances(...)` faqat `else` ichida | To'g'ridan-to'g'ri `METRIC(..., use_METRIC_resistance=True)` chaqirilsa, pikselli $R_A$ hech qachon hisoblanmaydi (NaN qoladi), `R_A_params` esa (2,) shaklida → H, LE = **NaN** | API'dan foydalanganda butun chiqish NaN |
| 2 | `METRIC.py:478, 546` | `Rn = Sn + Ln` (`calc_Ln` musbat) | Ishora xatosi: $R_n = S_n - L_n$ bo'lishi kerak. Bundan tashqari `pet_asce` maxrajida $\gamma\cdot1$ yo'q, aerodinamik hadning birligi ham mos emas | Namunada $LE_{ref}$ +27% → $LE_{cold}$, `fETr` ([04](04_reference_et.md#51-farqlar-statik-tahlil--raqamli-tekshiruv)) |
| 3 | `PyMETRIC.py:216` | `geo[0]+subset[0]*geo[1]` | `geo` aniqlanmagan (`self.geo` bo'lishi kerak) | `subset` berilsa `NameError` (try ichida — "Error reading LST file" deb chiqadi) |
| 4 | `PyMETRIC.py:82–83` | `if "G_short" not in ...: parameters["G_tall"] = 0.10` | `G_short` o'rniga `G_tall` ustiga yoziladi | `G_short` berilmasa `G_tall` = 0.10 bo'lib qoladi, `G_short` esa umuman bo'lmaydi |
| 5 | `PyMETRIC.py:445` | `self._get_subset(..., prj, geo)` | `prj`, `geo` aniqlanmagan | `subset_output` berilsa `NameError` |
| 6 | `endmember_search.py:93–94, 121–122` | `lst_index = lst_array <= lst_low` | NDVI maskasi bilan kesishtirilmagan | Cold/hot kandidatlar orasiga NDVI sharti bajarilmagan piksellar kirishi mumkin |
| 7 | `endmember_search.py:23` | `np.nanpercentile(vi_array, 0.05)` | 5% emas, **0.05%** | MINMAX: cold ≈ tasvirdagi global min LST (suv, bulut chekkasi) |
| 8 | `Config_LocalImage.txt` | `ETrF_bare=0` | Kod `self.p['ET_bare_soil']` ni o'qiydi | `ETrF_bare` e'tiborga olinmaydi |
| 9 | `Output/test_image.tif` | zip ichidagi namuna | $H$: o'rtacha 690, maks 4020 W/m²; $LE$: o'rtacha −198, min −3670 W/m² | Fizik jihatdan noreal. Ancillary faylda 7 band bor, joriy kod 9 band yozadi → namuna **boshqa versiya** bilan yaratilgan bo'lishi mumkin |
| 10 | `PyMETRIC.py:607` | `SEARCH_ORDER` | GRASS, CROP_MOSAIC, BARREN, WETLAND ikkala guruhda | Short guruh natijalari tall natijalarni ustidan yozadi ([03](03_endmember_search.md#2-landcover-guruhlari-igbp-pytseb-kodlari)) |
| 11 | `endmember_search.py:107, 134` | `np.nanmin(cv[...])` bo'sh massivda | Kandidat yo'q bo'lsa `ValueError` / `IndexError` | `None` qaytmaydi → dastur to'xtaydi |
| 12 | `PyMETRIC.py:568` | `emiss = VI*emis_C + (1-VI)*emis_S` | VI ∉ [0, 1] bo'lsa ε fizik chegaradan chiqadi | Xom NDVI (manfiy) bilan xato |

## 2. Dizayn xususiyatlari (bug emas)

| Mavzu | Tafsilot |
|---|---|
| **Instant model** | Kunlik ET ($ET_{24}$) yo'q. Chiqish: W/m² va `fETr = LE/LE_ref` |
| **Mahalliy shamol** | $u_*$ o'lchangan $u(z_u)$ dan hisoblanadi, 200 m blending height ishlatilmaydi |
| **Datum = dengiz sathi** | $T + \Gamma_w z$ (namli adiabatik) |
| **dT chizig'i** | Bitta, butun aoi uchun |
| **Brutsaert stabillik funksiyalari** | Paulson emas; L virtual H bilan |
| **Albedo — chiqish** | Campbell modelidan, kirim emas |
| **IGBP landcover** | NLCD emas. ESA WorldCover yoki MODIS MCD12Q1 dan IGBP ga o'tkazish kerak |
| **Barcha rasterlar bir gridda** | Qayta proyeksiya yo'q |

## 3. 🇺🇿 Ishlatish bo'yicha amaliy eslatmalar

| Masala | Tavsiya |
|---|---|
| `stdlon`, `time` | O'zbekiston: `stdlon=75`, `time` = UTC + 5 (Landsat `SCENE_CENTER_TIME` dan) |
| `ea`, `p` | **mb**. ERA5 dewpoint'dan: $e_a = 6.112\exp(17.67T_d/(T_d + 243.5))$ |
| `T_R1` | Landsat C2 ST_B10 × 0.00341802 + 149 (K); NoData → NaN |
| `VI` | 0..1 ga normallashtirilgan (fc-shakli), aks holda ε va ETrF buziladi |
| `landcover` | IGBP: CROP=12, GRASS=10, BARREN=16, WATER=0, URBAN=13 |
| `endmember_search` | MINMAX (namuna) o'rniga **CIMEC (0)** yoki **ESA (1)** |
| CRS | Barcha kirimlarni bitta UTM gridga (masalan EPSG:32642, 30 m) `gdalwarp -tap` bilan keltiring |
| `use_METRIC_resistance` | Bug #1 tufayli config'da hech narsani o'zgartirmaydi |
