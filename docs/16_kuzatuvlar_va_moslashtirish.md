# 16 — Kod kuzatuvlari (bug / nuance) va O'zbekiston uchun moslashtirish

> Bu bo'lim — kodni o'qish davomida topilgan **muhandislik kuzatuvlari**. Ular statik tahlil asosida (kod ishga tushirilmagan, EE da test qilinmagan). Har birini o'z ma'lumotlaringizda tekshiring — "ishonma, tekshir" (trust, but verify) 🛰️.

---

## 1. Mantiqiy xatolar ehtimoli (Potential bugs)

| # | Joy | Kod | Muammo | Ta'sir |
|---|---|---|---|---|
| 1 | `momentum_roughness.py:177` | `land_use.neq(52).Or(land_use.neq(71))` | Har doim True → `rextra = 0` hamma joyda | Butazor/o'tloq uchun qo'shimcha qarshilik o'chiq |
| 2 | `automated_pixel_selection.py:198, 211` | `landuse.neq(11).Or(landuse.neq(12))` | Har doim True → Ag yo'q sahnada suv/muz ham "yaroqli" | Kam Ag sahnalarida kandidat sifati |
| 3 | `automated_pixel_selection.py:1346` | `slope_mask = cloud_mask.where(...)` | Hot uchun slope maskasi cloud maskasi bilan almashadi | Hot piksel tik qiyalikda tanlanishi mumkin (faqat `r_slope` reytingi himoya qiladi) |
| 4 | `gridded_dT.py:480` | `return single_block` | Lat/lon regressiyali `a`, `b` hisoblanadi, lekin ishlatilmaydi | "Gridded" dT amalda sahna-konstanta (dizayn tanlovi bo'lishi ham mumkin) |
| 5 | `lapsed_surface_regions.py:309` | `full_cover_temps.sort('elev', False)` | Natija o'zlashtirilmagan | Datum blok tanlovi deterministik emas |
| 6 | `weather.py:164–165, 184–196` | `wind_speed_u/v ... .max(0.0)` | Shamol **komponentlari** manfiy bo'lishi kerak | `instant_wind_speed` va `wind_aspect` buziladi → instant ETr, u200, leeward tuzatish |
| 7 | `eeflux.py:1805` | `EEFluxPreCalibrated.__init__` pozitsion argumentlar | `dem` → `image` parametriga tushadi | Klass ishlatilsa xato |
| 8 | `automated_pixel_selection.py:1504` | `daily_precip_etr(self, spinning_days)` | Funksiya 1 argument oladi | Chaqirilsa `TypeError` (hozir ishlatilmaydi) |
| 9 | `eeflux.py:1360` | `calib_prop_names = calib_prop_names.append([...])` | `list.append` → `None` | `copyProperties(img, None)` — barcha xususiyatlar ko'chiriladi (zararsiz) |
| 10 | `common_products.py:860` | RH: `e°(T_s)` Kelvin bilan | Formula °C uchun | `rh` noto'g'ri (faqat metadata) |
| 11 | `eeflux.py:1063` | `min_u200 = 5.0` | Izoh "4 m/s" deydi | Hujjat/kod nomuvofiqligi |

> 💡 **Tavsiya:** #1, #3, #6 ni tuzatish natijalarni o'zgartiradi. Fork qilib tuzatsangiz — OpenET bilan **solishtirma validatsiya** (masalan, flux tower yoki lizimetr) qiling. Upstream'ga issue ochish ham foydali.

---

## 2. Dizayn "nuance"lari (bug emas, lekin bilish shart)

| Mavzu | Tafsilot |
|---|---|
| **u200 — sahna konstantasi** | Shamol butun sahna bo'yicha o'rtacha (960 m reduksiya) va min 5 m/s. Katta sahnalarda shamol gradiyenti yo'qoladi. |
| **ETr_inst — cold piksel joyida** | ETrF maxraji sahna uchun bitta son. |
| **Cold ETrF ≠ 1.05** | Klassik METRIC 1.05; eeMETRIC NDVI asosida (≤ 1.0). |
| **Hot ETrF dynamic da Ke yo'q** | Faqat $f_c$; yaqinda yomg'ir bo'lgan sahnalarda hot piksel "nam" bo'lishi mumkin. |
| **gridMET ETr × 0.85, ETo × 1.0** | Kunlik ETr reduksiyasi asimmetrik. `et_fraction` ETrF ni instant ETr/ETo nisbatiga ko'paytiradi. |
| **Instant ETr clear-sky Rs bilan** | NLDAS Rs ishlatilmaydi. |
| **ETrF clamp** | `etrf` ≥ 0; `et_fraction` ≤ 2 (suv), ≤ 1.3 (boshqa). |
| **Lapse rate mavsumiy** | May–Oktyabr 3.0 K/km, qolgan oylar 6.5 K/km. |
| **`cloud_mask` ikki xil** | Pixel selection — simpleCloudScore + BQA (bufer 5 px); chiqish — QA_PIXEL + despeckle + 7.5 px dilate. |
| **Slope gradusda** | Docstring "percent" deydi. |
| **NDVI clamp** | `normalizedDifference` emas — NoData teshiklari yo'q. |

---

## 3. 🇺🇿 O'zbekiston (CONUS'dan tashqari) uchun moslashtirish

### 3.1 AQShga bog'liq assetlar

| Asset | Joy | Tashqarida | Yechim |
|---|---|---|---|
| `NASA/NLDAS/FORA0125_H002` | `weather.py` | ❌ NoData | `conus_only=False` → CFSv2; yoki ERA5-Land hourly ni `instant_*` ga bering |
| `IDAHO_EPSCOR/GRIDMET` | `weather.py` | ❌ | `conus_only=False` (CFSv2) yoki ERA5-Land daily → `daily_weather_series` |
| `projects/climate-engine/cimis/daily` | `weather.py` | ❌ (−300 sentinel bilan xavfsiz) | — |
| `projects/sat-io/.../ANNUAL_NLCD` | `common_products.py` | ❌ → ESA WorldCover ishlatiladi ✅ | ESA ni yangiroq `ESA/WorldCover/v200` bilan almashtirish mumkin |
| `projects/openet/assets/crop_type/v2024a` | `merge_nlcd_crop_type_layers` | ❌ (bo'sh → NLCD fallback) | `tall_crops_flag = 0` → bog'lar o'rmon sifatida emas; o'z bog'/tokzor maskangizni bering |
| `projects/openet/eemetric/elevation/stddev`, `.../relative` | `_std_elev`, `_rel_elev` | ⚠️ ehtimol qamrovsiz | `calculate_elevation_std(dem)`, `calculate_relative_elevation(dem)` bilan hisoblang |
| `projects/openet/assets/features/water_mask` | `lapsed_surface_regions.py` | ⚠️ | `JRC/GSW1_4/GlobalSurfaceWater` `max_extent` |
| `projects/eeflux/soils/gsmsoil_*` (STATSGO) | tuproq | ❌ → global `GSD_*` fallback ✅ | Yoki SoilGrids / OpenLandMap |
| `NASA/ASTER_GED/AG100_003` | core LST | ✅ global | — |
| `USGS/SRTMGL1_003` | DEM | ✅ (60°S–60°N) | Copernicus GLO-30 ham mumkin |
| `ESA/WorldCover/v100` | land use | ✅ | — |

### 3.2 Minimal global ishlatish

```python
import ee
import openet.eemetric as model

ee.Initialize()
img_id = 'LANDSAT/LC09/C02/T1_L2/LC09_PPPRRR_YYYYMMDD'   # o'z sahnangiz ID si (WRS-2 path/row + sana)

m = model.Image.from_landsat_c2_sr(
    img_id,
    conus_only=False,                 # ⭐ CFSv2 fallback
    spatial_delapsing=True,
    et_reference_source='projects/openet/assets/reference_et/...',   # yoki o'z ETo kolleksiyangiz
    et_reference_band='eto',
    et_reference_factor=1.0,
    et_reference_resample='bilinear',
)
out = m.calculate(['et_fraction', 'ndvi'])
```

> ⚠️ `et_reference_source` uchun global ETo kolleksiyasi kerak (masalan ERA5-Land dan oldindan hisoblangan ASCE ETo). Bu — alohida modul sifatida qurilishi kerak bo'lgan "Preprocessing" qismi.

### 3.3 O'zbekistonga xos fizik eslatmalar

| Masala | Eslatma |
|---|---|
| **Sho'rlangan tuproqlar** (Sirdaryo, Qoraqalpog'iston) | Yuqori albedo (>0.3) → hot piksel albedo targeti 0.20 dan uzoq; reyting past bo'lishi mumkin |
| **Paxta defoliatsiyasi** (sentyabr) | NDVI keskin tushadi → $K_{c,cold}$ va EToF interpolyatsiyasida "sakrash" |
| **Sholi** (Xorazm) | NDVI past + suv → `snow_water_flag = 2` bo'lishi mumkin → aerodinamik bug'lanish |
| **Tog' oldi** (Toshkent, Surxondaryo) | `mountain_toggle` (Δz > 1000 m) → lapse, $C_{rad}$, Zom tuzatishlari faollashadi |
| **Orol bo'yi** | Katta suv havzasi + spatial delapsing → `water_mask` muhim |
| **CRS** | O'zbekiston UTM zonalari: **EPSG:32641** (λ < 66°), **32642** (66–72°), **32643** (> 72°). Eksportda Landsat sahnaning o'z CRS ini (`img.select('SR_B4').projection()`) ishlating. |
| **Vaqt** | Overpass ~05:30–06:00 UTC (10:30–11:00 mahalliy). Quyosh kuni UTC+~4.6 soat siljiydi. |

---

## 4. Modulli (Clean Code) refaktoring g'oyalari

Sizning Preprocessing / Calculations / Output uslubingiz uchun:

```text
metric_uz/
├── preprocessing/
│   ├── landsat.py        # C2 SR scale, cloud mask, LST correct   ← 01
│   ├── weather.py        # ERA5-Land instant + daily               ← 04 (NLDAS/gridMET o'rniga)
│   ├── reference_et.py   # ASCE PM (sof funksiyalar)               ← 04 asce_*
│   ├── terrain.py        # DEM, slope, σz, RE, cosθ               ← 05
│   └── landcover.py      # ESA WorldCover → NLCD + bog' maskasi   ← 05
├── calculations/
│   ├── surface.py        # albedo, NDVI, LAI, ε, snow/water        ← 02
│   ├── temperature.py    # lapse, spatial delapsing, canopy        ← 03, 11
│   ├── radiation.py      # Rso, Rn                                 ← 06
│   ├── soil_heat.py      # G                                       ← 07
│   ├── roughness.py      # Zom                                     ← 08
│   ├── calibration.py    # pixel selection + dT                    ← 10, 09
│   ├── sensible_heat.py  # H, M–O                                  ← 09
│   └── et.py             # ETrF, ET24, SWB                         ← 12
└── output/
    ├── interpolation.py  # kunlik/oylik                            ← 13
    └── export.py         # CRS, scale, metadata
```

Asosiy prinsip: eeMETRIC'dagi `*_general(...)` funksiyalar allaqachon **sof** (self'siz) — ularni to'g'ridan-to'g'ri qayta ishlatish mumkin. `self`-ga bog'liq wrapperlarni `dataclass` konfiguratsiya + dependency injection bilan almashtirish kodni test qilinadigan qiladi.

> ⚠️ **Litsenziya:** eeMETRIC — **AGPL-3.0**. Koddan nusxa olib (hatto refaktoring qilib) tarqatsangiz yoki tarmoq servisi sifatida ishlatsangiz, sizning kodingiz ham AGPL bo'lishi kerak. Faqat formulalarni (ilmiy maqolalardan) mustaqil implementatsiya qilish — boshqa masala.
