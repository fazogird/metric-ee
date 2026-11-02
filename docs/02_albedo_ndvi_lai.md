# 02 — Albedo, NDVI, LAI va Snow/Water flag

> **Manba fayllar:** `surface_albedo.py`, `vegetation_indices.py`, `snow_water_flag_calculation.py`

---

## 1. Feynman tushuntirish

- **Albedo** — yer "oynasi" qanchalik yorug'likni qaytaradi. Qor ≈ 0.8 (oq ko'ylak), asfalt ≈ 0.1 (qora ko'ylak). Qaytarilmagan energiya — ET uchun "yoqilg'i".
- **NDVI** — o'simlik "yashilligi". Yashil barg qizil nurni yutadi, NIR ni qaytaradi.
- **LAI** — 1 m² yer ustidagi barglar umumiy maydoni (m²/m²). NDVI dan empirik formula bilan olinadi.
- **Snow/Water flag** — "bu piksel suvmi, qormi yoki quruqlik?" degan savolga javob. Suv va qor energiya balansida butunlay boshqacha "o'ynaydi".

---

## 2. Surface Albedo — `calculate_surface_albedo`

Keng polosali (broadband) albedo — og'irlangan yig'indi (Allen et al., 2007; Tasumi et al., 2008):

$$\alpha = \sum_{b} w_b\,\rho_{s,b} = 0.2545\rho_{blue} + 0.1486\rho_{green} + 0.148\rho_{red} + 0.31\rho_{nir} + 0.1025\rho_{swir1} + 0.0364\rho_{swir2}$$

```python
wb = ee.Image.constant(self.image.get('wb'))
albedo = self.surface_reflectance.multiply(wb)
albedo = (albedo.select([0]).add(albedo.select([1])).add(albedo.select([2]))
          .add(albedo.select([3])).add(albedo.select([4])).add(albedo.select([6])))
```

> 💡 **Nega `reduce(ee.Reducer.sum())` emas?** Kod izohida: reducer tasvirning `footprint`ini yo'qotgan. Shuning uchun bandlar qo'lda qo'shilgan. Index 5 (`thermal`) o'tkazib yuborilgan.

### 2.1 Tall vegetation albedo adjustment — `calculate_albedo_tall_veg_adj`

Daraxtlar (NLCD 41/42/43) va baland ekinlar (bog', tokzor) soyalari tufayli Landsat nadir ko'rinishida **albedo past** chiqadi → ET haddan ortiq. Tuzatish:

**(a) Tall vegetation** (`_tall_veg_flag == 1`):

$$\alpha' = \min\!\Big(\max\big(0.12,\ (1 + (2 - 2\cos\theta)\cdot \tfrac{NDVI}{0.8})\,\alpha\big),\ \max(0.23,\ \alpha)\Big)$$

**(b) Ekin maydonlari** (NLCD 81 pasture / 82 cultivated, $\alpha < \alpha_{min}=0.18$):

$$\alpha' = \alpha + (\alpha_{min} - \alpha)\cdot \mathrm{clamp}\!\left(\frac{NDVI - 0.45}{0.7 - 0.45},\,0,\,1\right)$$

> Tarix (kod izohidan): 2010-yil Allen & Aureo — kuzgi bug'doy albedosi ≥ 0.18 bilan cheklangan, chunki ETrF > 1.05 ga chiqib ketardi.

| Parametr | Default | Ma'no |
|---|---|---|
| `albedo_min` | 0.18 | Ekinlar uchun minimal albedo |
| `albedo_adj_toggle` | 2 | 0=yo'q, 1=tall veg, 2=tall veg + ag |

**Albedo farqi** (keyin LST va Zom tuzatishlarida ishlatiladi):

$$\Delta\alpha = \alpha' - \alpha \qquad (\texttt{calculate\_albedo\_adj})$$

---

## 3. NDVI — `calculate_ndvi`

$$NDVI = \mathrm{clamp}\!\left(\frac{\rho_{nir} - \rho_{red}}{\rho_{nir} + \rho_{red}},\,-1,\,1\right)$$

> ⚠️ **Muhim nuance:** `normalizedDifference()` ishlatilmagan, chunki u [-1,1] dan tashqari qiymatlarni **masklaydi**. Bu yerda esa **clamp** qilinadi → NoData "teshik"lari paydo bo'lmaydi. (SR offset −0.2 tufayli manfiy reflectance bo'lishi mumkin.)

## 4. NDWI — `calculate_ndwi`

$$NDWI = \frac{\rho_{swir1} - \rho_{green}}{\rho_{swir1} + \rho_{green}}$$

(Gao/McFeeters ko'rinishining teskari belgisi; asosiy oqimda kam ishlatiladi.)

## 5. LAI — `calculate_lai`

$$LAI = \min\big(10\cdot \max(NDVI,0)^{3.5},\ 6.0\big)$$

```python
lai = self.ndvi.max(0.0).expression('10.0 * pow(b(), 3.5)').min(6.0)
```

| NDVI | LAI |
|---|---|
| 0.3 | 0.15 |
| 0.5 | 0.88 |
| 0.7 | 2.87 |
| 0.8 | 4.58 |
| ≥0.86 | 6.0 (cap) |

## 6. Percent residue — `calculate_percent_residue`

Aggarwala et al. (1991):

$$R\% = \mathrm{clamp}(788.4\,\rho_{swir1} - 711.5\,\rho_{swir2} - 39.16,\ 10^{-5},\ 100)$$

Maxsus qiymatlar: NLCD 31 (barren) → 0.001; qor → −0.00002; NDVI > 1 → −0.00001.

## 7. Tall vegetation ID — `calculate_tall_veg_id`

```python
tall_veg = ee.Image(0) \
    .where(land_use.eq(41).Or(land_use.eq(42)).Or(land_use.eq(43)), 1) \  # o'rmonlar
    .where(tall_crops_flag.eq(1).And(tall_crops_toggle.eq(1)), 1)          # bog'/tokzor (CDL)
```

`tall_crops_flag` — OpenET crop type kolleksiyasidan (`projects/openet/assets/crop_type/v2024a`) olinadi, faqat CONUS uchun (qarang [05_common_products.md](05_common_products.md)).

---

## 8. Snow / Water flag — `calculate_snow_water_flag`

| Qiymat | Klass |
|---|---|
| 0 | quruqlik |
| 1 | qor |
| 2 | suv |

**Suv sharti:**

$$NDVI < 0.05\ \land\ T_s < T_{cold,dem} + \frac{T_{hot,dem} - T_{cold,dem}}{2}\ \land\ slope < 100$$

(ya'ni piksel sovuq va issiq kalibratsiya piksellarining **o'rtasidan sovuqroq**.)

**Qor sharti:**

$$NDSI = \frac{\rho_{green} - \rho_{swir1}}{\rho_{green} + \rho_{swir1}} \ge 0.4\ \land\ \rho_{green} > 0.2\ \land\ \rho_{nir} > 0.2\ \land\ T_s < 280\,K$$

**Bekor qilish (false positive):** $LAI < 0.5\ \land\ NLCD = 31\ \land\ \alpha < 0.1$ → 0 (qorong'i barren yer, masalan bazalt).

> 🧠 **Muhim bog'liqlik:** suv flagi hot/cold piksel temperaturasiga bog'liq → hot/cold tanlash **avval** bajarilishi kerak. Lazy property zanjiri buni avtomatik hal qiladi.
