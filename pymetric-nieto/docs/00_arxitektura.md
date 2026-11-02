# 00 — Arxitektura (pyMETRIC, Nieto)

## 1. Fayllar

```text
pyMETRIC-master/
├── METRIC_local_image_main.py      # CLI: python METRIC_local_image_main.py <config>
├── Config_LocalImage.txt           # namunaviy konfiguratsiya
├── setup.py                        # name=pyMETRIC, version=1.0, REQS: numpy, gdal, bokeh, pandas, netCDF4, pyTSEB
├── Input/                          # ExampleImage_{Trad_pm, LAI, NDVI}.tif
├── Output/                         # test_image.tif, test_image_ancillary.tif
└── pyMETRIC/
    ├── METRIC.py                   # ⭐ fizik yadro (606 qator)
    ├── endmember_search.py         # hot/cold tanlash (361 qator)
    ├── PyMETRIC.py                 # rasterlarni o'qish/yozish, orkestratsiya (888 qator)
    └── METRICConfigFileInterface.py# config parser (130 qator)
```

| Qatlam | Modul | Vazifa |
|---|---|---|
| Preprocessing | `PyMETRIC.process_local_image` | GDAL bilan o'qish, subset, quyosh burchaklari, $p$, $L_{dn}$, mask |
| Calculations | `PyMETRIC.run_METRIC`, `METRIC.py`, `endmember_search.py` | $S_n$, $z_{0M}$, datum, ETrF, endmember, oqimlar |
| Output | `PyMETRIC._write_raster_output` | GeoTIFF / VRT / NetCDF |

## 2. Klass ierarxiyasi

```text
pyTSEB.PyTSEB.PyTSEB
   └── pyMETRIC.PyMETRIC.PyMETRIC
METRICConfigFileInterface  ──(yaratadi)──►  PyMETRIC
```

`PyMETRIC` pyTSEB'ning `PyTSEB` klassidan **meros oladi**. U `_get_input_structure`, `_set_special_model_input`, `_get_output_structure` ni override qiladi. `G_form`, `p` (parametrlar lug'ati) va `_get_subset` lar ham pyTSEB'dan keladi.

### 2.1 `PyMETRIC.__init__` defaultlari

