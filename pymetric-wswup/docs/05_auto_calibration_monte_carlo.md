# 05 — Avtokalibratsiya va Monte Carlo (pymetric, WSWUP)

> **Manba:** `code/metric_functions/monte_carlo_func.py`, `code/metric_functions/auto_calibration_func.py`, `code/support/et_common.py` (`point_swb_func`, `daily_swb_func`), `misc/etrf_training_test.csv`
> **Asos:** Morton, C.G. et al. (2013). *Assessing calibration uncertainty and automation for estimating evapotranspiration from agricultural areas using METRIC*. JAWRA, 49(3).

---

## 1. Feynman tushuntirish: "ETrF gistogrammasining dumi"

Tajribali mutaxassis hot/cold nuqtani tanlaganda, natijada ekin maydonlari ETrF gistogrammasining **chekkalari** (dumlari) ma'lum shaklda bo'ladi. Masalan, Ag piksellarning ~1% i cold ETrF dan katta (1.05+), ~4% i hot ETrF dan kichik bo'ladi. Monte Carlo usuli teskari yo'ldan boradi: "tail size" (dum ulushi) ni beradi va **Kc ni shunday tuzatadiki**, ETrF gistogrammasi o'sha ulushlarga mos kelsin. Tasodifiy tail size'lar bilan ko'p marta takrorlab, kalibratsiya noaniqligi o'lchanadi.

---

## 2. Maqsadli Kc (DOY bo'yicha)

INI: `kc_cold_doy_dict`, `kc_hot_doy_dict` (masalan `1: 1.05, 366: 1.05`). Overpass DOY bo'yicha chiziqli interpolyatsiya:

$$K_{c,cold}^{tgt} = \mathrm{interp}(J;\ \text{kc\_cold\_doy\_dict}),\qquad K_{c,hot}^{tgt} = \mathrm{interp}(J;\ \text{kc\_hot\_doy\_dict})$$

Parse qilinmasa default: cold 1.05, hot 0.1.

> ⚠️ Kod `eval('{' + kc_cold_doy_dict + '}')` ishlatadi. INI fayl ishonchli bo'lmasa, bu ixtiyoriy Python kodini bajarish imkonini beradi ([09](09_kuzatuvlar.md)).

## 3. Tail size — `etrf_fractions(etrf_training_path)`

`misc/etrf_training_test.csv` dagi `kc_cld_pct`, `kc_hot_pct` ustunlari saralanadi va boshiga 0 qo'shiladi. Empirik CDF tuzilib, $U \sim \mathcal U(0, 1)$ bilan teskari namuna olinadi:

$$p_{cold} = F^{-1}_{cold}(U_1),\qquad p_{hot} = F^{-1}_{hot}(U_2)$$

`--tails 1 4` bilan qo'lda ham beriladi (`-mc 0`).

## 4. Hot Kc ni soil water balance bilan tuzatish — `hot_kc_swb_adjust`

Hot nuqtada `point_swb_func` (AWC raster + kunlik ETr, PPT, `swb_spinup_days`):

$$K_{c,hot}^{tgt} = \mathrm{clamp}(K_e,\ 0.1,\ 1.05)$$

Xato: $K_{c,hot}^{tgt} \ge 1.0$ yoki $K_{c,cold}^{tgt} - K_{c,hot}^{tgt} \le 0.05$.

### 4.1 Kunlik SWB — `daily_swb_func` / `array_swb_func` (FAO-56 + Allen 2011)

$$REW = 54.4\,AWC + 0.8,\qquad TEW = 166\,AWC - 3.7\quad[\mathrm{mm}]$$

$$K_r = \mathrm{clip}\!\left(\frac{TEW - D_e}{TEW - REW}, 0, 1\right),\qquad f_t = \mathrm{clip}\!\left(\frac{REW - D_{REW}}{K_{e,max}ET_r}, 0, 1\right)$$

$$E_s = \mathrm{clip}\big((1 - f_t)K_rK_{e,max}ET_r - D_{REW} + REW,\ 0,\ K_{e,max}ET_r\big)$$

$$c_{eff} = \mathrm{clip}\!\left(C_1\frac{TEW - D_e}{TEW} + C_0, 0, 1\right),\quad C_0 = 0.8,\ C_1 = 0.4$$

$$D_{REW} \leftarrow \mathrm{clip}(D_{REW} - c_{eff}P + E_s,\ 0,\ REW),\qquad D_e \leftarrow \mathrm{clip}(D_e - P + E_s,\ 0,\ TEW)$$

