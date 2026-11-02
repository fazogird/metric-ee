# 04 — Reference ET: `pet_asce`, `pet_fao56` (pyMETRIC, Nieto)

> **Manba:** `pyMETRIC/METRIC.py` (433–606-qatorlar)

---

## 1. Feynman tushuntirish

Cold piksel "yaxshi sug'orilgan beda" deb olinadi. Uning bug'lanishi $LE_{ref}$ ni Penman–Monteith tenglamasi beradi. Bu modelda $LE_{ref}$ to'g'ridan-to'g'ri **W/m² dagi latent issiqlik** sifatida hisoblanadi (mm/soat emas), so'ng $LE_{cold} = ET_rF_{cold}\cdot LE_{ref}$.

---

## 2. Yordamchi meteo funksiyalar (pyTSEB `meteo_utils`)

| Funksiya | Formula | Birlik |
|---|---|---|
| `calc_vapor_pressure(T)` | $e_s = 6.112\exp\!\frac{17.67t}{t + 243.5}$ (Bolton) | mb |
| `calc_delta_vapor_pressure(T)` | $\Delta = \frac{4098\cdot0.6108\exp(17.27t/(t+237.3))}{(t + 237.3)^2}$ | kPa/K (kodda ×10 → mb/K) |
| `calc_lambda(T)` | $\lambda = 10^6(2.501 - 2.361\cdot10^{-3}t)$ | J/kg |
| `calc_psicr(c_p, p, λ)` | $\gamma = c_pp/(0.622\lambda)$ | mb/K |
| `calc_rho`, `calc_c_p` | [02 §3](02_metric_yadro.md#3-umumiy-kattaliklar) | |

$t = T - 273.15$.

---

## 3. `calc_Ln(T_A_K, ea, f_cd=1)` — sof uzun to'lqin

$$L_n = \sigma f_{cd}\,(0.34 - 0.14\sqrt{0.1\,e_a})\,T_A^4$$

($0.1e_a$ — mb → kPa.) FAO-56 Eq. 39 shakli, lekin **musbat** qiymat qaytaradi (bu yo'qotish miqdori).

`calc_cloudiness(Sdn, S_0)`: $f_{cd} = \mathrm{clamp}(1.35S_{dn}/S_0 - 0.35,\ 0.05,\ 1)$ — kodda chaqirilmaydi, `f_cd = 1`.

---

## 4. `wind_profile(u, z_u, z_0M, d, z)`

$$u_z = u\,\frac{\ln((z - d)/z_{0M})}{\ln((z_u - d)/z_{0M})}$$

---

## 5. `pet_asce(T_A_K, u, ea, p, Sdn, z_u, z_T, f_cd=1, reference=TALL)`

| Parametr | Tall (alfalfa) | Short (grass) |
|---|---|---|
| G/Rn | 0.04 | 0.10 |
| $h_c$ | 0.5 m | 0.12 m |
| $C_d$ | 0.25 | 0.24 |
| $C_n$ | 66 | 37 |

$$\alpha = 0.23,\quad S_n = 0.77S_{dn},\quad R_n = S_n + L_n,\quad G = r_GR_n$$

$$z_{0M} = 0.123h_c,\quad d = 0.67h_c,\quad u_2 = \text{wind\_profile}(u, z_u, z_{0M}, d, 2)$$

**Kodda yozilgani:**

$$LE = \frac{\Delta(R_n - G) + \gamma\,C_n\,u_2\,(e_s - e_a)/T_A}{\Delta + \gamma\,C_d\,u_2}$$

**ASCE-EWRI (2005) standarti** (soatlik, mm/h):

$$ET_{ref} = \frac{0.408\,\Delta(R_n - G) + \gamma\frac{C_n}{T + 273}u_2(e_s - e_a)}{\Delta + \gamma(1 + C_du_2)}$$

### 5.1 Farqlar (statik tahlil + raqamli tekshiruv)

| # | Masala | Kod | Standart |
|---|---|---|---|
| a | $L_n$ ishorasi | $R_n = S_n + L_n$ | $R_n = S_n - L_n$ |
| b | Maxraj | $\Delta + \gamma C_du_2$ | $\Delta + \gamma(1 + C_du_2)$ |
| c | Aerodinamik had birligi | $C_n$ (MJ/mm/kPa uchun kalibrlangan) × $(e_s - e_a)$ [mb] | $\lambda/3600$ va kPa ga moslash kerak |

**Raqamli misol** — namunaviy config qiymatlari ($T_A$ = 299.18 K, $u$ = 2.15 m/s @ 5 m, $e_a$ = 13.4 mb, $p$ = 1011 mb, $S_{dn}$ = 861.74 W/m²). Formulalar alohida skriptda qayta yozib hisoblandi:

| Kattalik | pyMETRIC `pet_asce` | ASCE standarti |
|---|---|---|
| $R_n$ | **744.4** W/m² | **582.7** W/m² |
| $u_2$ | 1.64 m/s (log profil) | 1.80 m/s (Eq. 67) |
| Aerodinamik had | 4.93 | — |
| Maxrajdagi γ hadi | 0.276 mb/K | 0.977 mb/K |
| **LE / ETr** | **629.8 W/m²** | 0.734 mm/h = **497.5 W/m²** |

→ Bu holatda `pet_asce` ETr ni **~27% oshirib** beradi. Asosiy sabab — $L_n$ ishorasi. Aerodinamik had esa amalda deyarli nolga teng. Natija $LE_{cold}$ va `fETr` ga to'g'ridan-to'g'ri o'tadi. ([06](06_kuzatuvlar.md) #2)

---

## 6. `pet_fao56(...)` — FAO-56 qarshilik shakli (kodda chaqirilmaydi)

$$R_c = 70\ \mathrm{s/m},\quad R_a = 208/u_2,\quad z_{0M} = 0.123h_c,\quad d = \tfrac23h_c$$

$$LE = \frac{\Delta(R_n - G) + \rho c_p(e_s - e_a)/R_a}{\Delta + \gamma(1 + R_c/R_a)}$$

> ✔️ Birlik tekshiruvi: surat $[\mathrm{mb/K}\cdot\mathrm{W/m^2}] + [\mathrm{J\,m^{-3}K^{-1}}\cdot\mathrm{mb}/(\mathrm{s/m})] = [\mathrm{mb/K}\cdot\mathrm{W/m^2}]$, maxraj [mb/K] → natija **W/m²**. Demak bu shakl birlik jihatdan **izchil**.
> ⚠️ Lekin bu yerda ham $R_n = S_n + L_n$ (ishora xatosi, a-band). `reference` default — SHORT.
