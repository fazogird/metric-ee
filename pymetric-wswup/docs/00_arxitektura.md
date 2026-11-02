# 00 — Arxitektura (pymetric, WSWUP)

## 1. Papka tuzilishi (31 417 qator Python, 62 fayl)

```text
pymetric-master/
├── code/
│   ├── local/                 # ⭐ foydalanuvchi ishga tushiradigan skriptlar (CLI)
│   │   ├── landsat_prep_path_row.py   (1087)
│   │   ├── landsat_prep_ini.py        (767)
│   │   ├── landsat_prep_scene.py
│   │   ├── metric_model1.py / metric_model2.py
│   │   ├── metric_pixel_rating.py / metric_pixel_points.py
│   │   ├── metric_monte_carlo.py      (359)
│   │   └── landsat_interpolate.py     (266)
│   ├── prep_functions/landsat_prep_scene_func.py   (1124)
│   ├── metric_functions/
│   │   ├── metric_model1_func.py      (1147)
│   │   ├── metric_model2_func.py      (1830)
│   │   ├── pixel_rating_func.py       (827)
│   │   ├── pixel_points_func.py       (382)
│   │   ├── auto_calibration_func.py   (753)
│   │   └── monte_carlo_func.py        (560)
│   ├── interp_functions/
│   │   ├── interpolate_support.py     (1027)
│   │   ├── interpolate_rasters_func.py(2166)
│   │   └── interpolate_tables_func.py (1809)
│   ├── support/
│   │   ├── et_numpy.py      (2271) ⭐ fizik formulalar (60 funksiya)
│   │   ├── et_common.py     (1759) ⭐ quyosh, atmosfera, SWB, RefET o'qish
│   │   ├── et_image.py      (577)    Landsat sahna klassi (MTL, koeffitsientlar)
│   │   └── python_common.py (358)
│   └── ini_templates/       # landsat_project.ini, landsat_metric_inputs.ini, ...
├── tools/                   # download, nldas, gridmet, cimis, daymet, plotting
├── misc/                    # zom_nlcd_*.json, etrf_training_*.csv, etrf_doy_adj.csv
├── example/                 # Harney Basin (Oregon), landsat_2015.ini
└── docs/                    # INSTALL, EXAMPLE_DATA/SETUP/METRIC
```

| Qatlam | Modullar |
|---|---|
| Preprocessing | `tools/*`, `landsat_prep_path_row`, `landsat_prep_ini`, `landsat_prep_scene_func`, `et_image` |
| Calculations | `metric_model1_func`, `pixel_rating_func`, `pixel_points_func`, `metric_model2_func`, `auto_calibration_func`, `monte_carlo_func`, `et_numpy`, `et_common` |
| Output | `interpolate_*`, `tools/plotting` |

