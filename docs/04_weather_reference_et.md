# 04 — Meteorologik ma'lumotlar va ASCE Reference ET

> **Manba fayllar:** `weather.py`, `asce_et_reference_products.py`, `eeflux.py` (`instant_reference_etr`, `daily_reference_etr`, `instant_wind_speed`, ...)

---

## 1. Feynman tushuntirish: "Etalon dala"

METRIC ET ni to'g'ridan-to'g'ri o'lchamaydi. U har bir pikselni **etalon dala** bilan solishtiradi: "Agar bu yerda yaxshi sug'orilgan, 50 sm bo'yli **beda (alfalfa)** o'sganida, u qancha suv bug'latardi?" — bu **ETr** (tall reference). Keyin piksel uchun nisbat topiladi:

$$ET_a = ET_rF \times ET_r$$

ETrF — "bu piksel etalon daladan necha foiz suv sarflaydi". Shuning uchun ob-havo (havo harorati, namlik, shamol, radiatsiya) ma'lumotlari aniq bo'lishi juda muhim.

---

## 2. Ma'lumot manbalari

| Manba | EE ID | Vaqt qadami | Ishlatilishi |
|---|---|---|---|
| **NLDAS-2** | `NASA/NLDAS/FORA0125_H002` | 1 soat, 0.125° | Overpass (instant) ob-havo — CONUS |
| **CFSv2** | `NOAA/CFSV2/FOR6H` | 6 soat, ~0.2° | Global fallback (`conus_only=False`) |
| **gridMET** | `IDAHO_EPSCOR/GRIDMET` | kunlik, 4 km | Kunlik ob-havo, ETr/ETo — CONUS |
| **Spatial CIMIS** | `projects/climate-engine/cimis/daily` | kunlik, 2 km | Kaliforniya (1999+) — eng yuqori ustuvorlik |

> 🌍 **O'zbekiston uchun muhim:** default `conus_only=True` → faqat NLDAS + gridMET ishlatiladi. AQShdan tashqarida bular **NoData** beradi! Global ishlash uchun `conus_only=False` (CFSv2 fallback) yoki `daily_weather_series` va `instant_*` ni o'zingiz (masalan ERA5-Land) berishingiz kerak. `EEFluxFlat` klassi esa majburan `conus_only=False`.

---

## 3. Overpass (instant) ob-havo

### 3.1 Vaqt bo'yicha chiziqli interpolyatsiya — `weather_interpolation`

```python
weather_filter = ee.Filter.maxDifference(12*3600*1000, 'system:time_start', None, 'system:time_start', None)
# Join.saveBest → Landsat vaqtidan oldingi (prev) va keyingi (next) eng yaqin tasvir
```

$$r = \frac{t_{scene} - t_{prev}}{t_{next} - t_{prev}},\qquad W(t_{scene}) = W_{prev} + r\,(W_{next} - W_{prev})$$

Natija `resample('bilinear')` bilan fazoviy silliqlanadi.

### 3.2 Kompozit — `calculate_overpass_global_weather`

```python
nldas = nldas.updateMask(nldas.mask().eq(1))      # qisman masklangan piksellarni olib tashlash
# conus_only=True → faqat NLDAS
# conus_only=False → CFSv2.where(NLDAS mavjud, NLDAS)
```

| Chiqish band | Birlik | Cheklov |
|---|---|---|
| `instant_air_temperature` | °C | — |
| `instant_specific_humidity` | kg/kg | ≥ 0 |
| `instant_sw_radiation` | W/m² | ≥ 0 |
| `instant_wind_speed` | m/s | ≥ 0 |
| `wind_speed_u`, `wind_speed_v` | m/s | ≥ 0 (!) |

