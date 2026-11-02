# 12 — ETrF, kunlik ET (ET24) va Soil Water Balance

> **Manba fayllar:** `etrf_et24.py`, `soil_water_balance.py`, `eeflux.py` (`etrf`, `etrf_instant`, `eta`, `etof`, `et_fraction`, `et`)

---

## 1. Feynman tushuntirish: "Bir lahzalik foto → butun kunlik kino"

Landsat yer ustidan **soat ~10:30–11:00** da bir marta o'tadi. Bizda ET ning bitta "fotosurati" bor (mm/soat). Kunlik ET (mm/kun) kerak.

**METRIC hiylasi:** ETrF (piksel ET / beda ET) kun davomida deyarli **o'zgarmas** deb faraz qilinadi:

$$ET_{24} = ET_rF_{inst}\times ET_{r,24}$$

Bu xuddi "bu o'quvchi soat 11 da sinfdoshining 80% tezligida yozyapti — demak kun bo'yi ham 80%" deyishga o'xshaydi. Ekinlar uchun bu juda yaxshi ishlaydi (stomata quyosh bilan sinxron). Ekin bo'lmagan yerlar (cho'l, butazor) uchun esa **evaporative fraction** (EF) bilan tuzatiladi.

---

## 2. Instant ET — `calculate_et_instant` (Allen et al., 2007, Eq. 52–53)

$$LE = R_n - G - H$$

$$ET_{inst} = \frac{3600\,(R_n - G - H)}{\lambda},\qquad \lambda = (2.501 - 0.00236\,(T_s - 273.15))\times10^6\ \mathrm{J/kg}$$

Birlik: **mm/soat**.

---

## 3. Instant ETrF — `calculate_etrf` (Eq. 54)

$$ET_rF_{inst}^{raw} = \frac{ET_{inst}}{ET_{r,inst}^{cold}}$$

> ⚠️ $ET_{r,inst}$ — **cold piksel joyidagi** instant ETr (`reduceRegion(mean, cold_candidate.geometry())`) — butun sahna uchun **bitta konstanta**. Bu kalibratsiyaga to'liq mos: cold pikselda $ET = K_{c,cold}\cdot ET_r^{cold}$ deb belgilangan edi.

**Tog' radiatsiya tuzatishi** (`eeflux.etrf_instant`):

$$ET_rF_{inst} = ET_rF_{inst}^{raw}\times C_{rad},\qquad C_{rad}\le 1.5$$

($C_{rad}$ — qarang [06 §5](06_net_radiation.md#5-radiation-adjustment-coefficient--radiation_adjustment_coefficient))

`EEFluxFlat` da $C_{rad}$ yo'q.

---

## 4. Evaporative Fraction va Slob Rn24 (non-ag uchun)

### 4.1 EF — `calculate_evaporative_fraction`

$$EF = \mathrm{clamp}\!\left(\frac{R_n - G - H}{R_n - G},\ 0,\ 1\right)$$

### 4.2 Kunduzgi soatlar — `daylight_hours`

$$N = \frac{24}{\pi}\arccos\big(-\tan\varphi\,\tan(0.409\sin(2\pi J/365 - 1.39))\big)$$

### 4.3 Slob kunlik net radiation — `calculate_rn_slob`

Kunlik net longwave (de Bruin & Stricker, 1982; Slob uslubi):

$$R_{nl}^{hot} = (0.5\cdot140 + 0.5\cdot180)\,\tau_{sw,24} = 160\,\tau_{sw,24},\qquad R_{nl}^{cold} = (0.5\cdot115 + 0.5\cdot145)\,\tau_{sw,24} = 130\,\tau_{sw,24}$$

(hot/cold piksel joyidagi qiymat, W/m²). Piksel uchun chiziqli interpolyatsiya:

$$R_{nl} = \mathrm{clamp}\!\left(R_{nl}^{cold} + \frac{T_s - T_{cold}^{lap}}{T_{dry}^{lap} - T_{cold}^{lap}}(R_{nl}^{hot} - R_{nl}^{cold}),\ R_{nl}^{cold},\ R_{nl}^{hot}\right)$$

$T^{lap} = T - \Delta T_{total}$, $T_{dry}$ — ETrF=0 ekstrapolyatsiya temperaturasi ([09](09_sensible_heat_flux.md#32-dt-va-uning-chegaralari-allen-et-al-2014-eq-154156)).

**Tog' reduksiyasi:**

$$k_{mtn} = \mathrm{clamp}\!\left(\frac{R_{L\uparrow} - R_{L\downarrow}^{mtn}}{R_{L\uparrow} - R_{L\downarrow}^{flat}},\ 0.6,\ 1.0\right)$$

**Rn24** (effektiv kun og'irligi $w = 0.5$):

$$R_{n,24} = \frac{(1-\alpha')\,R_{so,24}\cdot 24}{w\cdot 24 + (1-w)N} - R_{nl}\cdot k_{mtn}$$

$R_{so,24}$ = `_daily_sw_radiation_clear_sky` ([06](06_net_radiation.md#43-calculate_daily_rso_flat-va-calculate_daily_rso)).

### 4.4 EF asosidagi ET24 — `calculate_et_ef` (Allen et al., 2014)

$$ET_{24}^{EF} = ET_{inst}\cdot\frac{N(1-w) + 24w}{R_n - G}\cdot\big(R_{n,24} - G(1-w)\big)$$

**Stress tuzatishi** (ETrF/NDVI nisbati):

$$k_s = \min\!\left(\frac{ET_rF_{inst}}{\max(NDVI, 0.2)}\cdot0.9 + 0.05,\ 1\right),\quad k_s<0 \Rightarrow 1$$

$$ET_{24}^{EF} \leftarrow \mathrm{clamp}(k_s\cdot ET_{24}^{EF},\ -3ET_{r,24},\ 3ET_{r,24})$$

---

## 5. Ochiq suv/qor uchun kunlik bug'lanish — `evap_aerodynamic`

Instant aerodinamik bug'lanish ($E_{aero}$, [09](09_sensible_heat_flux.md#4-ochiq-suvdan-aerodinamik-buglanish-allen-et-al-2014-ch-10)) kunlik masshtabga o'tkaziladi:

$$Z_{om,w} = \max(6.57\times10^{-7}u_{10}^{2.55},\ 5\times10^{-5}),\qquad r_{av} = \frac{\ln^2(10/Z_{om,w})}{k^2\,u_{10}}$$

$$E_{art,inst} = \frac{3600\rho_a(q_s(T_a) - q_a)}{r_{av,inst}},\qquad E_{art,24} = \frac{86400\rho_{a,24}(q_s(\bar T) - q_{a,24})}{r_{av,24}}$$

$$E_{24} = E_{aero}\cdot\mathrm{clamp}\!\left(\frac{E_{art,24}}{E_{art,inst}},\ 1,\ 30\right)$$

($e_s$ — Tetens Kelvin formulasi, $T<275$ K da muz varianti; $\rho_a = \frac{1000P}{1.01\cdot287\cdot T}$; kunlik $e_s = (e_s(T_{min}) + e_s(T_{max}))/2$.)

---

## 6. Yakuniy ET24 va ETrF24 — `calculate_etrf_et24`

```text
            ┌──────────── land_use ≥ 80 (Ag, wetland) ─────► ET24 = ETrF_inst × ETr24
ETrF_inst ──┤
            ├──────────── land_use < 80, quruqlik ─────────► ET24 = ETrF24_mix × ETr24
            └──────────── snow_water_flag > 0 ─────────────► ET24 = E24_aero
```

**Non-ag aralashtirish:**

1. $ET_rF_{24}^{EF} = ET_{24}^{EF}/ET_{r,24}$, lekin $|ET_rF_{24}^{EF}| \le |ET_rF_{inst}|$ (bir xil ishorada) va $[-1.99, 1.99]$.
2. Og'irlangan aralashma ($K_{cc}$ = cold piksel ETrF):

$$ET_rF_{24}^{mix} = \max(0,F)\cdot\mathrm{clamp}\!\left(\frac{F}{K_{cc}},0,1\right) + ET_rF_{24}^{EF}\cdot\left(1 - \frac{\mathrm{clamp}(F, 0, K_{cc})}{K_{cc}}\right),\quad F = ET_rF_{inst}$$

> 🧠 Ma'nosi: nam piksellarda ($F \to K_{cc}$) — oddiy ETrF; quruq piksellarda ($F \to 0$) — EF usuli. "Ikki retseptni namlik darajasiga qarab aralashtirish".

3. $ET_rF_{24} = ET_{24}/ET_{r,24}$; **qor**: $ET_rF_{24} \le 0.5$.

Chiqish: `etrf`, `eta` bandlari.

---

## 7. EEFlux chiqish xususiyatlari

| Xususiyat | Formula | Cheklov |
|---|---|---|
| `etrf` | `calculate_etrf_et24().select('etrf')` | `.max(0)` |
| `etrf_export` | `etrf` | [0, 2] |
| `etrf_for_stats` | cheklovsiz | — |
| `eta` | $ET_{24}$ (mm/d) | — |
| `etof` | $ET_{24}/ET_{o,24}$ | — |
| `instant_reference_etr` | hourly ETr × 0.85 | — |
| **`et_fraction`** (OpenET) | $\min(ET_rF, 2)$; agar ETrF > 1.3 ∧ LU ≠ 11 → 1.3; $\times ET_{r,inst}/ET_{o,inst}$ | ≥ 0 |
| **`et_reference`** | tashqi ETo manba ([04](04_weather_reference_et.md#8-openet-eksporti-uchun-tashqi-reference-et-et_reference)) | — |
| **`et`** | `et_fraction × et_reference` | ≥ 0 |

> 🧠 **EToF konversiyasi:** OpenET ansambl modeli grass reference (ETo) bilan ishlaydi. $EToF = ETrF\cdot\frac{ET_r}{ET_o}$ — overpass vaqtidagi soatlik nisbat bilan.

---

## 8. Soil Water Balance — `soil_water_balance.py`

### 8.1 Maqsad

Hot pikselda tuproq to'liq quruq bo'lmasligi mumkin (yaqinda yomg'ir). FAO-56 + "skin layer" (Allen, 2011) modeli bilan **bare soil evaporation coefficient** $K_e$ hisoblanadi. U `daily_evaporation_bare_soil` → **static** hot piksel ETrF da ishlatiladi ([10](10_pixel_selection.md#53-hot-static--calculate_hot_pixel_etrf_static)).

### 8.2 Kirish — `daily_precip_etr`

10 kunlik seriya: `daily_precipitation`, `daily_reference_etr` + **ertangi kun yog'ini** (`precip_next`, vaqt −1 kun siljitilgan) — `ee.Join.inner` bilan birlashtiriladi.

### 8.3 Tuproq parametrlari

| Belgi | Formula | Ma'no |
|---|---|---|
| $\theta_{FC}, \theta_{WP}$ | STATSGO / global GSD | m³/m³ |
| $Z_e$ | 0.10 m | Bug'lanish qatlami qalinligi |
| TEW | $1000(\theta_{FC} - 0.5\theta_{WP})Z_e$ | Total evaporable water, mm (FAO-56 Eq. 73) |
| REW | $\min(0.8 + 54.4(\theta_{FC} - \theta_{WP}),\ TEW)$ | Readily evaporable, mm |
| $K_{e,max}$ | 1.0 | ETr bazasida |
| $f_P$ | 0.5 | Yog'inning "bugungi" ulushi |
| $C_0, C_1$ | 0.8, $2(1-C_0) = 0.4$ | Skin layer samaradorligi |

**Boshlang'ich holat:** quruq (`IWC = 1`) → $D_e = TEW$, $D_{REW} = \min(REW, TEW)$.

### 8.4 Kunlik iteratsiya (Allen, 2011)

$$c_{eff} = \min\!\left(C_0 + C_1\left(1 - \frac{D_e}{TEW}\right),\ 1\right)\qquad(\text{Eq. 15})$$

$$f_t = \mathrm{clamp}\!\left(\frac{REW - D_{REW}^{prev}}{K_{e,max}\,ET_r},0,1\right)\qquad(\text{Eq. 12 — stage 1 ulushi})$$

$$K_r = \mathrm{clamp}\!\left(\frac{TEW - D_e^{prev}}{TEW - REW},0,1\right)\qquad(\text{FAO-56 Eq. 74})$$

$$K_e = \big(f_t + (1 - f_t)K_r\big)K_{e,max}\qquad(\text{Eq. 13b})$$

$$E_s = K_e\cdot ET_r$$

$$P^* = f_P\,P_{next} + (1-f_P)\,P_{today}$$

$$D_e = \mathrm{clamp}(D_e^{prev} - P^* + E_s,\ 0,\ TEW)\qquad(\text{FAO-56 Eq. 77})$$

$$D_{REW} = \mathrm{clamp}(D_{REW}^{prev} - c_{eff}P^* + E_s,\ 0,\ REW)\qquad(\text{Eq. 14})$$

Oxirgi kun (overpass) $K_e$ → `daily_evaporation_bare_soil`.

> 🐛 `automated_pixel_selection.get_soil_moisture_rating` `daily_precip_etr(self, spinning_days)` ni 2 argument bilan chaqiradi, funksiya esa 1 ta oladi → chaqirilsa `TypeError`. Hozircha hech qayerda ishlatilmaydi.

---

## 9. Manual stretch — `stretch.py`

Foydalanuvchi qo'lda ETrF ni "cho'zishi" uchun:

$$ET_rF' = ET_rF + Adj_{Low}(1 - ET_rF) + Adj_{High}\cdot ET_rF$$

$$ET_a' = ET_rF'\cdot ET_{r,24},\qquad EToF' = ET_a'/ET_{o,24}$$