> 💡 Arxitektura **funksional**: `et_numpy.py` dagi formulalar sof NumPy funksiyalari (`self` yo'q), orkestratorlar (`*_func.py`) ularni bloklar bo'yicha (`drigo.block_gen`, default 1024–2048 piksel) chaqiradi. Bu xotira jihatidan samarali: butun sahna xotiraga yuklanmaydi.

## 2. Ishga tushirish ketma-ketligi

```bash
python code/local/landsat_prep_path_row.py -i example/landsat_2015.ini
```

```bash
python code/local/landsat_prep_ini.py -i example/landsat_2015.ini
```

```bash
python code/local/landsat_prep_scene.py -i example/landsat_2015.ini
```

```bash
python code/local/metric_model1.py -i example/landsat_2015.ini
```

```bash
python code/local/metric_pixel_rating.py -i example/landsat_2015.ini
```

```bash
python code/local/metric_pixel_points.py -i example/landsat_2015.ini
```

> ⚠️ Rasmiy hujjat: Model 2 dan oldin kalibratsiya nuqtalarini **ArcGIS'da qo'lda** tuzatish kerak. Aks holda ETrF "sezilarli darajada yomonlashadi". Muqobil yo'l — Monte Carlo ([05](05_auto_calibration_monte_carlo.md)).

```bash
python code/local/metric_model2.py -i example/landsat_2015.ini
```

```bash
python code/local/landsat_interpolate.py -i example/landsat_2015.ini --tables
```

```bash
python code/local/landsat_interpolate.py -i example/landsat_2015.ini --rasters
```

Monte Carlo (1% cold, 4% hot tail):

```bash
python code/local/metric_monte_carlo.py -i example/landsat_2015.ini -mc 0 --tails 1 4
```

## 3. INI fayllar

| Fayl | Bo'limlar | Vazifa |
|---|---|---|
| `landsat_project.ini` | `[INPUTS]` | Loyiha papkalari, yil, path/row, keyingi INI yo'llari |
| `landsat_metric_inputs.ini` | `[INPUTS]` | Model 1/2 parametrlari (pastda) |
| `landsat_metric_pixel_rating.ini` | | Rating flaglari, persentillar |
| `landsat_metric_monte_carlo.ini` | | Tail size, Kc DOY jadvali, SWB |
| `landsat_interpolate.ini` | | Interpolyatsiya, chiqish proyeksiyasi |

`dripy.read_param(name, default, config, section)` — INI dan qiymat va default.

### 3.1 `landsat_metric_inputs.ini` asosiy defaultlari

| Parametr | Default | Ma'no |
|---|---|---|
| `kc_cold_pixel` / `kc_hot_pixel` | 1.05 / 0.10 | Kalibratsiya ETrF |
| `datum` | sahna (masalan 86.868 m) | Delapse balandligi |
| `lapse_rate` | 6.5 K/km | |
| `weather_data_source` | NLDAS | NLDAS / REFET / MANUAL |
| `wind_speed_height` / `station_roughness` | 2.0 m / 0.015 m | $u_{200}$ uchun |
| `additional_wind_speed` | 0.0 | |
| `pair_model` | DEM | DEM / DATUM |
| `cos_theta_model` | **CENTROID** | SOLAR / CENTROID / SPATIAL / MOUNTAIN |
| `refl_sur_model_type` | TASUMI | TASUMI / LEDAPS |
| `lai_toa_veg_index_type` | SAVI | SAVI / NDVI |
| `em_refl_type` | TOA | |
| `g_model_type` / `g_refl_type` | METRIC / TOA | METRIC / SEBAL |
| `use_g_water_flag` | True | |
| `zom_remap_path` | `misc/zom_nlcd_default.json` | |
| `stability_pixel_mode` | AUTO2 | MANUAL / AUTO / AUTO2 |
| `stability_raster_mode` / `_iters` | MANUAL / 6 | |
| `block_size` | 1536 | |

## 4. Bog'liqliklar (`requirements.txt`)

`drigo>=0.1.4` (GDAL yordamchi — DRI), `gdal>=2.2.3`, `numpy>=1.14`, `scipy>=1.0`, `pandas`, `netCDF4`, `matplotlib`, `refet>=0.3.7`, `requests`, `requests-html`, `future==0.16.0`, `configparser`.

> ⚠️ Kodda `np.bool`, `np.int`, `np.float` 37 marta uchraydi. NumPy ≥ 1.24 da bular **olib tashlangan** → `AttributeError`. Eski NumPy (< 1.24) muhiti kerak yoki kodni tuzatish lozim ([09](09_kuzatuvlar.md)).

## 5. Sahna papkasi va fayl formatlari

`et_image.Image(image_folder)` — papka nomi Landsat **Collection 1** ID ga mos bo'lishi shart (regex: `^(LT04|LT05|LE07|LC08)_\w{4}_PPPRRR_YYYYMMDD_YYYYMMDD_\d{2}_\w{2}$`). Raster formati: **ERDAS Imagine `.img`**.

| Pastki papka | Rasterlar |
|---|---|
| `ORIGINAL_DATA` | DN bandlar, `*_MTL.txt` |
| `SUPPORT` | `common_area`, `fmask`, `cloud/snow/water_mask_fmask`, `ea_metric`, `wind_metric`, `etr_metric`, `etr_24hr_metric`, `tair_metric` |
| `REFLECTANCE_TOA` / `_SUR` | `refl_toa`, `refl_sur_tasumi`, `refl_sur_ledaps` |
| `INDICES` | `ndvi(_toa)`, `ndwi(_toa)`, `lai(_toa)`, `savi` |
| asosiy | `albedo_at_sur`, `ts`, `ts_dem`, `cos_theta` |
| `PIXELS`, `PIXEL_REGIONS` | `cold.shp`, `hot.shp`, rating rasterlari |
| `ETRF`, `ET24`, `RN`, `G`, `H`, `ZOM`, `LE` | Model 2 chiqishlari |

**CRS:** `env.snap_osr` = **EPSG:(32600 + UTM_ZONE)** (MTL dan), `cellsize = 30`, snap nuqtasi (15, 15) — Landsat L1 grid'iga mos.
