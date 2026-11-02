# 03 — Endmember (hot/cold) qidiruvi va ETrF (pyMETRIC, Nieto)

> **Manba:** `pyMETRIC/endmember_search.py`, `pyMETRIC/PyMETRIC.py` (`run_METRIC`, 584–695-qatorlar)

---

## 1. Feynman tushuntirish

Tasvir — bu bir sinfdagi o'quvchilar. Uchta "tanlov komissiyasi" bor:

| Usul | Kod | Uslub |
|---|---|---|
| **MINMAX** | 2 | "Eng sovuq va eng issiq piksel" — eng oddiy, lekin bulut/suvni ham tanlashi mumkin |
| **CIMEC** | 0 (default) | Allen et al. (2013): NDVI va LST persentillari + albedo + bir xillik |
| **ESA** | 1 | Bhattarai et al. (2017): bir xillik filtri → gistogramma tozalash → bosqichma-bosqich qidiruv → reyting |

---

## 2. Landcover guruhlari (IGBP, pyTSEB kodlari)

`run_METRIC` model fizikasini ikki guruh uchun **alohida** ishga tushiradi:

| Guruh | `SEARCH_ORDER[j]` | Reference |
|---|---|---|
| `tall` | CONIFER_E(1), BROADLEAVED_E(2), CONIFER_D(3), BROADLEAVED_D(4), FOREST_MIXED(5), SAVANNA_WOODY(8), GRASS(10), SHRUB_C(6), SHRUB_O(7), CROP_MOSAIC(14), BARREN(16), WETLAND(11) | tall (alfalfa), `ET0_SEARCH_STRING=1` |
| `short` | SAVANNA(9), GRASS(10), CROP(12), CROP_MOSAIC(14), BARREN(16), WETLAND(11) | short (grass), `0` |

> ⚠️ GRASS, CROP_MOSAIC, BARREN, WETLAND **ikkala** guruhda bor. Ikkinchi (short) o'tishda bu piksellar qayta hisoblanadi va **ustiga yoziladi** — natijada ular uchun yakuniy qiymat short guruh kalibratsiyasidan olinadi.

Har guruh uchun: `aoi` maskasi → `ET0_datum`, `ET0` (`pet_asce`) → endmember qidiruvi → `METRIC.METRIC`.

---

## 3. ETrF cold va hot (Allen et al., 2013)

$VI_{max} = 0.95$:

$$ET_rF_{cold} = \begin{cases} 1.05, & VI \ge 0.95\\ \dfrac{1.05}{0.95}VI, & VI < 0.95\end{cases}\qquad(\text{Eq. 4})$$

$$ET_rF_{hot} = VI\cdot ET_rF_{cold} + (1 - VI)\cdot ET_rF_{bare}\qquad(\text{Eq. 5})$$

$ET_rF_{bare}$ = `ET_bare_soil` (raster yoki 0). Keyin:

$$LE_{cold} = ET_rF_{cold}\cdot LE_{ref,datum}^{cold},\qquad LE_{hot} = ET_rF_{hot}\cdot LE_{ref,datum}^{hot}$$

> 🧠 Hot pikselda ham ETrF > 0: qisman o'simlik qoplami ($VI$) transpiratsiya qiladi. Shu sababli $LE_{hot} \ne 0$.

---

## 4. Bir xillik o'lchovlari — `moving_cv_filter(data, (11, 11))`

$$\bar x = x * K_{11\times11},\qquad \sigma = \sqrt{(x - \bar x)^2 * K},\qquad CV = \sigma/\bar x$$

`convolve2d(mode='same', boundary='symm')`. $K$ — tekis kernel ($1/121$).

| Massiv | Ishlatilishi |
|---|---|
| `cv_ndvi` | CIMEC hot, ESA |
| `cv_lst` (Tr_datum) | CIMEC cold |
| `std_lst` | ESA |
| `cv_albedo` | ESA |

> ⚠️ `convolve2d` NaN ni tarqatadi: NaN pikseldan 5 piksel radiusda CV = NaN. Bulut chekkalari avtomatik "bir xil emas" bo'lib qoladi (`nanmin` NaN larni o'tkazib yuboradi). Bu foydali yon effekt. Bundan tashqari CV $\bar x$ ga bo'linadi — LST Kelvinda bo'lgani uchun $CV_{LST}$ juda kichik (~0.001) chiqadi.

---

## 5. CIMEC — `cimec(vi, lst, albedo, sza, cv_ndvi, cv_lst, adjust_rainfall=False)`

(Allen et al., 2013, *Calibration using Inverse Modeling at Extreme Conditions*)

### 5.1 🥶 Cold

1. $VI \ge P_{95}(VI)$ — eng yashil 5%
2. $T_{low} = P_{20}(LST\,|\,VI \ge P_{95})$; `lst_index` $= LST \le T_{low}$
3. $\bar T_{cold} = \overline{LST[\text{lst\_index}]}$
4. Alfalfa albedo ($\beta = 90° - SZA$):

$$\alpha_{thr} = 0.001343\,\beta + 0.3281\,e^{-0.0188\beta}\qquad(\text{Eq. 7})$$