| Parametr | Default | Ma'no |
|---|---|---|
| `use_METRIC_resistance` | 1 | 1 = Allen (z_T=2, z_0H=0.1, d=0), 0 = Kustas & Norman 1999 (⚠️ [06](06_kuzatuvlar.md) #1 ga qarang) |
| `ET_bare_soil` | 0 | Yalang'och tuproq ETrF (raster yoki 0) |
| `VI` | `''` | Vegetatsiya indeksi raster |
| `endmember_search` | 0 | 0 = CIMEC, 1 = ESA, 2 = MINMAX |
| `G_tall` | 0.04 | G/Rn baland o'simlik |
| `G_short` | — | 🐛 Kod `parameters["G_tall"] = 0.10` deb yozadi ([06](06_kuzatuvlar.md) #4) |
| `resistance_form` | 0 (majburan) | KUSTAS_NORMAN_1999 |

### 2.2 Modul konstantalari

| Konstanta | Qiymat | Joy |
|---|---|---|
| `L_thres` | 0.001 | L konvergensiya (nisbiy) |
| `u_friction_min` | 0.01 m/s | |
| `ITERATIONS` | 15 | |
| `kB` | 0 | $z_{0H} = z_{0M}$ |
| `SB` | 5.670373e-8 | |
| `KARMAN` | 0.41 | |
| `VI_MAX` (PyMETRIC) | 0.95 | |
| `VI_SOIL`, `VI_FULL` (endmember) | 0.0, 0.95 | e'lon qilingan, ishlatilmaydi |

## 3. Konfiguratsiya fayli (`Config_LocalImage.txt`)

Format: `kalit=qiymat`, `#` bilan izoh. Har bir raster parametr **fayl yo'li** yoki **son** (butun maydon uchun konstanta) bo'lishi mumkin (`_open_GDAL_image`: avval `float()` sinab ko'riladi, bo'lmasa GDAL).

| Guruh | Kalitlar | Birlik |
|---|---|---|
| Asosiy | `model=pyMETRIC`, `T_R1` (LST, **majburiy**), `input_mask`, `output_file` | K |
| Vegetatsiya | `LAI`, `VI`, `f_c`, `h_C`, `w_C`, `x_LAD`, `landcover` (IGBP kodlari) | m²/m², –, m |
| Joy | `lat`, `lon`, `alt`, `stdlon`, `z_T`, `z_u` | °, m |
| Meteo | `DOY`, `time` (soat, `stdlon` vaqti), `T_A1`, `u`, `p`, `ea`, `S_dn`, `L_dn` | K, m/s, **mb**, **mb**, W/m² |
| Spektr | `emis_C`, `emis_S`, `rho_vis_C`, `tau_vis_C`, `rho_nir_C`, `tau_nir_C`, `rho_vis_S`, `rho_nir_S` | – |
| Qarshilik | `use_METRIC_resistance`, `z0_soil` | m |
| G | `G_form` (0/1/2/4/5), `G_constant`, `G_ratio`, `G_amp`, `G_phase`, `G_shape`, `G_tall`, `G_short` | |
| METRIC | `endmember_search`, `ETrF_bare` | |

> ⚠️ **Birliklar:** `ea` va `p` — **millibar (hPa)**, kPa emas. `time` — `stdlon` meridianidagi mahalliy standart vaqt (UTC emas). O'zbekiston uchun `stdlon=75` (UTC+5).

### `G_form` variantlari (`get_data`)

| Kod | `G_form` strukturasi | Ma'no |
|---|---|---|
| 0 | `[[0], G_constant]` | Konstant G |
| 1 | `[[1], G_ratio]` | $G = r\cdot R_n$ |
| 2 | `[[2, amp, phase, shape], 12.0]` | Santanello & Friedl (2003) |
| 4 | `[[4], (G_tall, G_short)]` | ASCE nisbatlari (tall/short guruh bo'yicha) |
| 5 | `[[5], None]` | Bastiaanssen/Allen 2007 Eq. 26 |

## 4. Ma'lumot oqimi (`process_local_image` → `run_METRIC`)

1. `T_R1` ni ochish → `prj`, `geo` (GeoTransform), `dims`; ixtiyoriy `subset = [xoff, yoff, xsize, ysize]`.
2. Barcha rasterlarni ochish (har biri `success` tekshiruvi bilan; xato bo'lsa `return`).
3. `met.calc_sun_angles(lat, lon, stdlon, doy, time)` → `SZA`, `SAA`.
4. `p` berilmagan bo'lsa → `met.calc_pressure(alt)`.
5. `L_dn` berilmagan bo'lsa → $\varepsilon_a(e_a, T_a)\,\sigma T_a^4$ (Brutsaert).
6. **Mask:** `input_mask` raster yoki landcover ∉ {WATER, URBAN, SNOW}; `VI` yoki `T_R1` NaN bo'lsa 0.
7. `ET_bare_soil` raster yoki 0.
8. `G_form` sozlash.
9. `run_METRIC(in_data, mask)` → [01](01_kirish_va_radiatsiya.md), [02](02_metric_yadro.md), [03](03_endmember_search.md).
10. Chiqish: `S_P` (primary) va `S_A` (ancillary) maydonlar alohida faylga.

## 5. Chiqish maydonlari (`_get_output_structure`)

| Maydon | Saqlanadi | Ma'no |
|---|---|---|
| `R_n1`, `H1`, `LE1`, `G1` | **primary** (`output_file`) | W/m² |
| `R_ns1`, `R_nl1`, `R_A1`, `L`, `u_friction`, `flag`, `ET0_datum`, `ET0`, `fETr` | ancillary (`*_ancillary.*`) | |
| `omega0`, `theta_s1`, `F`, `z_0M`, `d_0`, `Skyl`, `n_iterations` | saqlanmaydi (`S_N`) | |

> `OrderedDict` da `'L'` ikki marta yozilgan — bitta kalit bo'lib qoladi.

### Formatlar (`_write_raster_output`)

| Kengaytma | Natija |
|---|---|
| `.nc` | GDAL netCDF + `netCDF4` bilan band nomlari va `grid_mapping` tuzatiladi |
| `.vrt` | `<nom>.data/<maydon>.tif` (har maydon alohida) + `gdal.BuildVRT(separate=True)` |
| boshqa | Bitta ko'p bandli GeoTIFF |

NoData = `NaN`, tip `Float32`, CRS va GeoTransform kirish `T_R1` dan **o'zgarishsiz** olinadi.
