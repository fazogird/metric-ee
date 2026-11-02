# 06 — Vaqt bo'yicha interpolyatsiya (pymetric, WSWUP)

> **Manba:** `code/local/landsat_interpolate.py`, `code/interp_functions/interpolate_support.py`, `interpolate_rasters_func.py` (`--rasters`), `interpolate_tables_func.py` (`--tables`)

---

## 1. Feynman tushuntirish

Har bir Landsat sahnasi ETrF ning "suratini" beradi, lekin suratlar orasida 8–16 kun (bulut bo'lsa undan ham ko'p) bo'shliq bor. Interpolyatsiya — "multfilm chizuvchi": kalit kadrlar (sahnalar) orasidagi oraliq kadrlarni chizadi. Har kun uchun ETrF chiziqli (yoki kubik) to'ldiriladi, so'ng **o'sha kunning** ETr si bilan ko'paytiriladi:

$$ET_d = ET_rF_d^{interp}\cdot ET_{r,d},\qquad ET_{oy} = \sum_{d\in oy}ET_d$$

---

## 2. Bosqichlar (`block_func`, har blok uchun)

### 2.1 ETrF ni yuklash va mozaika — `load_etrf_func`

Bir sana uchun bir nechta tile (path/row) bo'lishi mumkin. Har tile ETrF chiqish gridiga qayta proyeksiyalanadi (`clip_project_raster_func`, `resampling_type`). So'ng:

$$ET_rF_d = \mathrm{nanmean}_{tile}(ET_rF_{d,tile})$$

`mosaic_func` (boshqa joylarda): `first`, `last`, `mean` usullari.

### 2.2 Yaroqlilik

$$N_{px} = \sum_d[ET_rF_d\ \text{finite}],\qquad \text{count\_mask} = N_{px} \ge \text{usable\_image\_count}\ (2)$$

$0 < N_{px} < 2$ bo'lgan piksellar butunlay NaN qilinadi.

### 2.3 ETrF ni NDVI bilan almashtirish (ixtiyoriy, `etrf_ndvi_flag`)

ETrF yo'q, lekin NDVI bor sanalar yoki berilgan oy/DOY lar uchun:

$$ET_rF = s\cdot NDVI + o\qquad(s = \text{etrf\_ndvi\_slope},\ o = \text{etrf\_ndvi\_offset})$$

### 2.4 Chegaralash

$$ET_rF < L_{low} \Rightarrow L_{low} + 10^{-7},\qquad ET_rF > L_{high} \Rightarrow L_{high}$$

(`low_etrf_limit`, `high_etrf_limit` — INI da berilsa)

### 2.5 Chekka to'ldirish — `end_fill_func`

Yilning **birinchi** va **oxirgi** kuni (cubicspline bo'lsa 2-va oxiridan 2-kun ham) NaN bo'lsa, eng yaqin mavjud sana qiymati bilan to'ldiriladi (birinchi kun — keyingi sanalardan, oxirgi kun — oldingilardan). Ya'ni chekkalarda **konstanta ekstrapolyatsiya**.

### 2.6 Vaqt bo'yicha bo'shliq to'ldirish — `temporal_fill_func`

Sahna sanalari orasida piksel NaN bo'lsa (bulut), oldingi mavjud va keyingi mavjud qiymat orasida interpolyatsiya qilinadi:

| `fill_method` | Formula |
|---|---|
| `linear` (default) | `scipy.interpolate.interp1d(kind='linear')` 2 nuqtada |
| `cubicspline` | 4 nuqta (2 oldingi + 2 keyingi), `kind=3` |
| `nearest` | (amalga oshirilmagan — `pass`) |
| `spatial` | `sys.exit()` |

### 2.7 Kunlik interpolyatsiya — `interpolate_func`

Har kun $t$ uchun eng yaqin oldingi va keyingi sahna sanasi ($t_p \le t < t_n$):

$$ET_rF(t) = ET_rF_p + \frac{t - t_p}{t_n - t_p}(ET_rF_n - ET_rF_p)$$

(`interp_method = cubic/cubicspline` — 4 nuqta.)

NDVI ham xuddi shu tartibda interpolyatsiya qilinadi.

### 2.8 Ob-havo

| O'zgaruvchi | Ishlov |
|---|---|
| ETr (kunlik) | `drigo.project_array(..., GRA_Bilinear)` → chiqish gridi |
| PPT | xuddi shu |
| SWB ($K_e$) | `array_swb_func` hisoblanadi, lekin **natija o'chiriladi** (`del ke_array`) — qo'llanmaydi ([09](09_kuzatuvlar.md)) |

### 2.9 Agregatsiya

| Davr | ET | ETr | PPT | NDVI | count |
|---|---|---|---|---|---|
| kunlik | $ET_rF\cdot ET_r$ | | | | ETrF mask |
| oylik | $\sum$ (nansum) | $\sum$ | $\sum$ | $\overline{NDVI}$ (nanmean) | $\sum$ mask |
| yillik | $\sum$ | $\sum$ | $\sum$ | o'rtacha | $\sum$ |

`count_mask` dan tashqari piksellar NaN; `etr_mask`, `ppt_mask` — ob-havo NaN bo'lgan joylar.

Ko'p protsessorli rejim: `block_worker` + `multiprocessing` Queue, ETr/PPT umumiy xotirada (`ctypeslib.as_array(shmem)`).

---

## 3. Parametrlar (`landsat_interpolate.ini`)

| Parametr | Default | Ma'no |
|---|---|---|
| `study_area_proj`, `study_area_cellsize`, `study_area_snap` | —, 30, (0, 0) | Chiqish CRS va grid |
| `tile_list` | | path/row ro'yxati |
| `use_landsat4/5/7/8_flag` | False | Qaysi sensorlar |
| `fill_method` / `interp_method` | linear / linear | |
| `mosaic_method` | mean | |
| `tile_buffer` | 0.25° | |
| `blocksize` | 256 | |
| `swb_adjust_flag`, `swb_ndvi_bare`, `swb_ndvi_full` | False | (ishlatilmaydi) |
| `etrf_ndvi_flag`, `_slope`, `_offset`, `_doy_list`, `_month_list` | False | |
| `low_etrf_limit`, `high_etrf_limit` | — | |
| `calc_daily/monthly/annual_{et, etr, etrf, ndvi, ppt, count}_flag` | | Chiqishlar |

`swb_adjust_fc(ndvi, full, bare)` = $1 - (NDVI_{full} - NDVI)/(NDVI_{full} - NDVI_{bare})$ — kodda e'lon qilingan, ishlatilmaydi.

---

## 4. `--tables` rejimi (`interpolate_tables_func.py`)

Rasterlar o'rniga **zonalar** (masalan dala poligonlari, `zones_*` parametrlari) bo'yicha jadval chiqaradi. Interpolyatsiya mantiqi xuddi shu (`interpolate_support`), natija — CSV/jadval.

---

## 5. CRS / NoData

| Masala | Xatti-harakat |
|---|---|
| Chiqish CRS | `study_area_proj` (WKT yoki EPSG), `cellsize`, `snap` — barcha tile'lar shu gridga **qayta proyeksiyalanadi** |
| Ikki UTM zona | Har tile o'z zonasida → umumiy chiqish gridiga `clip_project_raster_func` bilan |
| ETr/PPT resampling | Bilinear (4 km gridMET → 30 m) |
| Bo'sh davr | Yil chekkalarida konstanta; ichkarida chiziqli |
| Ko'p tile o'rtachasi | `nanmean` (qoplanish zonalarida ikkala path o'rtachasi) |
