# Taqqoslash: eeMETRIC vs pyMETRIC (Nieto) vs pymetric (WSWUP)

> Bu bo'lim uchta implementatsiyani **yonma-yon** qo'yadi. Har bir modelning to'liq formulalari va belgilashlari o'z papkasida qoladi va bu yerga ko'chirilmaydi. Har bir qator manba hujjatga havola beradi. Raqamli jadvallar [`formulalar_taqqoslash.py`](formulalar_taqqoslash.py) bilan hisoblangan (faqat `numpy` kerak).

| Qisqa nom | Model | Papka |
|---|---|---|
| **EE** | OpenET eeMETRIC v0.21.0 | [`openet-eemetric/`](../openet-eemetric/README.md) |
| **NI** | pyMETRIC (Hector Nieto, IRTA) v1.0 | [`pymetric-nieto/`](../pymetric-nieto/README.md) |
| **WS** | pymetric (WSWUP / DRI) v0.2.3 | [`pymetric-wswup/`](../pymetric-wswup/README.md) |

---

## 1. Feynman tushuntirish: "Bitta retsept, uchta oshpaz"

Uchala model ham bir xil ilmiy retseptga (Allen et al., 2007) asoslanadi: $LE = R_n - G - H$, $H$ esa hot/cold piksellar bilan kalibrlangan $dT$ dan topiladi. Farq "oshxona"da:

- **EE** — sanoat oshxonasi. Google Earth Engine bulutida ishlaydi, hamma narsa avtomatik va global ma'lumotlarga ulangan (default sozlamalari esa AQSh uchun).
- **NI** — laboratoriya stoli. Siz tayyor ingredientlarni (rasterlarni) olib kelasiz, u fizikani toza va moslashuvchan qilib bajaradi, lekin kunlik ET bermaydi.
- **WS** — an'anaviy restoran. To'liq konveyer bor (yuklashdan oylik ET gacha), lekin "bosh oshpaz" (mutaxassis) hot/cold ni qo'lda tekshirishi kutiladi. Ingredientlar ham eskirgan (Landsat C1).

---

## 2. Umumiy taqqoslash

| Mezon | EE | NI | WS |
|---|---|---|---|
| Platforma | Google Earth Engine (server-side graf) | NumPy + GDAL, butun rasterni xotirada | NumPy + GDAL + `drigo`, bloklar bo'yicha |
| Kod hajmi | ~13 300 qator | ~2 100 qator (+ pyTSEB) | ~31 400 qator |
| Arxitektura | `EEFlux` klassi + lazy property | `PyMETRIC(PyTSEB)` + funksiyalar | CLI skriptlar + sof funksiyalar (`et_numpy`) |
| Kirish | Landsat **C2 L2** (SR + ST), L4–L9 | Tayyor rasterlar (LST, LAI, VI, landcover, DEM) | Landsat **C1 L1** DN + MTL, L4–L8 |
| Ob-havo | NLDAS / CFSv2 (instant), gridMET / CIMIS / CFSv2 (kunlik) | Konfiguratsiyada son yoki raster | NLDAS / gridMET / CIMIS / Daymet yoki MANUAL |
| Land cover | NLCD + CDL (AQSh), ESA WorldCover (global) | **IGBP** | NLCD |
| Hot/cold | Avtomatik (dynamic reyting, 16×16 blok) | Avtomatik: CIMEC / ESA / MINMAX | Reyting + **qo'lda** (ArcGIS) yoki Monte Carlo |
| Kunlik ET | ✅ ETrF × ETr24 (+ EF, aero suv) | ❌ (faqat instant LE, fETr) | ✅ ETrF × ETr24 |
| Vaqt interpolyatsiyasi | ✅ kunlik / oylik / yillik (EToF × ETo) | ❌ | ✅ kunlik / oylik / yillik (ETrF × ETr), linear / cubic |
| Chiqish | `ee.Image` (eksport) | GeoTIFF / VRT / NetCDF | ERDAS `.img`, CSV jadval |
| Litsenziya | AGPL-3.0 | GPL-3.0 | Apache-2.0 |
| Zamonaviy muhitda ishlashi | ✅ | ⚠️ pyTSEB versiyasiga bog'liq | ❌ NumPy ≥ 1.24, pandas ≥ 2.0 va C1 muammolari |

---

## 3. Preprocessing

