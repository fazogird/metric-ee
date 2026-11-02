# 05 — Funksiyalar indeksi (pyMETRIC, Nieto)

> Qator raqamlari — yuklangan `pyMETRIC-master_1.zip` dagi fayllar bo'yicha. Jami: **33** funksiya/metod (5 fayl) + **27** ta ishlatilgan pyTSEB funksiyasi.

## `pyMETRIC/METRIC.py` — fizik yadro

| # | Funksiya | Qator | Vazifa / formula | Hujjat |
|---|---|---|---|---|
| 1 | `METRIC` | 37 | Endmember kalibratsiya + piksel iteratsiyasi → (flag, Ln, LE, H, G, R_A, u*, L, n) | [02](02_metric_yadro.md) |
| 2 | `_L_diff` | 350 | $\lvert L - L_{old}\rvert/\lvert L_{old}\rvert$, NaN→∞ | [02](02_metric_yadro.md) |
| 3 | `calc_dT` | 356 | $HR_A/(\rho c_p)$ | [02](02_metric_yadro.md) |
| 4 | `calc_G_Allen` | 362 | $R_n(T-273.15)(0.0038+0.0074\alpha)(1-0.98NDVI^4)$ | [01](01_kirish_va_radiatsiya.md) |
| 5 | `calc_H` | 383 | $\rho c_pdT/R_A$ | [02](02_metric_yadro.md) |
| 6 | `calc_H_residual` | 411 | $R_n - G - LE$ | [02](02_metric_yadro.md) |
| 7 | `pet_asce` | 433 | ASCE tipidagi PM, W/m² (⚠️ birliklar) | [04](04_reference_et.md) |
| 8 | `pet_fao56` | 505 | FAO-56 $R_c/R_a$ shakli (chaqirilmaydi) | [04](04_reference_et.md) |
| 9 | `calc_Ln` | 570 | $\sigma f_{cd}(0.34-0.14\sqrt{0.1e_a})T^4$ | [04](04_reference_et.md) |
| 10 | `calc_cloudiness` | 595 | $\mathrm{clamp}(1.35S/S_0-0.35, 0.05, 1)$ (chaqirilmaydi) | [04](04_reference_et.md) |
| 11 | `wind_profile` | 602 | Log shamol profili | [04](04_reference_et.md) |

## `pyMETRIC/endmember_search.py`

| # | Funksiya | Qator | Vazifa | Hujjat |
|---|---|---|---|---|
| 1 | `maxmin_temperature` | 15 | Min/max LST (VI ≥ / ≤ $P_{0.05}$) | [03](03_endmember_search.md) |
| 2 | `cimec` | 39 | Allen 2013 CIMEC | [03](03_endmember_search.md) |
| 3 | `esa` | 143 | Bhattarai 2017 ESA | [03](03_endmember_search.md) |
| 4 | `histogram_fiter` | 255 | Gistogramma chekka bin tozalash (<50 px) | [03](03_endmember_search.md) |
| 5 | `rank_array` | 300 | Rang massivi | [03](03_endmember_search.md) |
| 6 | `incremental_search` | 307 | Persentil oynasini kengaytirib ≥10 kandidat | [03](03_endmember_search.md) |
| 7 | `moving_cv_filter` | 348 | 11×11 CV, mean, std | [03](03_endmember_search.md) |

## `pyMETRIC/PyMETRIC.py`

