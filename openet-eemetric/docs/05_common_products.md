# 05 — Common products: DEM, quyosh geometriyasi, land use, shamol u200, tuproq

> **Manba fayl:** `common_products.py`

Bu modul — "asboblar qutisi". Boshqa barcha modullar shu yerdagi yordamchi kattaliklardan foydalanadi.

---

## 1. Quyosh kuni (Solar day) — `get_solar_day_start_end`

### Feynman
UTC bo'yicha "kun" Toshkent uchun soat 05:00 da boshlanadi — bu fizik jihatdan noto'g'ri. Kunlik ETr **mahalliy quyosh kuni** (yarim tundan yarim tungacha, quyosh vaqtida) bo'yicha olinishi kerak.

### Formula (ASCE Eq. 57–58)

$$b = \frac{2\pi(J - 81)}{364},\quad S_c = 0.1645\sin 2b - 0.1255\cos b - 0.025\sin b\ [\text{soat}]$$

$$\Delta t = \frac{12\,\lambda_{rad}}{\pi} + S_c \qquad (\text{UTC dan quyosh vaqtigacha farq, soat})$$

```python
new_date = date.advance(delta, 'hour')                         # quyosh vaqti
start = new_date.update(hour=0, minute=0, second=0).advance(-delta, 'hour')   # → UTC ga qaytarish
end   = start + 1 day
```

$\lambda$ — sahna **centroid** uzunligi (`geometry().centroid(30)`).

> Misol: Toshkent λ ≈ 69.3° → Δt ≈ 4.6 soat. Quyosh kuni UTC 19:24 (oldingi kun) dan boshlanadi.

**Mahalliy quyosh vaqti** (`calculate_solar_time`): $t_{solar} = t_{UTC} + \Delta t$ (piksel uzunligi bilan).

---

## 2. Quyosh tushish burchagi (Solar incidence)

### 2.1 Tekis yuza — `calculate_cos_theta_flat` (Allen et al., 2007, Eq. 8)

$$\delta = 0.409\sin\!\left(\tfrac{2\pi}{365}J - 1.39\right),\qquad \omega = \frac{\pi}{12}(t_{solar} - 12)$$

$$\cos\theta_{hor} = \sin\delta\sin\varphi + \cos\delta\cos\varphi\cos\omega$$

`ee.Image.pixelLonLat()` → **har piksel uchun o'z lat/lon** (METRIC original sahna markazini ishlatadi).

### 2.2 Kunlik o'rtacha — `calculate_cos_theta_flat_daily`

$$\cos\theta_{24} = \sin\big(\max(0.85 + 0.3\varphi\sin(\tfrac{2\pi}{365}J - 1.39) - 0.42\varphi^2,\ 0)\big)$$

### 2.3 Tog'li relyef — `calculate_cos_theta_mountain` (Duffie & Beckman)

