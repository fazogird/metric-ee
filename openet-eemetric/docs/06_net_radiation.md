# 06 — Net Radiation ($R_n$) va clear-sky radiatsiya

> **Manba fayl:** `net_radiation.py`

---

## 1. Feynman tushuntirish: "Energiya hamyoni"

Yer yuzasi — hamyon. Kirim:
- **Qisqa to'lqin** (quyosh): $R_{s\downarrow}$, lekin bir qismi qaytadi ($\alpha R_{s\downarrow}$).
- **Uzun to'lqin** (atmosfera issiqligi): $R_{L\downarrow}$.

Chiqim:
- **Yerning o'z issiqlik nurlanishi**: $R_{L\uparrow} = \varepsilon_0\sigma T_s^4$.
- Atmosfera nurining qaytgan qismi: $(1-\varepsilon_0)R_{L\downarrow}$.

Qolgan "sof pul" — $R_n$ — keyin G (tuproq), H (havo isishi) va LE (bug'lanish) ga taqsimlanadi.

$$R_n = (1-\alpha)R_{s\downarrow} + R_{L\downarrow} - R_{L\uparrow} - (1-\varepsilon_0)R_{L\downarrow}$$

---

## 2. Atmosfera transmissivity (Allen et al., 2014, Eq. 17–19)

### 2.1 Direct beam — `calculate_direct_transmissivity`

$$\tau_B = 0.98\exp\!\left[\frac{-0.00146\,P}{K_t\cos\theta_{hor}} - 0.075\left(\frac{W}{\cos\theta_{hor}}\right)^{0.4}\right],\quad W = 0.14\,e_a P + 2.1$$

### 2.2 Diffuse — `calculate_diffuse_transmissivity`

$$\tau_D = \begin{cases} 0.35 - 0.36\,\tau_B, & \tau_B \ge 0.15 \\ 0.18 + 0.82\,\tau_B, & \tau_B < 0.15\end{cases}$$

$$\tau_{sw} = \tau_B + \tau_D$$

---

## 3. Instant clear-sky Rso

### 3.1 Tekis — `calculate_instant_rso_flat`

$$R_{so,inst}^{flat} = G_{sc}\cos\theta_{hor}\,d_r\,\tau_{sw},\qquad G_{sc} = 1367\ \mathrm{W/m^2},\ d_r = 1 + 0.033\cos\tfrac{2\pi J}{365}$$

### 3.2 Tog'li — `calculate_instant_rso` (default `instant_incoming_sw_clear_sky`)

Uch komponent: **beam** (qiyalikka tushadigan), **diffuse** (osmon ko'rinish faktori bilan), **reflected** (qo'shni relyefdan qaytgan):

$$f_{sky} = 0.75 + 0.25\cos s - 0.5\frac{s}{\pi}\quad(s\ \text{radian})$$

$$R_{so,inst} = \underbrace{\tau_B G_{sc} d_r\cos\theta_{mtn}}_{beam} + \underbrace{\tau_D G_{sc} d_r\cos\theta_{hor}\,f_{sky}}_{diffuse} + \underbrace{R_{so}^{flat}\,\alpha_{terr}(1 - f_{sky})}_{terrain}$$

$\alpha_{terr} = 0.2$ (hardcoded, TODO izohi bor). Kodda $\cos\theta_{hor}$ = `cos(pi/2 - asin(sinβ))` ko'rinishida yozilgan (bu $\sin\beta$ ga teng).

---

## 4. Daily clear-sky Rso

### 4.1 Kunlik extraterrestrial (qiyalikda) — `calculate_daily_extraterr_radiation`

24 soat **48 ta yarim soatlik** qadamga bo'linadi ($t = 0.25, 0.75, ..., 23.75$), $\omega = 15°(t-12)$:

$$\cos\theta_{rel}(\omega) = X + Y\cos\omega + Z\sin\omega$$

$$X = \sin\delta\sin\varphi\cos s - \sin\delta\cos\varphi\sin s\cos\gamma,\quad Y = \cos\delta\cos\varphi\cos s + \cos\delta\sin\varphi\sin s\cos\gamma,\quad Z = \cos\delta\sin s\sin\gamma$$

Quyosh gorizontdan past ($\sin\beta \le 0$) yoki qiyalik soyada ($\cos\theta_{rel} \le 0$) → 0.

$$R_{a,24}^{temp} = \frac{1367\,d_r}{24}\cdot 0.5\sum_{i=1}^{48}\cos\theta_{rel}(\omega_i)$$

Minimal chegara ($r_{min} = 0.1$):

$$R_{a,24}^{flat} = \frac{1367}{\pi}d_r[\omega_s\sin\varphi\sin\delta + \cos\varphi\cos\delta\sin\omega_s]$$

$$R_{a,24} = \begin{cases} R_{a,24}^{temp}/\cos s, & R_{a,24}^{temp} > r_{min}R_{a,24}^{flat} \\ r_{min}R_{a,24}^{flat}/\cos s, & \text{aks holda}\end{cases}$$

### 4.2 Kunlik transmissivity

Kunlik o'rtacha zenit (`calculate_cos_theta_flat_daily`) va kunlik $e_a$ (gridMET $q$ dan) bilan $\tau_{B,24}$, $\tau_{D,24}$.

### 4.3 `calculate_daily_rso_flat` va `calculate_daily_rso`

$$R_{so,24}^{flat} = (\tau_{B,24} + \tau_{D,24})\,R_{a,24}^{flat}$$

$$R_{so,24} = \tau_{B,24}R_{a,24} + \tau_{D,24}R_{a,24}^{flat}f_{sky} + R_{so,24}^{flat}\,0.2\,(1-f_{sky})$$

---

## 5. Radiation adjustment coefficient — `radiation_adjustment_coefficient`

Tog'da instant ETrF ni kunlik ETrF ga o'tkazishda qiyalik effekti kun davomida o'zgaradi. Tuzatish:

$$C_{rad} = \min\!\left(\frac{R_{so,inst}^{flat}}{R_{so,inst}}\cdot\frac{R_{so,24}}{R_{so,24}^{flat}},\ 1.5\right)$$

> 🧠 **Feynman:** Ertalabki soat 11 da sharqiy qiyalik quyoshga "yuzma-yuz" — Landsat paytida unga ko'p energiya tushadi. Lekin kun bo'yi (tushdan keyin) u soyada. Demak overpass paytidagi nisbat kunlik nisbatdan katta. $C_{rad}$ shu "ertalab–kun" farqini tekislaydi.

`etrf_instant = calculate_etrf(self) × C_rad` (eeflux.py:1219).

---

## 6. Net radiation (tog'li, default) — `calculate_net_radiation_mountain`

### 6.1 Incoming longwave

Cold piksel temperaturasi **cold piksel balandligidan** har bir piksel balandligiga lapse qilinadi:

$$T_{cold}(z) = T_{s,cold} - \Delta T_{lapse}(z;\ z_{cold})$$

$$\varepsilon_a = 0.85\,(-\ln\tau_{sw})^{0.09}\qquad (\text{Allen et al., 2007 Eq. 25})$$

$$R_{L\downarrow} = \varepsilon_a\sigma T_{cold}^4\,f_{sky} + \varepsilon_0\sigma T_{terr}^4\,(1 - f_{sky})$$

Ikkinchi had — qo'shni qiyaliklardan kelgan uzun to'lqin ($T_{terr}$ — [03](03_surface_temperature.md#6-terrain-lst--calculate_lst_terrain_general)).

> 🧠 **Nega cold piksel temperaturasi?** Yaxshi sug'orilgan sovuq piksel ustidagi havo harorati ≈ uning yuza temperaturasi. Bu NLDAS dan "qo'pol" $T_a$ ishlatishdan aniqroq — **internal calibration** g'oyasi.

### 6.2 Rn formulasi

$$R_n = (1-\alpha')R_{so,inst} + R_{L\downarrow} - \varepsilon_0\sigma T_s^4 - (1-\varepsilon_0)R_{L\downarrow},\quad \sigma = 5.67\times10^{-8}$$

- $\alpha'$ = `albedo_tall_vegetation` (tuzatilgan albedo!)
- $\varepsilon_0$ — broadband emissivity ([05](05_common_products.md#9-emissivity-va-sifat-maskasi))
- $T_s$ — asl (tuzatilmagan) surface temperature

> 📝 Kodda `Rso_adj = 0` → $\sqrt{R_{so}R_{so}^{flat}}$ variant **hech qachon** ishlamaydi (o'chirilgan feature). Har doim $(1-\alpha')R_{so,inst}$.

---

## 7. Net radiation (tekis) — `calculate_net_radiation` (`EEFluxFlat`)

$$R_{L\downarrow} = 0.85(-\ln\tau_{sw})^{0.09}\sigma\,(T_{cold} - \Delta T_{total})^4$$

$$R_n = (1-\alpha)G_{sc}\cos\theta_{hor}d_r\tau_{sw} + R_{L\downarrow} - \varepsilon_0\sigma T_s^4 - (1-\varepsilon_0)R_{L\downarrow}$$

Qaytaradi: `(RLin_flat, RLout, Rn)` — eeflux'da `[2]` index olinadi.

---

## 8. Yordamchi funksiyalar

| Funksiya | Vazifa |
|---|---|
| `calculate_radiation_lw_incoming_flat(T, τ)` | $0.85(-\ln\tau)^{0.09}\sigma T^4$ |
| `calculate_radiation_lw_incoming_mountain(T, τ, s, ε, T_terr)` | §6.1 formula |
| `calculate_radiation_lw_outgoing(T, ε)` | $\varepsilon\sigma T^4$ |
| `calculate_rso_products(...)` | Barcha Rso + $C_{rad}$ bir tasvirda (legacy) |