| # | Funksiya | Qator | Vazifa | Hujjat |
|---|---|---|---|---|
| 1 | `class PyMETRIC(PyTSEB)` | 69 | Orkestrator | [00](00_arxitektura.md) |
| 2 | `PyMETRIC.__init__` | 71 | Defaultlar | [00](00_arxitektura.md) |
| 3 | `PyMETRIC._get_input_structure` | 91 | Kirish maydonlari (TSEB'dan farq) | [00](00_arxitektura.md) |
| 4 | `PyMETRIC._set_special_model_input` | 120 | `x_LAD`, `f_c`, `w_C` ixtiyoriy (default 1) | [00](00_arxitektura.md) |
| 5 | `PyMETRIC._get_output_structure` | 150 | Chiqish maydonlari va saqlash turi | [00](00_arxitektura.md) |
| 6 | `PyMETRIC.process_local_image` | 192 | O'qish → `run_METRIC` → yozish | [00](00_arxitektura.md) |
| 7 | `PyMETRIC.run_METRIC` | 479 | Sn, roughness, datum, ETrF, guruh tsikli | [01](01_kirish_va_radiatsiya.md), [03](03_endmember_search.md) |
| 8 | `PyMETRIC._call_flux_model` | 724 | `METRIC.METRIC` chaqiruvi | [02](02_metric_yadro.md) |
| 9 | `PyMETRIC._open_GDAL_image` | 764 | Son yoki GDAL raster → massiv | [00](00_arxitektura.md) |
| 10 | `PyMETRIC._write_raster_output` | 796 | GeoTIFF / VRT / NetCDF | [00](00_arxitektura.md) |
| 11 | `get_nested_position` | 883 | aoi 1-D indeks → global (row, col) | [03](03_endmember_search.md) |

## `pyMETRIC/METRICConfigFileInterface.py` va `METRIC_local_image_main.py`

| # | Funksiya | Qator | Vazifa |
|---|---|---|---|
| 1 | `class METRICConfigFileInterface` | 22 | Config → parametrlar |
| 2 | `.__init__` | 24 | `PyMETRIC` dan kirish maydonlari ro'yxatini oladi |
| 3 | `.parse_input_config` | 34 | `kalit=qiymat` qatorlari |
| 4 | `.get_data` | 60 | `G_form`, `calc_row`, `water_stress`, `output_file` |
| 5 | `.run` | 115 | `model == "pyMETRIC"` → `process_local_image` |
| 6 | `run_METRIC_from_config_file` (main) | 24 | CLI kirish nuqtasi |

---

## Ishlatilgan pyTSEB funksiyalari

| Modul | Funksiya | Formula / vazifa | Hujjat |
|---|---|---|---|
| `meteo_utils` | `calc_rho` | $\frac{100p}{R_dT}(1 - 0.378e_a/p)$ | [02](02_metric_yadro.md) |
| | `calc_c_p` | $(1-q)1003.5 + 1865q$ | [02](02_metric_yadro.md) |
| | `calc_lambda` | $10^6(2.501 - 2.361\cdot10^{-3}t)$ | [04](04_reference_et.md) |
| | `calc_psicr` | $c_pp/(0.622\lambda)$ | [04](04_reference_et.md) |
| | `calc_vapor_pressure` | $6.112e^{17.67t/(t+243.5)}$ mb | [04](04_reference_et.md) |
| | `calc_delta_vapor_pressure` | FAO Δ, kPa/K | [04](04_reference_et.md) |
| | `calc_pressure` | $1013.25(1 - 2.2256\cdot10^{-5}z)^{5.256}$ | [01](01_kirish_va_radiatsiya.md) |
| | `calc_stephan_boltzmann` | $\sigma T^4$ | [01](01_kirish_va_radiatsiya.md) |
| | `calc_sun_angles` | SZA, SAA (EOT bilan) | [01](01_kirish_va_radiatsiya.md) |
| | `calc_lapse_rate_moist` | $\Gamma_w$ K/m | [01](01_kirish_va_radiatsiya.md) |
| | `calc_mixing_ratio` | $0.622e_a/(p-e_a)$ | [01](01_kirish_va_radiatsiya.md) |
| `MO_similarity` | `calc_u_star` | $ku/(\ln\frac{z-d}{z_0} - \Psi_M + \Psi_{M0})$ | [02](02_metric_yadro.md) |
| | `calc_L` → `calc_mo_length_hv` | Virtual H bilan L | [02](02_metric_yadro.md) |
| | `calc_Psi_M` → `psi_m_brutsaert` | Brutsaert 2005 | [02](02_metric_yadro.md) |
| | `calc_Psi_H` → `psi_h_brutsaert` | Brutsaert 2005 | [02](02_metric_yadro.md) |
| `resistances` | `calc_R_A` | Norman 1995 | [02](02_metric_yadro.md) |
| | `calc_z_0H` | $z_{0M}e^{-kB}$ | [01](01_kirish_va_radiatsiya.md) |
| | `calc_roughness` | Schaudt & Dickinson 2000 | [01](01_kirish_va_radiatsiya.md) |
| | `raupach` | Raupach 1994 | [01](01_kirish_va_radiatsiya.md) |
| | IGBP konstantalari | WATER=0 … BARREN=16 | [03](03_endmember_search.md) |
| `net_radiation` | `calc_difuse_ratio` | Weiss & Norman 1985 | [01](01_kirish_va_radiatsiya.md) |
| | `calc_Sn_Campbell` | Campbell & Norman 1998 | [01](01_kirish_va_radiatsiya.md) |
| | `calc_emiss_atm` | Brutsaert 1975 | [01](01_kirish_va_radiatsiya.md) |
| `TSEB` | `calc_G` | G variantlari dispetcheri | [01](01_kirish_va_radiatsiya.md) |
| | `calc_resistances` | `KUSTAS_NORMAN_1999` | [02](02_metric_yadro.md) |
| | `_check_default_parameter_size` | Skalyar → massiv | [02](02_metric_yadro.md) |
| `PyTSEB` | `PyTSEB` (bazaviy klass), `S_N`, `S_P`, `S_A` | | [00](00_arxitektura.md) |
