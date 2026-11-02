# 03 — Surface Temperature (LST), delapsing va tall vegetation tuzatishlari

> **Manba fayl:** `surface_temperature.py` (+ `eeflux.py` dagi `_std_lapse`, `_total_lapse`, `ts_dem_latlon`)

---

## 1. Feynman tushuntirish: "Tog'dagi termometr"

Toshkentda +35°C, Chimyon cho'qqisida +20°C. Bu farq **ET** dan emas, **balandlikdan** (lapse rate ~6.5 K/km). METRIC esa issiq/sovuq piksellarni temperatura bo'yicha tanlaydi. Agar balandlikni hisobga olmasak, tog' cho'qqisidagi quruq tosh "sovuq = nam" deb noto'g'ri tanlanadi.

Yechim: **delapsing** — barcha piksellarning temperaturasini bitta "datum" balandlikka keltirish:

$$T_{s,dem} = T_s + \Gamma\,(z - z_{datum})/1000$$

Bu xuddi har xil qavatdagi odamlarning bo'yini bir poldan o'lchashga o'xshaydi.

---

## 2. LST hisoblash (legacy METRIC) — `calculate_surface_temperature`

> C2 oqimida `surface_temperature` tayyor (openet-core LST correction, qarang [01](01_preprocessing_landsat.md#5-c2-lst-correction-default-_c2_lst_correct--true)). Bu funksiya user o'zi `surface_temperature` bermaganda va eski oqimda ishlatiladi.

**Narrow-band emissivity** (Tasumi, 2003; Allen et al., 2007 Eq. 22):

$$\varepsilon_{NB} = \begin{cases} 0.97 + 0.0033\,LAI, & LAI \le 3 \\ 0.98, & LAI > 3 \\ 0.99, & NDVI < 0\ \lor\ \alpha > 0.47\ (\text{suv/qor}) \end{cases}$$

**Termal radiance:** $L_6 = DN\cdot M_L + A_L$

**Korreksiyalangan radiance** (Eq. 21):

$$R_c = \frac{L_6 - R_p}{\tau_{NB}} - (1 - \varepsilon_{NB})\,R_{sky},\quad R_p = 0.91,\ \tau_{NB}=0.866,\ R_{sky}=1.32\ \mathrm{W/m^2/sr/\mu m}$$

**Plank** (Eq. 20):

$$T_s = \frac{K_2}{\ln\!\left(\dfrac{K_1\,\varepsilon_{NB}}{R_c} + 1\right)}$$

---

## 3. Lapse rate tizimi

### 3.1 Tog'li sahnami? — `calc_mountain_toggle`

$$\text{mountain\_toggle} = (z_{max} - z_{min}) > 1000\,m$$

DEM ~480 m (16× native) masshtabda `reduceRegion(minMax)`.

### 3.2 Lapse o'zgarish balandligi — `find_elev_for_lapse_rate_change`

1. `slope > 10°` bo'lgan DEM piksellari qoldiriladi.
2. Sahna **mesh** (to'r bloklar, qarang [10](10_pixel_selection.md)) bo'yicha `intervalMean(20, 40)` — har blokda 20–40 persentil o'rtachasi.
3. Barcha bloklar o'rtachasi = `lapse_elev`.
4. Hech qanday tik qiyalik bo'lmasa → `lapse_elev = 100000 m` (ya'ni mountain lapse hech qachon ishlamaydi).

> `ee.Feature(None, {...}).toDictionary().combine({'lapse_elev': 100000}, overwrite=False)` — null qiymatga default berishning EE server-side hiylasi.

### 3.3 Ikki qismli lapse — `calculate_lapse_general`

$z$ — piksel balandligi, $z_d$ — datum, $z_L$ — lapse_elev, $\Gamma_f$ — flat, $\Gamma_m$ — mountain (K/km):

| Holat | Formula |
|---|---|
| Default | $\Delta T = (z - z_d)\,\Gamma_f/1000$ |
| $z_d < z_L < z$ | $\Delta T = (z_L - z_d)\Gamma_f/1000 + (z - z_L)\Gamma_m/1000$ |
| $z_d > z_L,\ z > z_L$ | $\Delta T = (z - z_d)\,\Gamma_m/1000$ |
| $z_d > z_L > z$ | $\Delta T = (z - z_L)\Gamma_f/1000 + (z_L - z_d)\Gamma_m/1000$ |

(Oxirgi 3 holat faqat `mountain_toggle = 1` bo'lganda.)

### 3.4 Standart va umumiy lapse — `eeflux.py`

```python
# _std_lapse
full_lapse = calculate_std_lapse(self, 6.5, self.lapse_mtn)
std_lapse  = calculate_std_lapse(self, self.lapse_flat, self.lapse_mtn)   # lapse_flat=3.0 default
std_lapse  = std_lapse.where(month.gt(10).Or(month.lt(5)), full_lapse)     # Noyabr–Aprel: 6.5

# _total_lapse
lapse = std_lapse.where(spatial_lapse_success.eq(0), full_lapse)          # spatial regressiya muvaffaqiyatsiz → 6.5
if self.spatial_delapsing:
    lapse = lapse.add(spatial_lapse)                                      # lat/lon trend qo'shiladi
```

| Parametr | Default | Izoh |
|---|---|---|
| `lapse_flat` | **3.0 K/km** | Vegetatsiya mavsumida (May–Okt) — sug'oriladigan vodiylar uchun past |
| `lapse_mtn` | **6.5 K/km** | Tog' qismi |
| Mavsumdan tashqari | 6.5 K/km | Environmental lapse rate |

> 🧠 **Nega mavsumda 3.0?** Sug'oriladigan dalalar havoni sovutadi va inversiya hosil qiladi — real gradient 6.5 dan kichik.

### 3.5 Delapsed temperaturalar

| Xususiyat | Formula | Ishlatilishi |
|---|---|---|
| `surface_temperature_dem` | $T_s + \Delta T_{std}$ | Pixel selection (statik reyting) |
| `ts_dem_latlon` | $T_s + \Delta T_{total}$ (spatial lapse bilan) | Kalibratsiya, dT |
| `ts_dem_latlon_alb_adj` | `ts_dem_latlon` + low-albedo tuzatish | $H$ hisoblash |

---

## 4. Tall vegetation LST tuzatishi — `calculate_lst_tall_vegetation_general`

### 4.1 Feynman

Bog'ni yuqoridan termal kamera bilan ko'rsak, piksel = **soyabon (canopy) + soyadagi yer + quyoshdagi yer** aralashmasi. Soyadagi yer sovuq, quyoshdagi yer issiq. Bizga **faqat barg temperaturasi** kerak (u transpiratsiyani aks ettiradi). Shuning uchun aralashmani "ajratamiz" (unmixing).

### 4.2 Formulalar

Quyosh zenit burchagi: $\theta = 90° - \text{SUN\_ELEVATION}$

**Clumping factor** ($\Omega_0 = 0.7$, $D$ = crown height/width = 3.0):

$$\Omega(\theta) = \frac{\Omega_0}{\Omega_0 + (1-\Omega_0)\exp\!\left[-2.2\,\theta_{rad}^{\,(3.8 - 0.46D)}\right]}$$

**Umumiy soya maydoni:**

$$f_{shade,tot} = \frac{1 - \exp(-0.5\,\Omega(\theta)\,LAI)}{\cos\theta}$$

**Daraxt ostidagi soya ulushi** ($z_{lf}$ = leafless fraction = 0.25, shapefactor = 2.0):

$$f_{under} = 1 - \frac{2\cdot (2.5\,LAI\cdot z_{lf})/\tan(90°-\theta)}{2.5\,LAI/D}$$

**Nadirdan ko'rinadigan vegetatsiya ulushi:**

$$f_{veg} = 1 - \exp(-0.5\,\Omega_0\,LAI)$$

**Yerdagi soya va quyoshli ulushlar:**

$$f_{sh} = \min\big(f_{shade,tot} - f_{veg}\,f_{under},\ 1 - f_{veg}\big),\qquad f_{sun} = \max(1 - f_{veg} - f_{sh},\ 0)$$

**Temperatura offsetlari:**

Ho'l termometr bug' bosimi (geometrik o'rtacha): $e_{wet} = \sqrt{e_a\cdot e^\circ(T_a)}$, $e^\circ(T) = 0.6108\exp\!\frac{17.27T}{T+237.3}$

$$T_{wb}\,[°C] = \frac{116.91 + 237.3\ln e_{wet}}{16.78 - \ln e_{wet}}$$

$$\Delta T_{shade} = \frac{T_{cold,dem} - \Gamma - (T_{wb} + 273.17)}{k_{sh}},\qquad \Delta T_{sun} = \frac{T_{hot,dem} - T_{cold,dem}}{k_{sun}},\quad k = 2.0$$

**Canopy temperaturasi (unmixing):**

$$T_c^* = \frac{T_s - f_{sh}(T_{cold} - \Delta T_{shade}) - f_{sun}(T_{cold} + \Delta T_{sun})}{f_{veg}}$$

Cheklash: $T_s - 1 \le T_c^* \le T_s + 2$

**LAI bo'yicha aralashtirish:**

$$T_c = \begin{cases} T_s, & LAI \le 1 \\ 2(LAI-1)\,T_c^* + (1 - 2(LAI-1))\,T_s, & 1 < LAI < 1.5 \\ T_c^*, & LAI \ge 1.5 \end{cases}$$

Faqat `tall_veg_id == 1` piksellarda qo'llanadi.

---

## 5. Low-albedo LST tuzatishi — `calculate_lst_tall_veg_adj_low_albedo_general`

Albedo sun'iy oshirilgani ($\Delta\alpha$, qarang [02](02_albedo_ndvi_lai.md#21-tall-vegetation-albedo-adjustment--calculate_albedo_tall_veg_adj)) uchun temperaturani ham moslashtirish kerak (aks holda energiya balansi buziladi):

$$T' = T + \Delta\alpha \cdot m \cdot (T_{hot,dem} - T_{cold,dem}),\qquad m = \frac{k}{K_{c,cold} - K_{c,hot}},\ k=2.0$$

```python
k_factor.divide(etrf_cold_pixel_dem.subtract(etrf_hot_pixel_dem))   # calculate_lst_adj_multiplier
lst.expression('b()+albedo_adj*lst_adj_multiplier*(ts_dem_hot-ts_dem_cold)', ...)
```

> Funksiya argumentlari `etrf_*_dem` deb nomlangan, lekin aslida `_kc_hot_pixels`, `_kc_cold_pixels` (ETrF) beriladi.

---

## 6. Terrain LST — `calculate_lst_terrain_general`

Quyoshga qaragan / teskari qiyaliklar uchun:

$$\phi = \begin{cases}(\psi - \psi_{sun})\pi/180, & \psi \ge \psi_{sun}\\ (360 - \psi_{sun} + \psi)\pi/180, & \psi < \psi_{sun}\end{cases},\qquad T_{terr} = T - 10\cos|\phi|$$

$slope \le 5°$ bo'lsa → tuzatish yo'q.
