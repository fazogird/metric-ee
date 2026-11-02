# 02 — METRIC yadrosi: `METRIC.METRIC()` (pyMETRIC, Nieto)

> **Manba:** `pyMETRIC/METRIC.py` (37–347-qatorlar), pyTSEB `MO_similarity`, `resistances`, `meteo_utils`

---

## 1. Feynman tushuntirish

Funksiya ikki bosqichda ishlaydi:

1. **Kalibratsiya (2 ta piksel):** cold va hot nuqtada $H = R_n - G - LE_{ref}$ ma'lum. Ulardan $dT = H\,R_A/(\rho c_p)$ topiladi. Muammo shundaki, $R_A$ atmosfera barqarorligiga (L) bog'liq, L esa H ga bog'liq. Shuning uchun "tovuq va tuxum" iteratsiyasi qilinadi: L → u* → L → ... (≤15 marta).
2. **Tasvir (barcha piksellar):** chiziqli $dT(T_R)$ bilan har piksel uchun H topiladi. Keyin $LE = R_n - G - H$ va yana L iteratsiyasi. Bu bosqichda tebranishni ushlaydigan "aqlli" konvergensiya testi ishlatiladi.

---

## 2. Signatura

```python
flag, Ln, LE, H, G, R_A, u_friction, L, n_iterations = METRIC(
    Tr_K, T_A_K, u, ea, p, Sn, L_dn, emis, z_0M, d_0, z_u, z_T,
    cold_pixel, hot_pixel, LE_cold, LE_hot=0,
    use_METRIC_resistance=True, calcG_params=[[1], 0.35],
    UseL=False, UseDEM=False)
```

| Kirim | Birlik | Izoh |
|---|---|---|
| `Tr_K`, `T_A_K` | K | radiometrik LST va havo harorati |
| `u` | m/s | `z_u` balandlikda |
| `ea`, `p` | **mb** | |
| `Sn`, `L_dn` | W/m² | |
| `z_0M`, `d_0`, `z_u`, `z_T` | m | |
| `cold_pixel`, `hot_pixel` | index | massiv indeksi (tuple yoki 1-D int) |
| `LE_cold`, `LE_hot` | W/m² | massiv: `LE_cold[cold_pixel]` olinadi |
| `UseL` | bool / son | son bo'lsa L majburlanadi, iteratsiya = 1 |
| `UseDEM` | bool / massiv | massiv (balandlik) bo'lsa datum tuzatishi |

Skalyar kirimlar `tseb._check_default_parameter_size` bilan `Tr_K` shakliga yoyiladi. O'lcham mos kelmasa — `ValueError`.

---

## 3. Umumiy kattaliklar