| Bosqich | EE | NI | WS |
|---|---|---|---|
| Reflectance | C2 L2 SR ($2.75\cdot10^{-5}DN - 0.2$) ([EE 01](../openet-eemetric/docs/01_preprocessing_landsat.md)) | Kirim emas; spektral parametrlar (ρ, τ barg / tuproq) | TOA → **Tasumi SR** (narrowband τ, $C_1..C_5$, $C_b$) ([WS 01](../pymetric-wswup/docs/01_prep_landsat.md)) |
| Bulut | QA_PIXEL + despeckle + 7.5 px dilate | `input_mask` / landcover | C1 BQA Fmask + ixtiyoriy smooth / buffer + qo'lda shp |
| LST | C2 ST, **ASTER GED emissivity bilan qayta hisoblangan** | Tayyor `T_R1` | BT → $R_c$ ($R_p$, $\tau_{NB}$, $R_{sky}$) → $T_s$ (Allen 2007) |
| DEM | SRTM → GMTED → GTOPO (avtomatik) | `alt` raster | NED (AQSh) |
| CRS | EE native (UTM), chiqishda eksport CRS | `T_R1` CRS, **qayta proyeksiya yo'q** | MTL UTM (EPSG:326xx), 30 m, snap (15, 15) |

---

## 4. Yuza xususiyatlari

| Kattalik | EE | NI | WS |
|---|---|---|---|
| Albedo | $\sum w_b\rho_b$ (SR) | $1 - S_n/S_{dn}$ (Campbell 2 qatlam) | $\sum w_b\rho_b$ (Tasumi SR) |
| LAI | $\min(10NDVI^{3.5}, 6)$ | **kirim** | $\mathrm{clip}(11SAVI^3, 0, 6)$, SAVI L = 0.1 (TOA) |
| $\varepsilon_0$ | $0.95 + 0.01LAI$ | — | $0.95 + LAI/100$ |
| ε (LST/Rn uchun) | ASTER asosida (core) | $VI\varepsilon_C + (1 - VI)\varepsilon_S$ | $\varepsilon_{NB} = 0.97 + LAI/300$ |
| Tall-veg tuzatish | ✅ albedo, LST (canopy unmixing), Zom | ❌ (roughness orqali) | ❌ |

### 4.1 Raqamli: NDVI → LAI

Qizil reflectance $\rho_R$ = 0.15, 0.10, 0.06, 0.04 deb olingan va $\rho_{NIR}$ NDVI dan teskari hisoblangan (SAVI uchun).

| NDVI | SAVI (L=0.1) | EE $10NDVI^{3.5}$ | WS $11SAVI^3$ | WS $7NDVI^3$ |
|---|---|---|---|---|
| 0.2 | 0.174 | 0.036 | 0.058 | 0.056 |
| 0.4 | 0.338 | 0.405 | 0.427 | 0.448 |
| 0.6 | 0.495 | 1.673 | 1.334 | 1.512 |
| 0.8 | 0.704 | **4.579** | **3.838** | 3.584 |

→ To'liq qoplangan ekinda (NDVI 0.8) EE LAI ni ~19% yuqoriroq beradi. Bu $G$, $Z_{om}$ va $\varepsilon$ ga o'tadi.

---

## 5. Temperatura delapsing

