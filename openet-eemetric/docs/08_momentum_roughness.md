# 08 — Momentum roughness length (Zom) va qo'shimcha qarshilik

> **Manba fayl:** `momentum_roughness.py`

---

## 1. Feynman tushuntirish

Shamol silliq muz ustida tez esadi, o'rmon ustida esa "qoqiladi". **Zom** — yuzaning "g'adir-budurlik" o'lchami (m). Zom katta → turbulentlik kuchli → aerodinamik qarshilik $r_{ah}$ kichik → issiqlik (H) osonroq ko'tariladi.

Taxminiy qoida: $Z_{om} \approx 0.12\,h$ (o'simlik balandligining ~12%).

---

## 2. Asosiy Zom — `calculate_zom`

### 2.1 Land use bo'yicha lookup (NLCD → Zom, sm×100)

```python
landUseClass = [11, 12, 21, 22, 23, 24, 31, 41, 42, 43, 51, 52, 71, 72, 81, 82, 83, 84, 85, 86, 90, 94, 95]
landUseZom   = [50, 50, 500,800,1000,2000,200,5000,5000,5000,1000,1000,500,300,1200,1200,1200,200,500,3600,1000,2000,1000]
ZoM = land_use.remap(landUseClass, landUseZom).divide(10000)   # → metr
```

| NLCD | Klass | Zom (m) |
|---|---|---|
| 11 | Suv | 0.005 |
| 12 | Muz/qor | 0.005 |
| 21 | Developed, open | 0.05 |
| 22 | Developed, low | 0.08 |
| 23 | Developed, medium | 0.10 |
| 24 | Developed, high | 0.20 |
| 31 | Barren | 0.02 |
| 41/42/43 | O'rmon | 0.50 |
| 51/52 | Butazor | 0.10 |
| 71 | O'tloq | 0.05 |
| 72 | Sedge | 0.03 |
| 81/82/83 | Pasture/ekin | 0.12 (keyin LAI bilan almashadi) |
| 84 | — | 0.02 |
| 85 | — | 0.05 |
| 86 | — | 0.36 |
| 90 | Woody wetland | 0.10 |
| 94 | — | 0.20 |
| 95 | Herbaceous wetland | 0.10 |

> Kodlar 83–86, 94 — OpenET'ning kengaytirilgan land-use klasslari (CDL bilan birlashtirilgan).

### 2.2 Ekinlar — LAI asosida (Allen et al., 2014, Eq. 43)

$$Z_{om} = 0.018\cdot \max(LAI,\ 0.2778)\qquad (\text{NLCD }81,82,83)$$

$$Z_{om} = 0.5\cdot 0.12\cdot \max(LAI,\ 0.2778)\qquad (\text{NLCD }86)$$

### 2.3 Daraxtlar — Perrier (1982) funksiyasi (Allen et al., 2014, Eq. 2.1)

Barg taqsimot faktori ($f_P = 0.6$):

$$a = \begin{cases} 2f_P, & f_P \ge 0.5 \\ [2(1-f_P)]^{-1}, & f_P < 0.5\end{cases}\quad\Rightarrow a = 1.2$$

$$Z_{om} = \max\!\Big(\big(1 - e^{-a\,LAI/2}\big)\,e^{-a\,LAI/2}\cdot (m\cdot LAI),\ 0.005\Big)$$

| Holat | $m$ (perrier_multiplier) |
|---|---|
| O'rmon (41/42/43) | 2.5 |
| Tall crops (bog'lar) | 1.0 (Allen, 2022-02-01 tavsiyasi) |

Qo'llanish: o'rmon **yoki** (`tall_crops_flag == 1` ∧ `tall_crops_zom_toggle == 1` ∧ **tokzor emas**).

### 2.4 Silliqlash va maxsus holatlar

```python
ZoM = ZoM.where(...).convolve(ee.Kernel.square(2.5, 'pixels'))   # 5×5 o'rtacha
ZoM = ZoM.where(land_use.eq(95), 0.25*max(0.01, NDVI))            # wetland
ZoM = ZoM.where(land_use.eq(21).And(ndvi.gt(0.7)), 0.01)          # sug'oriladigan maysazor/golf
```

> ⚠️ `convolve` faqat lookup + ekin + daraxt qismiga qo'llanadi; wetland va golf maydon qiymatlari **silliqlashdan keyin** yoziladi.

---

## 3. Suv uchun Zom — `calculate_zom_with_water`

Suv yuzasi shamol bilan to'lqinlanadi (Allen et al., 2014, p. 10-8):

$$Z_{om,water} = \max(2.4\times 10^{-7}\,u_{200}^{2.55},\ 0.00005)$$

Faqat `snow_water_flag == 2` piksellarda. Bu yerda $u_{200}$ — **aerodinamik** (pastki chegarasiz) 200 m shamol.

---

## 4. Tog' va albedo uchun Zom tuzatishi — `calculate_zom_adj_general`

**1-qadam.** Qor uchun: $Z' = \dfrac{Z + Z_{water}(u_{200})}{2}$

**2-qadam.** Albedo tuzatilgan (lekin tall veg bo'lmagan) piksellar:

$$Z' = Z \cdot m_{tv}\cdot \left(\frac{\alpha + \Delta\alpha}{\alpha}\right)^2$$

**3-qadam.** Relyef g'adir-budurligi ($\sigma_z$ = DEM standart og'ish, max 200 m; $C_{zom}$ = `czom_adj` = **0.5**):

$$Z'' = Z' + C_{zom}\cdot 3\sin^3\!\left(\frac{\pi}{2}\cdot\frac{\min(\sigma_z,200)}{200}\right)\cdot\left(\frac{Z'}{7} + 0.3\right)$$

Suv va ekin maydonlarida (81/82) 3-qadam qo'llanmaydi.

> 🧠 **Fizik ma'no:** tog' tizmalari o'zi katta "g'adir-budurlik" elementi. $\sigma_z = 200$ m da qo'shimcha ≈ $0.5\cdot 3\cdot(Z/7+0.3)$ ≈ 0.45 m+.

---

## 5. Qo'shimcha aerodinamik qarshilik — `calculate_extra_aerodynamic_resistance`

Allen et al. (2014), Eq. 15.3:

$$r_{extra} = \begin{cases} 0, & u_{200} < 2.6 \\ 0.013u^3 - 0.4351u^2 + 4.2748u - 8.2835, & 2.6 \le u_{200} \le 15 \\ 2.0, & u_{200} > 15\end{cases}$$

```python
rextra = rextra.where(self.land_use.neq(52).Or(self.land_use.neq(71)), 0)
```

> 🐛 **Kod kuzatuvi (bug ehtimoli):** `neq(52).Or(neq(71))` mantiqan **har doim True** (bir piksel bir vaqtda 52 va 71 bo'la olmaydi). Natijada `rextra` **hamma joyda 0**. Ehtimol "faqat butazor (52) va o'tloq (71) uchun" niyat qilingan: `.where(land_use.neq(52).And(land_use.neq(71)), 0)`. `_rextra` kalibratsiyada ham ([09 §2](09_sensible_heat_flux.md#2-kalibratsiya--calculate_gridded_dt)), pikselli $r_{ah}$ da ham qo'shiladi — lekin har doim 0 bo'lgani uchun amalda **o'chirilgan** feature. Tuzatilsa, natijalar (ayniqsa butazor/o'tloq H) o'zgaradi — tuzatishdan oldin validatsiya kerak.
