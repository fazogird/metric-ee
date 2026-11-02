# 07 — Tools: ma'lumot yuklash va ob-havo (pymetric, WSWUP)

> **Manba:** `tools/` (download, nldas, gridmet, cimis, daymet, plotting), `code/support/et_common.py` (RefET o'qish funksiyalari)

---

## 1. Umumiy ko'rinish

| Papka | Skriptlar | Mahsulot |
|---|---|---|
| `download/` | `download_landsat.py`, `download_footprints.py` (WRS-2), `download_ned.py` (1″ NED tiles), `download_nlcd.py` (2006/2011), `download_cdl.py`, `download_landfire.py`, `download_soils.py` (STATSGO2 AWC) | Kirish rasterlari |
| `nldas/` | `nldas_download.py` (.grb), `nldas_ancillary.py` (mask, elev, lat, lon), `nldas_hourly_ea.py`, `nldas_hourly_wind.py`, `nldas_hourly_refet.py`, `nldas_hourly_variable.py` | Soatlik `ea`, `wind`, `ETr/ETo` (.img) |
| `gridmet/` | `gridmet_download.py` (.nc), `gridmet_ancillary.py`, `gridmet_daily_refet.py`, `gridmet_daily_ea/ppt/temp/variables.py` | Kunlik ETr/ETo, PPT, Tmin/Tmax, ea |
| `cimis/` | `cimis_download.py`, `cimis_extract_convert.py`, `cimis_daily_refet.py`, `cimis_gridmet_fill.py`, `cimis_ancillary.py` | Kaliforniya kunlik RefET |
| `daymet/` | `daymet_download.py`, `daymet_daily_*.py`, `daymet_climatologies.py` | Kunlik meteo |
| `plotting/` | `summary_histograms.py` | Gistogrammalar |

> 🌍 Barcha ob-havo manbalari (NLDAS, gridMET, CIMIS, Daymet) va yer qoplami manbalari (NLCD, CDL, NED, STATSGO) **faqat AQSh** uchun.

## 2. NLDAS soatlik RefET — `nldas_hourly_refet.py`

`refet.Hourly` (ASCE-EWRI 2005) bilan:

```python
pair = refet.calcs._air_pressure(elev=elev_array)
ea   = refet.calcs._actual_vapor_pressure(q=sph_array, pair=pair)
refet_obj = refet.Hourly(tmean=..., ea=ea, rs=..., uz=wind, zw=10,
                         elev=elev_array, lat=lat_array, lon=lon_array,   # radian
                         doy=doy, time=int(time_str)/100, method='asce')
etr = refet_obj.etr();  eto = refet_obj.eto()
```

Formulalar `refet` kutubxonasida (alohida paket, `refet>=0.3.7`).

## 3. gridMET kunlik — `gridmet_daily_refet.py`

Joriy kodda gridMET NetCDF'dagi **tayyor** `etr`/`eto` o'zgaruvchilari o'qiladi va IMG ga yoziladi (`zw = 10`). `refet.Daily` bilan qayta hisoblash bloki izohga olingan.

## 4. Stansiya CSV (REFET rejimi) — `et_common.read_refet_instantaneous_func`

`weather_data_source = REFET` bo'lganda bitta stansiya faylidan overpass soatidagi:

| Qaytaradi | Birlik |
|---|---|
| dew point | °C |
| wind speed | m/s |
| $e_a$ | kPa |
| ETr (soatlik) | mm/h |
| ETr 24 soat | mm/d |

`localtime = acq_time + gmt_offset`. Kunlik qatorlar uchun `read_refet_daily_func`, `read_nvet_daily_func`, `read_csv_etr_daily_func`, `fixed_etr_data_func` mavjud.

## 5. Bog'liq yordamchi formulalar (`et_common`)

| Funksiya | Formula |
|---|---|
| `saturation_vapor_pressure_func(T)` | $0.6108\exp(17.27T/(T + 237.3))$ kPa, T °C |
| `air_pressure_func(z)` | $101.3((293.15 - 0.0065z)/293.15)^{5.26}$ |
| `ra_daily_func(lat, doy)` | $\frac{24}{\pi}\cdot4.92\,d_r[\omega_s\sin\varphi\sin\delta + \cos\varphi\cos\delta\sin\omega_s]$ |
| `omega_sunset_func` | $\arccos(-\tan\varphi\tan\delta)$ |
| `u_star_station_func`, `u3_func` | [04 §3](04_model2.md#3-shamol-stansiyadan-200-m-ga) |
| `doy_range_func` | Interpolyatsiya kunlari oralig'i (chekka oyda < 10 kun bo'lsa qisqartiradi) |

## 6. 🇺🇿 AQShdan tashqarida ishlatish

| Kerak | AQSh manbasi | Muqobil (global) |
|---|---|---|
| Soatlik $e_a$, $u$, ETr | NLDAS | ERA5-Land hourly → `refet.Hourly` |
| Kunlik ETr, PPT | gridMET | ERA5-Land daily / CHIRPS (PPT) |
| DEM | NED | SRTM / Copernicus GLO-30 |
| Land cover (NLCD kodlari) | NLCD | ESA WorldCover → NLCD remap (+ `zom_remap` JSON ni moslash) |
| AWC (SWB) | STATSGO2 | SoilGrids / OpenLandMap |
| Landsat | C1 L1 (to'xtatilgan) | **C2 L1** — `et_image` ni moslash kerak ([09](09_kuzatuvlar.md)) |

`weather_data_source = MANUAL` (INI'da `ea`, `wind_speed`, `etr`, `etr_24hr` sonlari) — eng tez sinov yo'li.