5. Kandidatlar: `lst_index` ∧ $|LST - \bar T_{cold}| \le 0.2$ K ∧ $|\alpha - \alpha_{thr}| \le 0.02$
6. Ular orasidan $CV_{LST}$ minimal bo'lgani → **birinchisi** (`argwhere[0]`)

### 5.2 🔥 Hot

1. $VI \le P_{10}(VI)$
2. $T_{high} = P_{80}(LST\,|\,VI \le P_{10})$; `lst_index` $= LST \ge T_{high}$
3. $\bar T_{hot} = \overline{LST[\text{lst\_index}]}$
4. Ixtiyoriy yog'in tuzatishi (Eq. 8), `adjust_rainfall = (P_{60}, ET_{r,60})`:

$$\bar T_{hot} \leftarrow \bar T_{hot} - \left(2.6 - 13\,\frac{P_{60}}{ET_{r,60}}\right)$$

5. Kandidatlar: `lst_index` ∧ $|LST - \bar T_{hot}| \le 0.2$ K
6. $CV_{NDVI}$ minimal → birinchisi

> 🐛 2-qadamda `lst_index` **butun aoi** bo'yicha olinadi, NDVI sharti bilan kesishtirilmaydi (`lst_array <= lst_low`, `ndvi_index` emas). Shuning uchun cold kandidatlar orasiga sovuq, lekin yashil bo'lmagan piksellar (suv, soya) kirib qolishi mumkin. Albedo sharti buni qisman to'xtatadi, hot uchun esa bunday himoya yo'q ([06](06_kuzatuvlar.md) #6).

> 🐛 Agar kandidat bo'lmasa, `np.nanmin` bo'sh massivda `ValueError` beradi, `argwhere(...)[0]` esa `IndexError` beradi. Funksiya `None` qaytarmaydi — dastur to'xtaydi.

---

## 6. ESA — `esa(vi, lst, cv_vi, std_lst, cv_albedo)` (Bhattarai et al., 2017)

### 6.1 Bir xillik

$$CV_{VI} \le 0.25\ \land\ CV_\alpha \le 0.25\ \land\ \sigma_{LST} < 1.5\ K$$

### 6.2 Gistogramma bo'yicha outlier tozalash — `histogram_fiter`

Takrorlash: LST bin = 0.25 K, VI bin = 0.01. Chekka binda (min/max) **< 50** piksel bo'lsa, o'sha bin tashlanadi. 4 ta chekka binning hammasida ≥ 50 piksel qolguncha davom etadi. Natija: $[LST_{min}, LST_{max}]$, $[VI_{min}, VI_{max}]$.

### 6.3 Bosqichma-bosqich qidiruv — `incremental_search`

Cold: $n_{LST}, n_{VI} = 1, 2, \dots, 10 + step$:

$$VI \ge P_{100 - n_{VI}}(VI),\quad LST \le P_{n_{LST}}(LST)$$

≥ 10 piksel topilsa → qaytaradi. Topilmasa `step += 5` (step > 90 bo'lsa `[]`). Hot — teskari ($VI \le P_{n_{VI}}$, $LST \ge P_{100 - n_{LST}}$).

### 6.4 Reyting — `rank_array`

Har massiv uchun rang (0..N−1, argsort'ning argsort'i):

$$R_{cold} = rank(VI) - rank(LST)\ \to\ \max,\qquad R_{hot} = rank(LST) - rank(VI)\ \to\ \max$$

> ⚠️ `rank_array` NaN larni ham saralaydi (NaN eng oxiriga tushadi va eng katta rangni oladi). Kandidatlar mask bilan cheklangani uchun NaN lar tanlanmaydi, lekin boshqa piksellarning rang qiymatlari siljiydi.

---

## 7. MINMAX — `maxmin_temperature(vi, lst, vi_lower_limit=None)`

```python
vi_lower_limit = np.nanpercentile(vi_array, 0.05)      # ⚠️ 0.05-persentil (5% emas!)
cold: min(LST | VI >= limit)    hot: max(LST | VI <= limit)
```

> 🐛 0.05-persentil deyarli minimal VI ga teng. Natijada cold = deyarli **butun tasvirdagi eng sovuq** piksel (bulut chekkasi, suv, qor bo'lishi mumkin). Hot esa eng past VI li bir necha piksel ichidan tanlanadi. Namunaviy config'da aynan shu usul (`endmember_search=2`) tanlangan ([06](06_kuzatuvlar.md) #7).

---

## 8. Natija metama'lumotlari (`out_data`)

| Kalit | Ma'no |
|---|---|
| `T_sd`, `T_vw` | hot ("soil dry") va cold ("vegetation wet") $T_{R,datum}$ |
| `VI_sd`, `VI_vw` | ularning VI qiymati |
| `cold_pixel_global`, `hot_pixel_global` | 2-D (row, col) — `get_nested_position` bilan |
| `LE_cold`, `LE_hot` | W/m² |

Topilmasa → `-9999`. Global indeks quyidagicha topiladi:

```python
G = np.ravel_multi_index(np.where(global_mask), global_mask.shape)
global_index = np.unravel_index(G[local_index], global_mask.shape)
```