$$K_e = \mathrm{clip}(E_s/ET_r,\ 0,\ 1),\qquad K_{e,max} = 1.0$$

Boshlang'ich holat: quruq ($D_e = TEW$, $D_{REW} = REW$).

## 5. Monte Carlo tsikli — `monte_carlo()`

```text
1. pixel_points (tasodifiy) → cold_xy, hot_xy       (≤ max_point_iterations = 10)
2. hot_kc_swb_adjust → hot_tgt_kc
3. kc_cold = cold_tgt_kc, kc_hot = hot_tgt_kc
4. while not calibrated (≤ max_cal_iterations = 5):
       metric_model2(kc_cold, kc_hot) → ETrF raster
       ETrF[~region_mask] = NaN                     (Ag region)
       calibration_params(cal_dict, ETrF)
       check_calibration → True? stop
       kc_calibration_adjust → yangi kc_cold, kc_hot
5. build_pixel_points: ETrF = tgt kc ga eng yaqin nuqtalar → cold.shp, hot.shp
```

### 5.1 Statistikalar — `calibration_params`

`sap_float(a, p)` = $P_p(a)$ ("score at percentile"), `pos_float(a, s)` = persentil o'rni ("percentile of score").

| Kalit | Formula |
|---|---|
| `cold_tgt_kc_pct` | $100 - \mathrm{pos}(ETrF, K_{c,cold}^{tgt})$ — cold ETrF dan kattalar ulushi |
| `hot_tgt_kc_pct` | $\mathrm{pos}(ETrF, K_{c,hot}^{tgt})$ — hot dan kichiklar ulushi |
| `cold_tgt_pct_kc` | $P_{100 - p_{cold}}(ETrF)$ |
| `hot_tgt_pct_kc` | $P_{p_{hot}}(ETrF)$ |

### 5.2 Konvergensiya — `check_calibration`

$$\lvert p_{cold} - \text{cold\_tgt\_kc\_pct}\rvert \le 0.5\%\ \land\ \lvert p_{hot} - \text{hot\_tgt\_kc\_pct}\rvert \le 0.5\%$$

### 5.3 Kc tuzatish — `kc_calibration_adjust` (chiziqli qayta masshtablash)

$K_{cc}^t, K_{ch}^t$ — maqsadli Kc; $Q_c$ = `cold_tgt_pct_kc`, $Q_h$ = `hot_tgt_pct_kc`:

$$K_{c,hot}' = \frac{K_{ch}^t - K_{cc}^t}{Q_h - K_{cc}^t}(K_{c,hot} - K_{cc}^t) + K_{cc}^t$$

$$K_{c,cold}' = \frac{K_{cc}^t - K_{ch}^t}{Q_c - K_{ch}^t}(K_{c,cold} - K_{ch}^t) + K_{ch}^t$$

> 🧠 Ma'nosi: agar ETrF ning $p_{hot}$-persentili ($Q_h$) maqsad $K_{ch}^t$ dan katta bo'lsa, `kc_hot` mos ravishda siljitiladi. Bu ETrF taqsimotini maqsadli dumlarga "cho'zish" bilan teng.

### 5.4 Yakuniy nuqtalar — `build_pixel_points`, `get_target_point_in_array`

$$\text{nuqta} = \arg\min\lvert ETrF - K_c^{tgt}\rvert\quad(\text{teng qiymatlilar orasidan tasodifiy})$$

### 5.5 Gistogrammalar

`save_etrf_histograms`, `save_ndvi_histograms` — `PLOTS` papkasiga (bin 0.01).

---

## 6. Parametrlar (`landsat_metric_monte_carlo.ini`)

| Parametr | Default |
|---|---|
| `max_cal_iterations` | 5 |
| `max_point_iterations` | 10 |
| `ts_diff_threshold` | 4 K |
| `swb_spinup_days` / `swb_min_spinup_days` | 5 / 30 (kod defaulti), example INI: 30 / 5 |
| `etrf_training_path` | `misc/etrf_training_test.csv` |
| `kc_cold_doy_dict`, `kc_hot_doy_dict` | DOY → Kc |
| `save_etrf_temp_plots`, `save_etrf_final_plots`, `save_ndvi_plots` | |

> ⚠️ Kodda `swb_spinup_days=5`, `swb_min_spinup_days=30` defaultlari mantiqan teskari (min > umumiy). Example INI esa to'g'ri qiymatlarni beradi (30 / 5).