| Kattalik | Formula | Funksiya |
|---|---|---|
| Havo zichligi | $\rho = \dfrac{100p}{R_dT_A}\left(1 - 0.378\dfrac{e_a}{p}\right)$, $R_d = 287.04$ | `met.calc_rho` |
| Solishtirma namlik | $q = \dfrac{0.622e_a}{p - 0.378e_a}$ | `met.calc_c_p` ichida |
| Issiqlik sig'imi | $c_p = (1 - q)\,1003.5 + q\,1865$ | `met.calc_c_p` |
| Datum (agar `UseDEM`) | $T_{datum} = T + \Gamma_w z$ | [01 §8](01_kirish_va_radiatsiya.md#8-datum-adiabatik-temperaturalar) |
| $\rho_{datum}$ | $\rho(p, e_a, T_{A,datum})$ | |
| $z_{0H}$ | $z_{0M}e^{-kB}$, $kB = 0$ | `res.calc_z_0H` |

**Net radiation:**

$$L_n = \varepsilon L_{dn} - \varepsilon\sigma T_R^4,\qquad R_n = S_n + L_n$$

> Bu yerda qaytgan uzun to'lqin $(1-\varepsilon)L_{dn}$ hisobga olingan: $L_{dn} - (1-\varepsilon)L_{dn} - \varepsilon\sigma T^4 = \varepsilon L_{dn} - \varepsilon\sigma T^4$ ✔️

**G:** `tseb.calc_G([calcG_params[0], calcG_array], Rn, i)` ([01 §9](01_kirish_va_radiatsiya.md#9-soil-heat-flux-variantlari)).

---

## 4. Monin–Obukhov (pyTSEB)

### 4.1 Friction velocity — `MO.calc_u_star`

$$u_* = \frac{k\,u}{\ln\!\left(\frac{z_u - d_0}{z_{0M}}\right) - \Psi_M\!\left(\frac{z_u - d_0}{L}\right) + \Psi_M\!\left(\frac{z_{0M}}{L}\right)},\qquad u_* \ge 0.01$$

Boshlanishda $L = \infty$ (neytral) → $\Psi = 0$.

### 4.2 Obukhov uzunligi — `MO.calc_L` → `calc_mo_length_hv` (virtual issiqlik oqimi)

$$E = \frac{LE}{\lambda},\quad \lambda = 10^6(2.501 - 2.361\times10^{-3}(T_A - 273.15))$$

$$H_v = H + 0.61\,T_A\,c_p\,E,\qquad L = -\frac{u_*^3}{\dfrac{kg}{T_A}\cdot\dfrac{H_v}{\rho c_p}},\quad g = 9.8$$

$H_v = 0 \Rightarrow L = \infty$.

> 🧠 Klassik METRIC'da $L = -\rho c_pu_*^3T/(kgH)$. Bu yerda esa namlikning suzuvchanlikka ta'siri ($0.61T c_p E$) qo'shilgan — Brutsaert (2005).

### 4.3 Stabillik funksiyalari — Brutsaert (2005)

$\zeta = z/L$.

**Barqaror ($\zeta \ge 0$), $\Psi_M = \Psi_H$:**

$$\Psi = -6.1\ln\!\left(\zeta + (1 + \zeta^{2.5})^{1/2.5}\right)$$

**Beqaror ($\zeta < 0$), $y = -\zeta$:**

$$\Psi_H = \frac{1 - 0.057}{0.78}\ln\frac{0.33 + y^{0.78}}{0.33}$$

$$\Psi_M = \ln(a + y) - 3by^{1/3} + \frac{ba^{1/3}}{2}\ln\frac{(1+x)^2}{1 - x + x^2} + \sqrt3ba^{1/3}\arctan\frac{2x - 1}{\sqrt3} + \Psi_0$$

bunda $a = 0.33$, $b = 0.41$, $x = (y/a)^{1/3}$, $y \le b^{-3}$, $\Psi_0 = -\ln a + \sqrt3ba^{1/3}\pi/6$.

> pyTSEB'da `psi_m_dyer` / `psi_h_dyer` (Paulson–Dyer, $\gamma = 16$, $\beta = 5$) ham bor, lekin default — **Brutsaert**.

### 4.4 Aerodinamik qarshilik — `res.calc_R_A` (Norman et al., 1995)

$$R_A = \frac{\ln\!\left(\frac{z_T - d_0}{z_{0H}}\right) - \Psi_H\!\left(\frac{z_T - d_0}{L}\right) + \Psi_H\!\left(\frac{z_{0H}}{L}\right)}{k\,u_*}$$

| Rejim | $z_T$ | $d_0$ | $z_{0H}$ |
|---|---|---|---|
| `use_METRIC_resistance is True` (Allen) | 2.0 | 0 | 0.1 |
| aks holda (Kustas & Norman 1999) | piksel `z_T` | piksel `d_0` | piksel $z_{0H}$ |

> 🐛 Konfiguratsiyadan kelgan `1` — `int`, `True` emas. `1 is True` → **False**. Shuning uchun config orqali ishlatganda doim KN99 rejimi tanlanadi ([06](06_kuzatuvlar.md) #1).

---

## 5. 1-bosqich: endmember kalibratsiyasi

```python
H_endmembers = Rn_end - G_end - LE_end                  # calc_H_residual
for iteration in range(15):
    if all(L_diff < 0.001): break
    L_end  = MO.calc_L(u*_end, Ta_datum_end, rho_datum_end, c_p_end, H_end, LE_end)
    L_diff = |L_end - L_old| / |L_old|
    u*_end = max(0.01, MO.calc_u_star(u_end, z_u_end, L_end, d_0_end, z_0M_end))
R_A_end = calc_R_A(...)                                   # §4.4
dT_end  = H_end * R_A_end / (rho_datum_end * c_p_end)    # calc_dT, Allen 2007 Eq. 46
```

**dT chizig'i** (kodda nomlari Allen 2007 dagidan almashtirilgan):

$$b = \frac{dT_{hot} - dT_{cold}}{T_{R,datum}^{hot} - T_{R,datum}^{cold}},\qquad a = dT_{hot} - b\,T_{R,datum}^{hot}$$

$$\boxed{dT = a + b\,T_{R,datum}}\qquad(\text{Allen 2007 Eq. 29})$$

> Kod izohi: *"the equations for a and b in the Allen 2007 paper (eq 50 and 51) appear to be wrong"*. Bu yerda `dT_b` — qiyalik, `dT_a` — kesishma.

> ⚠️ Kalibratsiyada **mahalliy shamol** `u` (`z_u` balandlikda) ishlatiladi, 200 m blending height emas. Hot va cold pikselning $u$, $z_{0M}$, $d_0$ qiymatlari o'zinikidir.

---

## 6. 2-bosqich: barcha piksellar

```python
for n in range(15):
    i = ~L_converged
    R_A[i] = calc_R_A(...)                      # faqat KN99 rejimida (bug #1 ga qarang)
    H[i]   = rho[i] * c_p[i] * dT[i] / R_A[i]   # calc_H, Allen 2007 Eq. 28
    LE[i]  = Rn[i] - G[i] - H[i]
    L[i]   = MO.calc_L(u*[i], T_A_K[i], rho[i], c_p[i], H[i], LE[i])
    u*[i]  = max(0.01, MO.calc_u_star(u[i], z_u[i], L[i], d_0[i], z_0M[i]))
    # konvergensiya testi (pastda)
```

$$H = \frac{\rho\,c_p\,dT}{R_A},\qquad LE = R_n - G - H$$

> Pikselda $\rho$ — **haqiqiy** $T_A$ bo'yicha ($\rho_{datum}$ emas), dT esa datum temperaturadan.

### 6.1 Tebranishga chidamli konvergensiya

`L_queue = deque(maxlen=6)` — oxirgi 6 ta L. Nisbiy farq: $\Delta(L_1, L_2) = |L_1 - L_2|/|L_2|$ (NaN → ∞). Piksel quyidagi uch shartdan **biri** bajarilsa yaqinlashgan deb belgilanadi:

| Test | Shart | Ushlaydi |
|---|---|---|
| 1 | $\Delta(L_0, L_1) < 0.001$ | oddiy yaqinlashish |
| 2 (≥4 qiymat) | $\Delta(L_0,L_2) < \epsilon \land \Delta(L_1,L_3) < \epsilon$ | 2 holat orasida tebranish |
| 3 (6 qiymat) | $\Delta(L_0,L_3), \Delta(L_1,L_4), \Delta(L_2,L_5) < \epsilon$ | 3 holatli tsikl |

> 🧠 **Feynman:** mayatnik ikki nuqta orasida abadiy tebranishi mumkin. "Oxirgi qiymat oldingisiga tengmi?" degan savol bunday holatda hech qachon "ha" javobini olmaydi. Shuning uchun "2–3 qadam orqadagisiga tengmi?" deb ham so'raladi. Bu oddiy METRIC'larda yo'q bo'lgan, juda amaliy yechim.

`iterations` — har pikselning iteratsiya soni. `flag` — hammasi 0 (ishlatilmaydi). `PyMETRIC` da aoi'dan tashqari piksellar uchun 255.

---

## 7. Yordamchi funksiyalar

| Funksiya | Formula | Allen 2007 |
|---|---|---|
| `calc_dT(H, R_AH, rho, c_p)` | $HR_{AH}/(\rho c_p)$ | Eq. 46, 49 |
| `calc_H(dT, rho, cp, R_AH)` | $\rho c_pdT/R_{AH}$ | Eq. 28 |
| `calc_H_residual(Rn, G, LE=0)` | $R_n - G - LE$ | |
| `calc_G_Allen(Rn, LST, albedo, NDVI)` | $R_n(T - 273.15)(0.0038 + 0.0074\alpha)(1 - 0.98NDVI^4)$ | Eq. 26 |
| `_L_diff(L, L_old)` | nisbiy farq, NaN→∞ | |

---

## 8. `PyMETRIC._call_flux_model` — qanday chaqiriladi

```python
METRIC.METRIC(T_R1[i], T_A1[i], u[i], ea[i], p[i], R_ns1[i], L_dn[i], emiss[i],
              z_0M[i], d_0[i], z_u[i], z_T[i],
              cold_pixel, hot_pixel,                       # aoi ichidagi 1-D indeks
              ET_r_f_cold[i] * ET0_datum[i],               # LE_cold massivi
              LE_hot = ET_r_f_hot[i] * ET0_datum[i],
              use_METRIC_resistance = self.use_METRIC_resistance,   # int!
              calcG_params = ..., UseDEM = alt[i])
```

`i` — aoi (landcover guruhi) maskasi bo'lgani uchun massivlar 1-D. Endmember indekslari ham shu 1-D aoi ichidagi indekslar. `ET0_datum` — `pet_asce` dan W/m² dagi **LE** ([04](04_reference_et.md)).

Oxirida (`run_METRIC`):

$$R_{n1} = R_{ns1} + R_{nl1},\qquad fETr = \frac{LE_1}{ET_0}$$
