# 10 — Automated Hot/Cold Pixel Selection (avtomatik kalibratsiya)

> **Manba fayl:** `automated_pixel_selection.py` (2709 qator — loyihaning eng katta moduli)
> **Asos:** Allen, R.G., Burnett, B., Kramber, W. et al. (2013). *Automated Calibration of the METRIC-Landsat Evapotranspiration Process*. JAWRA, 49(3). https://doi.org/10.1111/jawr.12056

---

## 1. Feynman tushuntirish: "Sinfdagi eng a'lochi va eng dangasa o'quvchi"

Kalibratsiya uchun ikki "etalon" piksel kerak ([09](09_sensible_heat_flux.md)):

| | 🥶 Cold piksel | 🔥 Hot piksel |
|---|---|---|
| Nima? | To'liq qoplangan, yaxshi sug'orilgan ekin (beda/makkajo'xori) | Quruq, yalang'och dala (shudgor, o'rilgan maydon) |
| NDVI | Yuqori (top 95–100%) | Past (bottom 2–10%) |
| Albedo | Bedaga xos (~0.18–0.25) | ~0.20 |
| $T_{s,dem}$ | Eng sovuq 5–10% | Eng issiq 90–95% |
| ETrF | $K_c \approx (NDVI - 0.15)/0.65$ | $\approx f_c$ (kichik) |
| Joylashuv | Tekis ($slope<5°$), bir xil maydon markazida (chekka emas) | |

Inson-mutaxassis buni ko'z bilan qiladi. eeMETRIC esa **reyting tizimi** quradi: har piksel uchun "qanchalik ideal" degan ball (0..∞), keyin eng yuqori ballni oladi. Bu xuddi o'qituvchi bir nechta mezon (baho, davomat, xulq) bo'yicha **ko'paytma** ball hisoblaganiga o'xshaydi — bitta mezon 0 bo'lsa, umumiy ball 0.

---

## 2. Arxitektura

```text
EEFlux.hot_and_cold_pixels
   └── PixelSelection(eeflux).selection_method
         ├── 'dynamic' (default) → select_pixels_dynamic_ratings()
         └── 'static'            → select_pixels_static_ratings()
   → ee.List([hot_pixel, cold_pixel, hot_rating_img, cold_rating_img,
              hot_ndvi_tar, ideal_hot_temp, ideal_cold_temp])

EEFlux._calibration_parameters = extract_calibration_params()
   → (hot_candidates FC, cold_candidates FC)  # lai, Ts, Ts_dem, elevation, kc
```

| Konstanta | Qiymat | Ma'no |
|---|---|---|
| `SCALE` | 120 m | Reduksiyalar masshtabi (<90 muammo beradi) |
| `self.scale` (eeflux) | 4 × nominalScale ≈ 120 m | |
| `min_pix_thresh` | 20 | "Yetarli Ag piksel" chegarasi |

---

## 3. Yordamchi bloklar

### 3.1 Mesh — `create_mesh` (dynamic)

Sahna footprint'i 4 marta rekursiv **to'rtga bo'linadi** → $4^4 = 256$ blok (**16 × 16**). Har bo'linishda burchaklar centroid'dan eng uzoq nuqta bo'yicha topiladi (Landsat qiyshiq "romb" footprint'i uchun).

`create_mesh_static` — 2 marta bo'linish → **4 × 4 = 16** blok.

> Kod izohlari ("256 x 256 grid", "16 x 16 grid") bloklar sonini emas, chalkash nomlangan; haqiqiy hisob yuqoridagidek.

### 3.2 Rational function — `rational_function`

$$f(x; x_0) = \frac{1}{|x - x_0|}$$

Reyting sifatida: $r = \mathrm{clamp}(c\cdot f(x;x_0),\ 0,\ 1)$ → $|x - x_0| \le c$ bo'lsa **1** ("plato"), uzoqlashgan sari $c/|x-x_0|$ ga kamayadi. $c$ — plato yarim kengligi.

```text
 r
 1 ┤      ┌──────┐
   │     /        \
   │   /            \___
 0 ┼──────x0-c──x0──x0+c──────► x
```

### 3.3 Edge detection — `detectEdges`

$$E = |\sigma_{3\times3}(NDVI) - 1|$$

(NDVI ning 3×3 oynadagi std). Bir xil maydonda $\sigma \approx 0 \Rightarrow E \approx 1$; dala chegarasida $E$ kichikroq.

### 3.4 Alfalfa albedo (Allen et al., 2013)

$$\alpha_{alf} = 0.03 + 0.001343\,\beta + 0.3281\,e^{-0.0188\,\beta},\quad \beta = \text{SUN\_ELEVATION}\ [°]$$

| β | α_alf |
|---|---|
| 30° | 0.258 |
| 45° | 0.198 |
| 60° | 0.187 |

### 3.5 Slope rating

$$r_{slope} = \mathrm{clamp}\!\left(\frac{127}{s^3 + 100},\ 0,\ 1\right)$$

$s \le 3°$ → 1; $s = 5°$ → 0.56; $s = 10°$ → 0.12.

### 3.6 Land use reytinglari (×0.001)

| NLCD | 11 | 12 | 21 | 22 | 23 | 24 | 31 | 41 | 42/43 | 51/52 | 71 | 72 | 81/82 | 90 | 95 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cold | 0.5 | 0.001 | 0.2 | 0.1 | 0.05 | 0.02 | 0.01 | 0.2 | 0.25 | 0.15 | 0.2 | 0.7 | **1.0** | 0.7 | 0.65 |
| Hot | 0.2 | 0.001 | 0.2 | 0.1 | 0.05 | 0.02 | 0.01 | 0.2 | 0.25 | 0.15 | 0.4 | 0.4 | **1.0** | 0.2 | 0.2 |

---

## 4. Dynamic selection — `select_pixels_dynamic_ratings` (default)

### 4.1 1-qadam: Ag piksellar yetarlimi? — `hot_cold_LU_mask`

Land use = `land_use_mode` (120 m). Ag = NLCD 81/82. Bulutsiz piksellar.

| Populyatsiya | NDVI oralig'i |
|---|---|
| Hot Ag | $0 < NDVI \le 0.5$ |
| Cold Ag | $0.5 < NDVI \le 1.0$ |

Har blokda count; o'rtachaning **1/4** dan kam (va <100) bloklar tashlanadi. Jami ≥ 20 → `has_sufficient_*_ag_pix = True`.

**Landcheck** maskasi:
- yetarli Ag → faqat 81/82
- aks holda → `landuse.neq(11).Or(landuse.neq(12))`

> 🐛 `neq(11).Or(neq(12))` **har doim True** (`A≠11 ∨ A≠12`). Niyat, ehtimol, "suv va muzdan tashqari" (`.And`) edi. Natijada Ag yetarli bo'lmaganda **suv ham** kandidat bo'lishi mumkin; amalda NDVI va temperatura maskalari buni ko'p hollarda filtrlaydi.

### 4.2 2-qadam: NDVI persentillari — `calculate_top_bot_ndvi`

Og'irlangan (`splitWeights`) persentillar, og'irlik = `ndvi_percentile_weights` (Ag va o'rmon uchun 1000, boshqalar kichik):

- Cold: **top95, top99, top99.5, top100**
- Hot: **bot1, bot2.5, bot5, bot10, bot25, bot50**

### 4.3 🔥 Hot piksel — `get_ideal_hot_temperature`

**(a) NDVI oynasi** (`set_hot_ndvi_mask_ranges`): asosan $[NDVI_{2}, NDVI_{10}]$, adaptiv:
- Juda yashil sahna (bot10 > 0.4, Ag yo'q) → bot10 ← bot5 yoki max(bot1, 0.10)
- Juda quruq sahna (bot10 < 0.2) → bot10 ← bot25 yoki min(bot50, 0.40)
- Oyna kengligi ≤ 0.10; yuqori chegara ≥ **0.23** (Roy et al., 2014: TOA 0.20 ≈ SR 0.23)
- $NDVI_5$ ← oyna o'rtasi (o'zgartirilgan bo'lsa)

**(b) Og'irliklar** (`assign_hot_reducer_weights`):

$$r_{edge}^{hot} = \mathrm{clamp}\!\left(\frac{0.15\,NDVI_5}{|E - 1.001|},\ 0.01,\ 1\right)$$

$$r_{om} = \mathrm{clamp}\!\left(\frac{325}{R\%^2 + 100},\ 0.01,\ 1\right)\quad(\text{qoldiq ko'p} \to \text{past ball})$$

$$w_T = \big(w_{edge} + \max(10\,w_{om}\cdot[Ag\ge20] + r_{slope},\ 0.1)\big)\cdot LU_{hot}$$

**(c) Maskalar:** NDVI oynasi ∧ landcheck ∧ bulutsiz ∧ $slope<5°$ ∧ $T_s > 275$ K.

> 🐛 Kod (1346-qator): `slope_mask = cloud_mask.where(tot_count.eq(0), 1)` — slope maskasi **cloud maskasi bilan almashtiriladi**. Natijada hot piksel uchun $slope<5°$ maskasi keyingi bosqichlarda yo'qoladi (faqat $r_{slope}$ reytingi qoladi). Cold versiyada to'g'ri (`slope_mask.where(...)`).

**(d) Blok filtrlash** (`count_filter_min_hot_blocks`): count ≥ mean/4 yoki ≥ 100.

**(e) Ideal hot temperatura:** har blokda og'irlangan $T_{s,dem}$ persentillari **p85, p90, p95, p99**. Keyin $p_{90} \ge \overline{p_{90}}$ bo'lgan (issiqroq yarmi) bloklar qoldiriladi va count bo'yicha og'irlangan o'rtacha:

$$T_{hot}^* = \sum_i \frac{n_i}{\sum n}\,p_{90,i}\quad(NDVI_2 > 0.30 \Rightarrow p_{95})$$

Spatial delapsing muvaffaqiyatli va `ag_elev_diff < 1000 m` bo'lsa → sahna bo'yicha yagona `reduceRegion` persentili (region_temps).

**(f) Hot albedo** (`calc_new_hot_alb_target`): $T_{s,dem} \in (p_{85}, p_{95})$ (yoki $(p_{90}, p_{99})$) oralig'idagi piksellar o'rtacha albedosi $\bar\alpha$; ideal 0.20 bilan aralashtiriladi:

$$\alpha_{targ} \in \{0.20,\ \bar\alpha,\ (\bar\alpha + 0.20)/2\},\qquad r_\alpha^{hot} = \mathrm{clamp}\!\left(\frac{c}{|\alpha - \alpha_{targ}|},0,1\right),\ c\in\{0.015, 0.025, 0.05\}$$

**(g) Hot NDVI reytingi:** $r_{NDVI}^{hot} = \mathrm{clamp}(0.025/|NDVI - NDVI_5|, 0, 1)$

**(h) Temperatura reytingi** (`get_temperature_rating`):

$$r_T = 10\cdot\sqrt{\mathrm{clamp}\!\left(\frac{0.2}{|T_{s,dem} - T^*|},\ 0,\ 1\right)}$$

(maksimal = $1/0.2$ ga normallashtirish → $|T - T^*| \le 0.2$ K da 10.)

**(i) Yakuniy hot reyting:**

$$R_{hot} = 10\cdot r_\alpha^{hot}\,r_{edge}^{hot}\,r_{slope} + r_T\cdot LU_{hot}\cdot r_{NDVI}^{hot} - 100\cdot cloud$$

### 4.4 🥶 Cold piksel — `get_ideal_cold_temperature`

**(a) NDVI oynasi** (`set_cold_ndvi_mask_ranges`): $[NDVI_{95}, NDVI_{100}]$, adaptiv:
- To'yingan NDVI (95–99 farqi < 0.05, NDVI95 > 0.95/0.80) → pastki chegara kengaytiriladi (−0.15/−0.20, clamp 0.80–1)
- NDVI95 = NDVI99 → NDVI95 − 0.20
- Juda past (NDVI95 < 0.5, Ag < 20) → NDVI95 ← min(NDVI99, 0.95)

**(b) Og'irliklar** (`assign_cold_reducer_weights`):

$$r_{edge}^{cold} = \mathrm{clamp}\!\left(\frac{0.15\,NDVI_{95}}{|E - 1.001|},0.01,1\right),\qquad w_T = r'_{edge}\,r_{slope}\,LU'_{cold}$$

($r'_{edge} < 0.5 \to 0.1$; $LU'$: Ag = 10, o'rmon = 2, wetland = 1, ...)

**(c) Ideal cold temperatura:** blok persentillari **p5, p10, p20**; $p_{20} \le \overline{p_{20}}$ (sovuqroq bloklar, faqat NDVI yuqori bo'lsa) filtr; count-og'irlangan:

$$T_{cold}^* = \sum_i w_i\,p_{10,i}\quad(NDVI_{99} - NDVI_{95} > 0.10\ \lor\ Ag \le 20 \Rightarrow p_5)$$

**(d) Cold albedo** (`calc_new_cold_alb_target`): $T \le \overline{p_{20}}$ piksellar o'rtacha albedosi $\bar\alpha$ (fallback 0.20) va $\alpha_{alf}$:

| $\vert \alpha_{alf} - \bar\alpha\vert $ | $\alpha_{targ}$ |
|---|---|
| < 0.02 | $\alpha_{alf}$ |
| 0.02–0.04 | $(\alpha_{alf} + \bar\alpha)/2$ |
| 0.04–0.08 (Ag) | $(\alpha_{alf} + \bar\alpha)/2$ |
| boshqa | $\bar\alpha$ |

Clamp: Ag → [0.15, 0.30], non-Ag → [0.10, 0.30]. Plato $c$ = 0.01 (Ag) / 0.025.

**(e) Cold NDVI** (`calc_new_cold_ndvi_target`): target = $(NDVI_{95} + NDVI_{100})/2$ (to'liq qoplama uchun moslashadi), $c$ = 0.10 (yoki 0.05 agar NDVI100 < 0.8).

**(f) Yakuniy cold reyting:**

$$R_{cold} = 10\cdot r_{NDVI}^{cold}\,r_\alpha^{cold}\,r_{edge}^{cold}\,r_{slope} + r_T\cdot LU_{cold} - 100\cdot cloud$$

### 4.5 Eng yaxshi pikselni topish — `get_max_rated_pixels`

```python
rating = rating.updateMask(self.surface_temperature)     # faqat yaroqli Ts
blocks_max = rating.reduceRegions(aoi, ee.Reducer.max(3).setOutputs(['rating','longitude','latitude']), scale)
best = blocks_max.filter(ee.Filter.gte('rating', blocks_max.aggregate_max('rating'))).first()
```

`Reducer.max(n)` — birinchi band bo'yicha max va **shu pikseldagi** qolgan bandlar (lon, lat) qiymatlari.

---

## 5. Hot va Cold piksel ETrF ($K_c$)

### 5.1 Cold — `calculate_cold_pixel_etrf`

$$K_{c,cold} = \mathrm{clamp}\!\left(\frac{NDVI - 0.15}{0.65},\ 0.11,\ 1.0\right)$$

> Klassik METRIC'da $ETrF_{cold} = 1.05$. eeMETRIC esa NDVI ga bog'liq ($fc$ bilan) → NDVI = 0.80 da 1.0.

### 5.2 Hot (dynamic) — `calculate_hot_pixel_etrf`

$NDVI$ ni target atrofida "snap": $|NDVI - NDVI_{targ}| \le 0.05 \Rightarrow NDVI = NDVI_{targ}$.

$$K_{c,hot} = f_c = \mathrm{clamp}\!\left(\frac{NDVI - 0.15}{0.80 - 0.15},\ 0.05,\ 0.95\right)$$

> ⚠️ Dynamic rejimda **soil water balance ($K_e$) ishlatilmaydi** — faqat $f_c$. `hot_pixel_etrf` NDVI target — `hot_and_cold_pixels[4]` (= $NDVI_5$).

### 5.3 Hot (static) — `calculate_hot_pixel_etrf_static`

$$f_c = \mathrm{clamp}(1.6\,NDVI - 0.5,\ 0,\ 0.95),\qquad K_c = f_c + (1 - f_c)\,K_e$$

$K_e$ faqat sahna "nam" bo'lsa qo'llanadi: $\overline{K_e} > 0.15 \land \sigma_{K_e} < 0.2$ (1 km masshtab). ($K_e$ — [12](12_etrf_et24_soil_water_balance.md#8-soil-water-balance--soil_water_balancepy))

---

## 6. Static selection — `select_pixels_static_ratings`

Eski, oddiyroq usul (`pixel_selection='static'`):

**Reytinglar** (`prepareRatingParams` + `calculate_*_rating`, ikkalasi bir xil formula):

$$R = -100\cdot cloud + 10\cdot r_{NDVI}\,r_\alpha\,E\,LU\,r_{slope}$$

| | Cold | Hot |
|---|---|---|
| $r_{NDVI}$ | $0.10/\vert NDVI - 0.85\vert $ | $0.10/\vert NDVI - 0.20\vert $ |
| $r_\alpha$ | $0.03/\vert \alpha - \alpha_{alf}\vert $ | $0.10/\vert \alpha - 0.20\vert $ |

**Ideal temperatura** (`get_ideal_temperatures`): reyting ≥ 99.6-persentil (cold) / 99.8 (hot) bo'lgan piksellar orasidan $T_{s,dem}$ ning **0.5-persentili** (cold) / **95-persentili** (hot).

Keyin $R \times r_T$ (weight=1), har 4×4 blokdan max, sahnadan max.

---

## 7. Kalibratsiya sifati — `calibration_rating`

$$Q = \underbrace{\mathrm{clamp}(R_{hot}/m)\cdot\mathrm{clamp}(R_{cold}/m)}_{0..1}\cdot\underbrace{[T_{hot,dem} - T_{cold,dem} > 4]}_{0/1}\cdot\underbrace{[0.01 < a < 1.0]}_{0/1}$$

$m$ = 20 (dynamic) / 10 (static). Eksportda `QUALITY` xususiyati.

> 💡 **Amaliy maslahat:** $Q = 0$ bo'lgan sahnalarni (masalan, bulutli, qishki yoki bir xil cho'l) natijada filtrlang. O'zbekistonda qishki sahnalar (dekabr–fevral) ko'pincha $\Delta T < 4$ beradi.

---

## 8. Kalibratsiya parametrlarini chiqarish

### 8.1 `extract_calibration_params`

Hot/cold nuqtada (`reduceRegion(max)`, `crs = Ts proj`, `scale = 120`):

| Xususiyat | Manba |
|---|---|
| `lai` | `leaf_area_index` |
| `surface_temperature` | `surface_temperature` |
| `surface_temperature_dem` | `ts_dem_latlon` |
| `elevation` | `dem` |
| `kc` | `cold_pixel_etrf` / `hot_pixel_etrf` |

### 8.2 `calibration_parameters_for_export`

Qo'shimcha: `ndvi`, `LU`, `static_rating`, `slope`, `surface_temperature_dem`, `albedo`, `G`, `Rn`, `H` (dT kalibratsiyasidan `h_hot`/`h_cold`), `etr_inst`.

### 8.3 `etrf_stats_calculation` (eksportda o'chirilgan — timeout)

Ag piksellar orasida: full cover (NDVI ≥ 0.8) %, ETrF ≥ 1.0 %, ETrF > 1.1 %, NDVI ≤ 0.2 %, ETrF < 0 %.

---

## 9. Server-side "fallback" naqshlari (EE hiylalari)

Kod bo'ylab takrorlanadigan pattern — `null` qaytishining oldini olish:

```python
result = ee.Feature(None, reducer_output).toDictionary()   # null kalitlar tushib qoladi
safe   = result.combine({'mean': 0.20}, overwrite=False)    # yo'q bo'lsa default
```

va "If-siz switch":

```python
flag = cond.multiply(1).add(one.subtract(cond).multiply(0))      # 0/1
coll = ee.FeatureCollection([img_a.set('k', flag), img_b])
chosen = coll.filter(ee.Filter.gt('k', 0)).first()
```

Hech qanday piksel qolmasa (`tot_count == 0`) maskalar "ochiladi" (`.where(tot_count.eq(0), 1)`) — xato o'rniga past sifatli natija.
