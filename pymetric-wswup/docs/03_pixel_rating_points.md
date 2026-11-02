# 03 — Pixel rating va kalibratsiya nuqtalari (pymetric, WSWUP)

> **Manba:** `code/metric_functions/pixel_rating_func.py`, `code/metric_functions/pixel_points_func.py`

---

## 1. Feynman tushuntirish

Bu bosqich — "nomzodlar ro'yxati". Avtomatik tizim yakuniy qarorni bermaydi. U har bir piksel uchun 0..1 atrofida "cold bo'lish ehtimoli" va "hot bo'lish ehtimoli" reytingini hisoblaydi va eng yaxshi 1% ni (`*_suggestion` raster) belgilaydi. Shundan keyin mutaxassis ArcGIS'da bitta cold va bitta hot nuqtani tanlaydi (`cold.shp`, `hot.shp`). `pixel_points` esa boshlang'ich nuqtani tasodifiy tanlab beradi.

---

## 2. Region mask

```python
region_mask = env.mask_array                 # common_area ∧ fmask toza
region_mask &= field_mask != nodata          # apply_field_mask (False)
region_mask &= ndwi_toa > 0.0                # apply_ndwi_mask (True)  — suvni chiqarish
region_mask &= ndvi_toa > 0.12               # apply_ndvi_mask (True)
region_mask &= cdl_ag_eroded != nodata       # apply_cdl_ag_mask (False), cdl_buffer_cells bilan erode
```

> NDWI bu yerda $(\rho_{SWIR1} - \rho_G)/(\rho_{SWIR1} + \rho_G)$. Suvda $\rho_G > \rho_{SWIR1}$ bo'lgani uchun NDWI < 0 → maskalanadi.

---

## 3. Reyting komponentlari (multiplikativ)

Boshlanishi: $R_{cold} = R_{hot} = 1$ (region ichida), tashqarida NaN.

### 3.1 Temperatura (`ts_rating_flag = True`)

$T_s$ ning `ts_bin_count = 10` ta persentil bini: $P_0, P_{10}, \dots, P_{100}$. Bin $i$ uchun ($i = 0..9$):

$$R_{hot}^{T} = \frac{i}{9},\qquad R_{cold}^{T} = 1 - \frac{i}{9}$$

(eng sovuq 10% → cold = 1, hot = 0; eng issiq 10% → cold = 0, hot = 1)

### 3.2 NDVI (`ndvi_rating_flag = True`)

$NDVI \leftarrow \mathrm{clip}(NDVI, 0, 0.833)$:

$$R_{cold} \mathrel{*}= 1.20\cdot NDVI\qquad(\text{maks}\ 1.2\cdot0.833 \approx 1)$$

$$R_{hot} \mathrel{*}= 1.25\cdot\mathcal N\!\left(\ln NDVI;\ \mu = \ln0.15,\ \sigma = 0.5\right)\quad(NDVI > 0)$$

($\mathcal N$ — normal taqsimot zichligi, `scipy.stats.norm.pdf`. Uning maksimumi $\approx 0.798$, shuning uchun $1.25\cdot0.798 \approx 1$.)

### 3.3 Albedo (`albedo_rating_flag = True`)

$$R_{cold} \mathrel{*}= 0.07\cdot\mathcal N(\alpha;\ 0.21,\ 0.03),\qquad R_{hot} \mathrel{*}= 0.15\cdot\mathcal N(\alpha;\ 0.21,\ 0.06)$$

(Maksimumlar: $0.07/(0.03\sqrt{2\pi}) \approx 0.93$, $0.15/(0.06\sqrt{2\pi}) \approx 1.0$.)

### 3.4 Land cover (`nlcd_rating_flag = True`) — `nlcd_rating`

| NLCD | 11 | 12 | 21 | 22 | 23 | 24 | 31/32 | 41 | 42/43 | 51/52 | 71 | 72 | 73/74 | **81/82** | 90 | 94 | 95 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Reyting | 0.5 | 0.001 | 0.2 | 0.1 | 0.05 | 0.02 | 0.01 | 0.2 | 0.25 | 0.15 | 0.4 | 0.7 | 0.3 | **1.0** | 0.7 | 0.2 | 0.65 |

Cold va hot uchun **bir xil** jadval.

### 3.5 Soil water ($K_e$) (`ke_rating_flag = False`)

$$R_{hot} \mathrel{*}= 1 - \mathrm{clip}(K_e, 0, 1)$$

---

## 4. Tavsiya (suggestion) rasterlari

$$S_{cold} = R_{cold} \ge P_{99}(R_{cold}),\qquad S_{hot} = R_{hot} \ge P_{99}(R_{hot})$$

(`cold_percentile`, `hot_percentile` = 99). Chiqish: `PIXEL_REGIONS/cold_pixel_suggestion.img`, `hot_pixel_suggestion.img` (uint8). Ixtiyoriy: `cold/hot_pixel_rating.img`, `region_mask.img`.

---

## 5. `pixel_points` — boshlang'ich nuqtalar

`get_random_point_in_raster(raster_path, groupsize, blocksize)`:

1. Suggestion raster bloklari **tasodifiy tartibda** o'qiladi (`drigo.block_gen_random`).
2. Har blokda `ndimage.label` (8-bog'lanish) bilan bog'langan klasterlar topiladi. Har pikselga o'z klasterining **o'lchami** (piksellar soni) yoziladi.
3. O'lchami ≥ `groupsize` bo'lgan klaster topilsa, undan **tasodifiy** piksel olinadi va qidiruv to'xtaydi. Topilmasa (yoki `groupsize = -1` bo'lsa), har blokdagi eng katta klasterdan nuqta saqlanadi va oxirida eng kattasi tanlanadi.
4. Piksel markazi koordinatasi shapefile'ga (`PIXELS/cold.shp`, `hot.shp`) yoziladi (sahna UTM proyeksiyasida).

> 🧠 Tasodifiylik muhim: Monte Carlo ([05](05_auto_calibration_monte_carlo.md)) har iteratsiyada boshqa nuqta tanlab, kalibratsiya noaniqligini o'lchaydi.