$s$ — slope, $\gamma = aspect - 180°$ (janubdan o'lchanadigan azimut):

$$\begin{aligned}\cos\theta_{rel} =\ & \sin\delta\sin\varphi\cos s - \sin\delta\cos\varphi\sin s\cos\gamma \\ &+ \cos\delta\cos\varphi\cos s\cos\omega + \cos\delta\sin\varphi\sin s\cos\gamma\cos\omega \\ &+ \cos\delta\sin\gamma\sin s\sin\omega\end{aligned}$$

$$\cos\theta_{rel} \leftarrow \max(\cos\theta_{rel},\ 0.1),\qquad \cos\theta_{mtn} = \frac{\cos\theta_{rel}}{\cos s}$$

> 💡 `/cos(s)` — chunki piksel gorizontal proyeksiyada o'lchanadi, lekin qiya yuzaning haqiqiy maydoni $1/\cos s$ marta katta. Minimal 0.1 — soya qiyaliklarida nolga bo'linishning oldini oladi.

---

## 3. Atmosfera kattaliklari

| Funksiya | Formula | Birlik |
|---|---|---|
| `calculate_air_pressure(dem)` | $P = 101.3\left(\frac{293.15 - 0.0065z}{293.15}\right)^{5.26}$ | kPa |
| `calculate_ea` | $e_a = \dfrac{P\,q}{0.622 + 0.378q}$ (Ross & Elliott, 1996) | kPa |
| `calculate_relative_humidity` | $RH = 100\,e_a / e^\circ(T_s)$ | % |

> ⚠️ `calculate_relative_humidity` da $e^\circ$ **yuza temperaturasi** ($T_s$, Kelvin!) bilan hisoblanadi: `0.6108*exp(17.27*b()/(b()+237.3))` ga Kelvin berilsa, qiymat juda katta → RH juda kichik. Bu RH faqat kalibratsiya "kandidat" xususiyati sifatida saqlanadi (`rh` — `_rh_cold_pixels`), fizik hisobga ta'siri yo'q.

---

## 4. DEM va relyef

### 4.1 `calculate_dem` — global DEM tanlash

| DEM | Qamrov (lat) | Rezolyutsiya |
|---|---|---|
| `USGS/SRTMGL1_003` | −60° … 60° | 30 m |
| `USGS/GMTED2010_FULL` (`be75`) | −56° … 90° | 7.5″ (~225 m) |
| `USGS/GTOPO30` | global | 30″ (~1 km) |

```python
dem = dem_collection.filter(ee.Filter.contains(leftField='footprint', rightValue=footprint)).first()
return dem.clip(footprint.buffer(20000))     # 20 km bufer
```

Sahna footprint'ini **to'liq qamragan** birinchi DEM tanlanadi (ustuvorlik: SRTM → GMTED → GTOPO).

> 🧠 **Nega 20 km bufer?** Footprint bo'yicha qattiq clip qilinsa, chekkada CIMIS piksellari qisman masklanib gridMET bilan aralashadi. Bufer — "xavfsizlik zonasi".

### 4.2 Slope / Aspect

```python
calculate_slope  = ee.Terrain.slope(self.dem)    # ⚠️ docstring "percent" deydi, aslida GRADUS
calculate_aspect = ee.Terrain.aspect(self.dem)   # gradus, shimoldan soat yo'nalishida
```

### 4.3 Datum — `calculate_datum`

$$z_{datum} = \mathrm{int}\big(\overline{z}_{scene}\big)$$

DEM ~480 m masshtabda (16× native) o'rtacha. **Butun songa** (`.int()`) aylantiriladi.

### 4.4 Relyef statistikalari

| Funksiya | Formula | Default radius |
|---|---|---|
| `calculate_elevation_std` | $\sigma_z$ = `reduceNeighborhood(stdDev, circle)` | 1500 m |
| `calculate_relative_elevation` | $RE = \mathrm{clamp}\!\left(\frac{z - z_{min}}{z_{max} - z_{min}},0,1\right)$ | 1500 m |
| `filter_std_elev_product` | Oldindan hisoblangan asset: `projects/openet/eemetric/elevation/stddev` | — |
| `filter_rel_elev_product` | `projects/openet/eemetric/elevation/relative` | — |

> ⚠️ **O'zbekiston uchun:** `projects/openet/eemetric/elevation/*` assetlari AQSh hududi uchun. Tashqarida `mosaic()` bo'sh tasvir → `_std_elev` / `_rel_elev` masklangan. `calculate_elevation_std/relative_elevation` funksiyalari bilan o'zingiz hisoblashingiz mumkin.

---

## 5. Land use (NLCD legendasiga keltirish)

### 5.1 Ierarxiya — `calculate_land_use_combined`

```text
ee.Image(11)  (default = suv)
  └─ .where(MODIS MCD12Q1 2013 — Arktika: 0→11, 15→12, boshqa→11)
       └─ .where(ESA WorldCover v100 → NLCD)
            └─ .where(USA: Annual NLCD + OpenET crop type (CDL))
```

### 5.2 ESA WorldCover → NLCD

| ESA | Klass | → NLCD |
|---|---|---|
| 10 | Tree cover | 43 |
| 20 | Shrubland | 52 |
| 30 | Grassland | 71 |
| 40 | **Cropland** | **82** |
| 50 | Built-up | 23 |
| 60 | Bare | 31 |
| 70 | Snow/ice | 12 |
| 80 | Water | 11 |
| 90 | Herbaceous wetland | 95 |
| 100 | Moss/lichen | 73 |

> 🌍 **O'zbekiston uchun asosiy manba** — ESA WorldCover 2020. Paxta/bug'doy maydonlari → 82 ("cultivated crops").

### 5.3 USA: Annual NLCD + CDL — `merge_nlcd_crop_type_layers`

- NLCD yili Landsat yiliga eng yaqin mavjud yilga clamp qilinadi.
- Crop type (CDL asosida) joriy yil uchun bo'lsa → **o'tgan yil** olinadi.
- CDL topilmasa → NLCD (server-side "switch" `FeatureCollection.filter(gt('crop_type_images', 0))` hiylasi).
- CDL ekin klasslari (< 111, ba'zi istisnolar bilan, yoki > 195) → **81**.
- **Tall crops** (bog'/tokzor) CDL kodlari: `66–72, 74–78, 204, 210–212, 217, 218, 220, 223` → `tall_crops_flag = 1`.
- **Grapes** (69, 78) → `grapes_mask = 1` (Perrier Zom ishlatilmaydi).
- Makkajo'xori, popcorn, shakarqamish, xmel, uzum (CDL 1, 13, 45, 56, 69, 78) → **86** (Zom uchun maxsus LAI multiplikator).
- Yo'llar/developed (NLCD 21–24) har doim NLCD dan.

### 5.4 Mode versiya — `calculate_land_use_combined_mode`

Pixel selection uchun **120 m** mode (82→81 birlashtiriladi), `reduceResolution(mode, maxPixels=64)` + Albers CONUS transform `[120, 0, -2493045, 0, -120, 3310005]`.

> Docstring "300 m" deydi, kod esa **120 m**.

---

## 6. Bulut maskasi (simpleCloudScore + BQA) — `calculate_cloud_mask`

Pixel selection'da ishlatiladi (production maska emas!):

| Komponent | Shart |
|---|---|
| Score mask | `simple_cloud_score ≥ 35` |
| Permanent | `score ≥ 20` yoki score/BQA mask |
| Buffer | `fastDistanceTransform(5).sqrt() ≤ 5` (5 px ≈ 150 m) |

Natija: buferlangan maska, ustiga "permanent" (qiymat 2) yoziladi.

Legacy `landsat_fmask(qa)`: bit 5–6 ≥ 2 (cloud) yoki bit 7–8 ≥ 3 (shadow) — C1 BQA uchun.

---

## 7. 200 m shamol — `calculate_u200` (Allen et al., 2007, Eq. 41)

### Feynman
Yer yuzasida shamol daraxt, bino bilan "ishqalanadi". 200 m balandlikda (blending height) esa shamol **yuza turidan mustaqil** — butun sahna uchun bitta qiymat. METRIC shu "erkin" shamoldan pastga, har piksel uchun o'z $Z_{om}$ bilan logarifmik profilni qayta quradi.

$$u_* = \frac{k\,u_{10}}{\ln(z_w/Z_{om})},\qquad u_{200} = \frac{u_*}{k}\ln\frac{200}{Z_{om}}\quad\Rightarrow\quad u_{200} = u_{10}\frac{\ln(200/Z_{om})}{\ln(10/Z_{om})}$$

$k = 0.41$ (von Kármán), $z_w = 10$ m, $Z_{om}$ = `aerodynamic_roughness_nonwater`.

```python
wind_scale = self.scale.multiply(8)       # scale = 4×30 = 120 m → 960 m
u200 = u200.reduceRegion(ee.Reducer.mean(), image_raw.geometry(), scale=wind_scale).toImage().float()
```

> ⚠️ **Muhim:** $u_{200}$ — **butun sahna bo'yicha bitta o'rtacha son** (konstanta tasvir).

| Xususiyat | Qiymat |
|---|---|
| `_wind_speed_200_aero` | o'rtacha $u_{200}$ (cheklovsiz) — suv Zom va aerodinamik bug'lanish uchun |
| `_wind_speed_200` | $\max(u_{200},\ 5.0)$ — H uchun (izoh "4 m/s" deydi, kod **5.0**) |
| `_wind_speed_200_combined` | ikkalasi: `aero_u200`, `u200` bandlari |

---

## 8. Tog' shamoli tuzatishi — `calculate_u200_adj`

$\sigma_z$ (SDE) — balandlik std, $RE$ (RE3) — nisbiy balandlik, $\psi$ — aspect, $\psi_w$ — shamol yo'nalishi.

**Shamol yo'nalishi** (`calculate_wind_aspect`, "qayerdan esadi"):

$$\psi_w = \mathrm{atan2}(-v, -u)\cdot\frac{180}{\pi},\quad \psi_w < 0 \Rightarrow \psi_w + 360$$

**Leeward (shamolga teskari tomon) reduksiyasi:** agar $slope > 5° \land \sigma_z > 30 \land 0.1 < RE < 0.95$:

$$w_r = \sin^{1.5}(s)\cdot|\cos(\psi - \psi_w)|\cdot\cos(\psi - \psi_w)$$

**Cho'qqi kuchaytirishi** ($C_w$ = `wind_adj` = **0.5**):

$$u' = \begin{cases} u_{200}, & \sigma_z \le 30\ \lor\ \text{NLCD }81/82 \\ u_{200}\cdot\max\!\left(1 + C_w\,RE\frac{\sigma_z - 30}{20},\ 1\right), & 30 < \sigma_z \le 50 \\ u_{200}(1 + C_w\,RE), & \sigma_z > 50\end{cases}$$

**Leeward kamaytirish** ($C_l$ = `leeward_adj` = **1.0**):

$$u'' = \frac{u'}{1 - 4\,C_l\,\min(w_r,0)}$$

> 🐛 **Diqqat:** $\min(w_r, 0) \le 0$ → maxraj $\ge 1$ → $u'' \le u'$. Ya'ni shamol teskari tomonda **kamayadi** — to'g'ri. Ekin maydonlarida (81/82) tuzatish bekor qilinadi.

---

## 9. Emissivity va sifat maskasi

**Broadband emissivity** (`calculate_broad_band_emissivity`, Allen et al., 2007, Eq. 17):

$$\varepsilon_0 = \begin{cases} 0.95 + 0.01\,LAI, & LAI \le 3\\ 0.98, & LAI > 3\\ 0.985, & NDVI < 0\ \lor\ \alpha > 0.47\end{cases}$$

**Quality mask** (`calculate_quality_mask`): `cloud ∨ (ETrF > 1.3 ∧ NLCD ≠ 11)` → 0.

---

## 10. Tuproq gidravlik xususiyatlari

| Funksiya | Asosiy (USA) | Fallback (global) |
|---|---|---|
| `calculate_soil_wilting_point` | `projects/eeflux/soils/gsmsoil_mu_a_wp_10cm_albers_100` ÷ 100 | `GSD_WP_depth_0-9cm-aggregated` |
| `calculate_soil_field_capacity` | `projects/eeflux/soils/gsmsoil_mu_a_fc_10cm_albers_100` ÷ 100 | `GSD_FC_depth_0-9cm-aggregated` |

Gap-filling: `global.where(usa.gte(0), usa)` — STATSGO bor joyda u, yo'q joyda global.

---

## 11. CRS eslatmalari

| Joy | CRS |
|---|---|
| Quyosh geometriyasi | `ee.Image.pixelLonLat()` → har piksel WGS84 lat/lon (radian) |
| DEM footprint'lar | EPSG:4326, `geodesic=False` |
| NLCD mode | NLCD native Albers (WKT) 120 m |
| Masshtab | `nominalScale()` — DEM native (~30.9 m), ×16 = ~494 m |