| | EE | NI | WS |
|---|---|---|---|
| Datum | Sahna o'rtacha balandligi | **Dengiz sathi** | INI `datum` |
| Lapse rate | 3.0 K/km (May–Okt, tekis) / 6.5 K/km (tog' va qish), ikki qismli | Namli adiabatik $\Gamma_w(T, e_a, p)$ (~5–6 K/km) | 6.5 K/km konstanta |
| Gorizontal (lat/lon) tuzatish | ✅ spatial delapsing (robust regressiya + 8 tekshiruv) | ❌ | ❌ |

[EE 03](../openet-eemetric/docs/03_surface_temperature.md) · [EE 11](../openet-eemetric/docs/11_lapsed_surface_regions.md) · [NI 01](../pymetric-nieto/docs/01_kirish_va_radiatsiya.md) · [WS 02](../pymetric-wswup/docs/02_model1.md)

---

## 6. Radiatsiya balansi

| Komponent | EE | NI | WS |
|---|---|---|---|
| $R_{s\downarrow}$ | Clear-sky $R_{so}$: beam + diffuse ($f_{sky}$) + terrain | `S_dn` kirim → Weiss–Norman diffuz ulush → Campbell | $G_{sc}d_r\tau\cos\theta$ |
| $R_{L\downarrow}$ | $0.85(-\ln\tau)^{0.09}\sigma T_{cold}^4 f_{sky}$ + qiyalik nurlanishi | `L_dn` kirim yoki Brutsaert $1.24(e_a/T)^{1/7}\sigma T^4$ | $0.85(-\ln\tau)^{0.09}\sigma T_{cold,lap}^4$ |
| Qiyalik | ✅ $\cos\theta_{mtn}$, $C_{rad}$, $f_{sky}$ | ❌ | faqat `MOUNTAIN` cos θ (🐛) |

[EE 06](../openet-eemetric/docs/06_net_radiation.md) · [NI 01](../pymetric-nieto/docs/01_kirish_va_radiatsiya.md) · [WS 04](../pymetric-wswup/docs/04_model2.md)

---

## 7. Soil heat flux

| | EE | NI | WS |
|---|---|---|---|
| Asosiy | $(0.1 + 0.17e^{-0.55LAI})R_n\cdot M_{om}$ | 5 variant (konstanta, nisbat, Santanello, ASCE 0.04 / 0.10, Bastiaanssen) | Tasumi 2003: $(0.05 + 0.18e^{-0.521LAI})R_n$ ($LAI \ge 0.5$) |
| Suv | DOY funksiyasi → **residual** $R_n - H - LE_{aero}$ | landcover WATER mask'dan tashqari | $0.5R_n$ |
| Boshqa | qor, wetland, bazalt, muzlagan tuproq, issiq piksel kamaytirish | — | qor, wetland (ixtiyoriy) |

### 7.1 Raqamli: G/Rn vs LAI ($T_s$ = 305 K, $R_n$ = 550 W/m²)

| LAI | EE | WS (Tasumi 2003) | NI `G_form=4` (tall / short) |
|---|---|---|---|
| 0.0 | 0.270 | 0.188 * | 0.04 / 0.10 |
| 0.5 | 0.229 | 0.189 | 0.04 / 0.10 |
| 1.0 | 0.198 | 0.157 | 0.04 / 0.10 |
| 2.0 | 0.157 | 0.113 | 0.04 / 0.10 |
| 3.0 | 0.133 | 0.088 | 0.04 / 0.10 |
| 5.0 | 0.111 | 0.063 | 0.04 / 0.10 |

\* WS da $LAI < 0.5$ uchun $G = 1.8(T_s - 273.16) + 0.084R_n$ ($T_s$ ga bog'liq).

→ EE G ni WS dan ko'p beradi: LAI = 0.5 da ~21%, LAI = 3 da ~51%, LAI = 5 da ~76% (farq LAI oshgan sari ortadi). Namunaviy NI konfiguratsiyasida (`G_form=4`) G/Rn LAI ga bog'liq emas va ancha kichik. Natijada NI'da $LE + H$ uchun ko'proq energiya qoladi.

---

## 8. Aerodinamika

| | EE | NI | WS |
|---|---|---|---|
| $Z_{om}$ | NLCD lookup + $0.018LAI$ (ekin) + Perrier (daraxt, bog') + 5×5 silliqlash + tog' tuzatishi; suv $f(u_{200})$ | Schaudt & Dickinson (Raupach + Lindroth); ekin $h_C/8$, $d_0 = 0.65h_C$ | JSON: son / `perrier` / `LAI` ($0.018LAI$) |
| $d_0$ | 0 | ✅ hisoblanadi | 0 |
| Shamol | NLDAS $u_{10}$ → $u_{200}$ (sahna o'rtachasi, ≥ 5 m/s) + tog' tuzatishi | Mahalliy $u(z_u)$, blending height **yo'q** | Stansiya $u(2\,m)$, $z_{0,st}$ = 0.015 → $u_{200}$ |
| $r_{ah}$ | $z_1 = 0.1$, $z_2 = 2$ | `z_T`, $d_0$, $z_{0H}$ (KN99) — METRIC rejimi ishlamaydi (🐛) | $z_1 = 0.1$, $z_2 = 2$ |
| ψ funksiyalar | Paulson (+ damping, tog'da buoyancy) | **Brutsaert (2005)** | Paulson (damping yo'q) |
| L | $-\rho c_pu_*^3T/(kgH)$ | **Virtual** $H_v = H + 0.61Tc_pE$ | $-\rho c_pu_*^3T/(kgH)$ |
| Iteratsiyalar | kalibratsiya 11, piksel 9 | 15 + tebranishni aniqlash (2–3 tsikl) | kalibratsiya 20 / 100 (AUTO), raster 6 |

### 8.1 Raqamli: stabillik tuzatishlari

| $z/L$ | $\psi_m$ Paulson (EE, WS) | $\psi_m$ Brutsaert (NI) | $\psi_h$ Paulson | $\psi_h$ Brutsaert |
|---|---|---|---|---|
| −2.0 | 1.495 | 1.312 | 2.431 | 2.207 |
| −0.5 | 0.793 | 0.713 | 1.386 | 1.229 |
| −0.1 | 0.284 | 0.228 | 0.534 | 0.493 |
| 0.1 | −0.500 | −0.588 | −0.500 | −0.588 |
| 0.5 | −2.500 | −2.741 | −2.500 | −2.741 |

→ Beqaror sharoitda (kunduz, issiq dala) Brutsaert ψ Paulson'dan ~8–20% kichik → $r_{ah}$ biroz katta → bir xil dT da H biroz kichik. Bu farq kalibratsiya bilan qisman kompensatsiya qilinadi.

---

## 9. Kalibratsiya (hot / cold)

| | EE | NI | WS |
|---|---|---|---|
| Tanlash | Dynamic reyting: NDVI persentil oynalari, albedo (alfalfa), edge, LU, slope, $T_{s,dem}$ persentillari | CIMEC (Allen 2013) / ESA (Bhattarai 2017) / MINMAX | Ts bin + NDVI + albedo PDF + NLCD reyting → top 1% → tasodifiy klaster nuqtasi → **qo'lda** yoki Monte Carlo |
| $K_{c,cold}$ | $\mathrm{clamp}((NDVI - 0.15)/0.65, 0.11, 1)$ | $1.05\min(VI/0.95, 1)$ | **1.05** (INI) yoki DOY jadvali |
| $K_{c,hot}$ | $f_c$ (dynamic) / $f_c + (1 - f_c)K_e$ (static) | $VI\cdot K_{cc} + (1 - VI)ET_rF_{bare}$ | **0.10** yoki $\mathrm{clamp}(K_e, 0.1, 1.05)$ (MC) |
| dT | $aT_{s,dem} + b$, ekstremumlarda qiyalik $a/8$ | $a + bT_{R,datum}$ | $aT_{s,dem} + b$ |
| Sifat | $Q$ (reyting × ΔT > 4 × 0.01 < a < 1) | — | ΔT ≥ 4 K tekshiruvi, a/b chegaralari |
| Noaniqlik | — | — | ✅ Monte Carlo (tail size, Morton et al. 2013) |

### 9.1 Raqamli: cold piksel ETrF

| NDVI | EE | NI (VI ≈ NDVI) | WS |
|---|---|---|---|
| 0.6 | 0.692 | 0.663 | 1.05 |
| 0.7 | 0.846 | 0.774 | 1.05 |
| 0.8 | 1.000 | 0.884 | 1.05 |
| 0.9 | 1.000 | 0.995 | 1.05 |

→ Cold piksel to'liq qoplanmagan bo'lsa (NDVI < 0.8), EE va NI uning ETrF ini pasaytiradi, WS esa doim 1.05 deb oladi. Shu sababli WS'da cold nuqtani to'g'ri tanlash ayniqsa muhim.

[EE 10](../openet-eemetric/docs/10_pixel_selection.md) · [NI 03](../pymetric-nieto/docs/03_endmember_search.md) · [WS 03](../pymetric-wswup/docs/03_pixel_rating_points.md) · [WS 05](../pymetric-wswup/docs/05_auto_calibration_monte_carlo.md)

---

## 10. ET hisoblash va chiqish

| | EE | NI | WS |
|---|---|---|---|
| $H$ | $\rho c_pdT/(r_{ah}\cos s)$ | $\rho c_pdT/R_A$ | $1004\rho dT/r_{ah}$ |
| $ET_rF_{inst}$ | $ET_{inst}/ET_{r,inst}^{cold}\times C_{rad}$ | `fETr` = $LE/LE_{ref}$ (W/m² nisbat) | $ET_{inst}/ET_r$ |
| Reference ET | ASCE soatlik / kunlik (ichki), gridMET ETr × 0.85 | `pet_asce` (🐛 ishora va birlik) | NLDAS / gridMET / CIMIS (`refet` paketi) |
| ET24 | Ag: ETrF × ETr24; non-ag: EF + Slob $R_{n,24}$; suv: aerodinamik | ❌ | ETrF × ETr24 |
| Cheklash | ETrF ≥ 0; EToF ≤ 1.3 (suv 2.0) | yo'q | yo'q (interpolyatsiyada `low/high_etrf_limit`) |
| OpenET EToF | $ET_rF\cdot ET_{r,inst}/ET_{o,inst}$ | — | — |

[EE 12](../openet-eemetric/docs/12_etrf_et24_soil_water_balance.md) · [NI 02](../pymetric-nieto/docs/02_metric_yadro.md) · [NI 04](../pymetric-nieto/docs/04_reference_et.md) · [WS 04](../pymetric-wswup/docs/04_model2.md)

---

## 11. Vaqt bo'yicha interpolyatsiya

| | EE | WS |
|---|---|---|
| Interpolyatsiya qilinadigan kattalik | EToF (va NDVI) | ETrF (va NDVI) |
| Usul | chiziqli, piksel bo'yicha eng yaqin bulutsiz (mosaic) | chiziqli yoki kubik, `end_fill` + `temporal_fill` |
| Oyna | ±32 kun (`interp_days`) | yil chegarasi, kamida 2 sahna (`usable_image_count`) |
| Chekkalar | konstanta (qarama-qarshi tomondan) | konstanta (eng yaqin sana) |
| Agregatsiya | $\sum ET$, $\sum ET_o$, EToF = $\sum ET/\sum ET_o$ | $\sum ET$, $\sum ET_r$, $\sum P$, $\overline{NDVI}$, count |
| SWB tuzatish | — | hisoblanadi, lekin qo'llanmaydi (🐛) |

NI'da interpolyatsiya yo'q. [EE 13](../openet-eemetric/docs/13_collection_interpolation.md) · [WS 06](../pymetric-wswup/docs/06_interpolation.md)

---

## 12. Topilgan muammolar soni

| | EE | NI | WS |
|---|---|---|---|
| Potensial buglar | 11 | 13 | 16 |
| Eng jiddiysi | Shamol u/v `.max(0)` → instant shamol va ETr | `pet_asce`: $R_n$ ishorasi (+27% ETr), `use_METRIC_resistance` ishlamaydi | Landsat C1 + NumPy/pandas API → zamonaviy muhitda ishga tushmaydi |
| Batafsil | [EE 16](../openet-eemetric/docs/16_kuzatuvlar_va_moslashtirish.md) | [NI 06](../pymetric-nieto/docs/06_kuzatuvlar.md) | [WS 09](../pymetric-wswup/docs/09_kuzatuvlar.md) |

---

## 13. 🇺🇿 O'zbekiston uchun tavsiya

| Vazifa | Tavsiya | Sabab |
|---|---|---|
| Hududiy, ko'p yillik ET xaritalari (suv resurslari balansi) | **EE** (`conus_only=False` + global ETo manbasi) | C2, avtomatik kalibratsiya, spatial delapsing, interpolyatsiya, bulutda masshtablanadi |
| Bitta sahna / tadqiqot, fizikani boshqarish, flux tower bilan validatsiya | **NI** (`pet_asce` ni tuzatgan holda) | Kichik, o'qilishi oson kod; Campbell radiatsiyasi; tebranishga chidamli M–O iteratsiyasi |
| Kalibratsiya noaniqligini o'rganish (Monte Carlo), qo'lda kalibratsiya o'qitish | **WS** (algoritm g'oyalari uchun) | Monte Carlo tail-size usuli noyob; lekin C2 va yangi NumPy ga ko'chirish talab qilinadi |
| O'z modulli pipeline'ingiz | EE fizikasi + WS ning `et_numpy` uslubidagi sof funksiyalar + NI ning konvergensiya testi | Uchalasining kuchli tomonlarini birlashtirish (litsenziyalarga e'tibor: AGPL / GPL / Apache) |