> 🐛 **Kod kuzatuvi:** `wind_speed_u/v` komponentlari `.max(0.0)` bilan cheklangan. Komponentlar ishorali (g'arbiy/janubiy shamol manfiy) bo'lishi kerak. Natijada `instant_wind_speed = sqrt(u²+v²)` (eeflux.py:376) **kamaytirilgan** bo'lishi mumkin (manfiy komponent 0 ga aylanadi). Bu instant ETr ga ta'sir qiladi. Tadqiqotda e'tibor bering.

Shamol tezligi: $u = \sqrt{u_x^2 + u_y^2}$

---

## 4. Kunlik ob-havo seriyasi (10 kunlik "spin-up")

### 4.1 `calculate_daily_weather_series_composite`

Overpass sanasidan **10 kun oldin** + overpass kuni (jami 11 ta tasvir). Bu seriya **soil water balance** uchun kerak (qarang [12](12_etrf_et24_soil_water_balance.md)).

Sahna markazining uzunligi (radian) olinadi → **quyosh kuni** chegaralarini hisoblash uchun (`get_solar_day_start_end`).

### 4.2 Kompozit ustuvorlik — `calculate_daily_weather_composite`

```text
conus_only=True :   gridMET  ──►  CIMIS (agar mavjud)
conus_only=False:   CFSv2 ──► gridMET (agar ≥0) ──► CIMIS (agar mavjud)
```

"Mavjudlik" testlari: `tmin ≥ -274 K`, `sph ≥ -1`, ... CIMIS yo'q bo'lsa qiymat **-300** sentinel bilan to'ldiriladi → test False bo'ladi.

### 4.3 CIMIS konversiyalari

| O'zgaruvchi | Konversiya |
|---|---|
| Tmin/Tmax | °C + 273.15 → K |
| Rs | MJ/m²/d × 11.574 → W/m² |
| U2 → U10 | $u_{10} = u_2\cdot \ln(67.8\cdot 10 - 5.42)/4.87$ |
| Tdew → q | $e_a = 0.6108\exp\frac{17.27T_d}{T_d+237.3}$, $q = \dfrac{0.622 e_a}{P - 0.378 e_a}$ |

### 4.4 CFSv2 kunlik

6 soatlik tasvirlarning `system:time_start` i davr **markaziga** suriladi (o'rtacha/yig'indi qiymatlar uchun):

| Band | Agregatsiya |
|---|---|
| Tmax | max |
| Tmin | min |
| q | mean |
| Rs | mean |
| u, v | mean → $\sqrt{u^2+v^2}$ |
| Precip | $\sum \text{rate}\times 21600$ s → mm |

### 4.5 Kunlik chiqish bandlari

`daily_air_temperature_min/max` (K), `daily_specific_humidity`, `daily_sw_radiation` (W/m²), `daily_wind_speed` (10 m), `daily_precipitation` (mm), **`daily_reference_etr`**, **`daily_reference_eto`** (mm/d).

---

## 5. ASCE Standardized Daily Reference ET — `asce_daily_et`

Walter et al. (2005), ASCE-EWRI.

### 5.1 Yordamchi kattaliklar

| Kattalik | Formula | ASCE Eq. |
|---|---|---|
| Bosim | $P = 101.3\left(\frac{293.15-0.0065z}{293.15}\right)^{5.26}$ kPa | 34 |
| Psixrometrik konst. | $\gamma = 0.000665\,P$ | 35 |
| O'rtacha T | $T = (T_{min}+T_{max})/2 - 273.15$ | — |
| Shamol 2 m | $u_2 = u_z\,\dfrac{4.87}{\ln(67.8 z_w - 5.42)}$, $z_w = 10$ m | 67 |
| To'yingan bosim | $e^\circ(T) = 0.6108\exp\frac{17.27T}{T+237.3}$, $e_s = \frac{e^\circ(T_{min}) + e^\circ(T_{max})}{2}$ | 37 |
| Qiyalik | $\Delta = \dfrac{4098\,e^\circ(T)}{(T+237.3)^2}$ | 36 |
| Haqiqiy bosim (q dan) | $e_a = \dfrac{P}{0.622/q + 0.378}$ | Ross & Elliott (1996) |

### 5.2 Radiatsiya (kunlik)

$$d_r = 1 + 0.033\cos\!\left(\tfrac{2\pi}{365}J\right),\quad \delta = 0.409\sin\!\left(\tfrac{2\pi}{365}J - 1.39\right),\quad \omega_s = \arccos(-\tan\varphi\tan\delta)$$

$$R_a = \frac{24}{\pi}\,G_{sc}\,d_r\,[\omega_s\sin\varphi\sin\delta + \cos\varphi\cos\delta\sin\omega_s],\quad G_{sc}=4.92\ \mathrm{MJ\,m^{-2}h^{-1}}$$

$$R_{so} = (0.75 + 2\times 10^{-5}z)\,R_a$$

$$f_{cd} = \mathrm{clamp}\!\left(1.35\frac{R_s}{R_{so}} - 0.35,\ 0.05,\ 1\right)$$

$$R_{ns} = (1 - 0.23)\,R_s,\qquad R_{nl} = \sigma f_{cd}(0.34 - 0.14\sqrt{e_a})\frac{T_{max,K}^4 + T_{min,K}^4}{2},\ \sigma = 4.901\times10^{-9}$$

$$R_n = R_{ns} - R_{nl}$$

$R_s$ W/m² → MJ/m²/d: ×0.0864.

### 5.3 Penman–Monteith (standartlashtirilgan, Eq. 1)

$$ET_{ref} = \frac{0.408\,\Delta\,R_n + \gamma\dfrac{C_n}{T+273}u_2(e_s - e_a)}{\Delta + \gamma(1 + C_d u_2)}$$

| Reference | $C_n$ | $C_d$ | Band nomi |
|---|---|---|---|
| Tall (alfalfa, ETr) | 1600 | 0.38 | `daily_etr` |
| Short (grass, ETo) | 900 | 0.34 | `daily_eto` |

> Kunlik formulada $G = 0$.

### 5.4 ⚠️ ETr reduction multiplier = 0.85

```python
etr_reduction_multiplier = 0.85  # 15% reduction in daily ETr except CIMIS.
gridmet_etr = asce_daily_et(...).multiply(0.85).max(0.001)
cimis_etr   = asce_daily_et(...).max(0.001)          # CIMIS — reduksiyasiz
gridmet_eto = asce_daily_et(...).max(0.001)          # ETo — reduksiyasiz!
```

> 🧠 **Nega?** gridMET kabi gridded ma'lumotlar sug'orilmagan stansiyalar asosida → havo **quruqroq va issiqroq** ("aridity bias"). Real sug'oriladigan dala ustida ETr ~15% kam. CIMIS stansiyalari esa sug'oriladigan maysazorda — tuzatish kerak emas. **ETo ga reduksiya qo'llanmaydi** — bu ETrF → EToF konversiyasida e'tiborga olinishi kerak.

---

## 6. ASCE Hourly (instant) Reference ET — `asce_hourly_et`

### 6.1 Quyosh geometriyasi

$$\delta = 0.40928\sin\!\left(\tfrac{2\pi}{365}J - 1.39435\right)$$

Mavsumiy tuzatish (equation of time): $b = \frac{2\pi(J-81)}{364}$, $S_c = 0.1645\sin 2b - 0.1255\cos b - 0.025\sin b$

Quyosh soat burchagi (soat $t$ — UTC, `getFraction('day')*24`):

$$\omega = \frac{\pi}{12}\left[\left(t + \frac{12\lambda}{\pi} + S_c\right) - 12\right]$$

> Kodda $L_z$ (vaqt zonasi meridiani) yo'q, chunki $t$ UTC va $\lambda$ radian — $12\lambda/\pi$ = uzunlik soatlarda. Bu ekvivalent.

$\omega_1 = \omega - \pi/24$, $\omega_2 = \omega + \pi/24$, ikkalasi $[-\omega_s, \omega_s]$ ga clamp.

$$R_a = \frac{12}{\pi}G_{sc}\,d_r\,[(\omega_2-\omega_1)\sin\varphi\sin\delta + \cos\varphi\cos\delta(\sin\omega_2 - \sin\omega_1)]$$

### 6.2 Clear-sky (to'liq ASCE Appendix D)

$$\sin\beta = \sin\varphi\sin\delta + \cos\varphi\cos\delta\cos\omega$$

$$W = 0.14\,e_a P + 2.1$$

$$K_B = 0.98\exp\!\left[\frac{-0.00146P}{K_t\sin\beta} - 0.075\left(\frac{W}{\sin\beta}\right)^{0.4}\right],\quad \sin\beta \ge 0.01$$

$$K_D = \min(0.35 - 0.36K_B,\ 0.18 + 0.82K_B),\qquad R_{so} = R_a(K_B + K_D)$$

### 6.3 Net radiatsiya (soatlik)

Overpass vaqtida $R_s/R_{so} = 1$ deb qabul qilinadi → $f_{cd} = 1$:

$$R_{nl} = 2.042\times10^{-10}f_{cd}(0.34 - 0.14\sqrt{e_a})(T + 273.16)^4,\qquad R_n = 0.77R_s - R_{nl}$$

$R_s$: W/m² × 0.0036 → MJ/m²/h.

### 6.4 Hourly PM

| Ref | $C_n$ | $C_d$ (kun) | $G/R_n$ (kun) | $C_d$ (tun) | $G/R_n$ (tun) |
|---|---|---|---|---|---|
| ETr (alfalfa) | 66 | 0.25 | 0.04 | 1.70 | 0.2 |
| ETo (grass) | 37 | 0.24 | 0.1 | 0.96 | 0.5 |

Tun: $R_n < 0$.

$$ET_{hr} = \frac{0.408\Delta(R_n - G) + \gamma\dfrac{C_n}{T+273}u_2(e^\circ(T) - e_a)}{\Delta + \gamma(1 + C_d u_2)}$$

### 6.5 `instant_refet` va eeflux wrapperlari

```python
InstETr = asce_hourly_et(
    self.instant_air_temperature,          # °C (NLDAS)
    self.instant_specific_humidity,
    self.instant_incoming_sw_clear_sky,    # ⚠️ CLEAR-SKY Rs, haqiqiy Rs emas!
    self.instant_wind_speed,
    self.dem, zw=10, doyW, hourW, reference_crop).max(0.001)

# eeflux.py
instant_reference_etr = instant_refet(self).select('hourly_etr').multiply(0.85)
instant_reference_eto = instant_refet(self, 'grass').select('hourly_eto').multiply(0.85)
```

> 🧠 **Clear-sky Rs nima uchun?** Bulutli piksellar baribir maskalanadi; toza osmon pikselida haqiqiy Rs ≈ Rso. Bu NLDAS radiatsiyasidagi xatolarni chetlab o'tadi.

> Instant ETr **va** ETo ikkalasi ×0.85 — shuning uchun `et_fraction` dagi `ETr_inst/ETo_inst` nisbatida 0.85 qisqaradi.

---

## 7. Kunlik qiymatlarni overpass kuniga moslash

```python
solar_day_start, solar_day_end = common_products.calculate_scene_solar_day_start_end(self)
daily_reference_etr = daily_reference_etr_series.filterDate(solar_day_start, solar_day_end).first()
```

**Quyosh kuni** (solar day) — UTC kuni emas, balki sahna uzunligiga qarab siljigan 24 soat (qarang [05](05_common_products.md)).

---

## 8. OpenET eksporti uchun tashqi reference ET (`et_reference`)

```python
Image(..., et_reference_source='IDAHO_EPSCOR/GRIDMET', et_reference_band='etr',
      et_reference_factor=0.85, et_reference_resample='bilinear')
```

| `et_reference_source` turi | Xatti-harakat |
|---|---|
| son (`float`) | `ee.Image.constant(x)` |
| `str` | ImageCollection ID; **0 UTC** sanadan +1 kun filtr |
| boshqa | `ValueError` |

`et_reference_factor` ko'paytiriladi; `bilinear`/`bicubic` resample ixtiyoriy.
