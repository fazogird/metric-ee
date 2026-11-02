# 07 — Soil Heat Flux ($G$)

> **Manba fayl:** `soil_heat_flux.py` (`calculate_soil_heat_flux` — tog'li/default, `calculate_soil_heat_flux_flat` — `EEFluxFlat`)

---

## 1. Feynman tushuntirish

Quyosh tushdan tuproq qiziydi — energiyaning bir qismi **yerga "yashirinadi"** (G). Yalang'och tuproq ko'proq qiziydi, qalin o'simlik ostidagi tuproq kamroq (soya). Suv havzalari esa juda katta "issiqlik akkumulyatori" — kunduzi ko'p energiya yutadi.

Asosiy g'oya: $G/R_n$ nisbati LAI ga bog'liq.

---

## 2. Quruqlik uchun G (Allen et al., 2014; Tasumi, 2003)

$$G_{land} = (0.1 + 0.17\,e^{-0.55\,LAI})\,R_n\cdot M_{om}$$

| LAI | G/Rn |
|---|---|
| 0 | 0.27 |
| 1 | 0.20 |
| 3 | 0.13 |
| 6 | 0.106 |

### 2.1 Organik modda / qoldiq multiplikatori $M_{om}$

$R\%$ — percent residue ([02](02_albedo_ndvi_lai.md#6-percent-residue--calculate_percent_residue)), $om = R\%/100$, $s_t$ = strength = 0.5:

$$m_0 = (1 - s_t) + s_t\cdot\max\!\Big(\mathrm{clamp}\big(\tfrac{0.3}{NDVI} - 0.35,0,1\big)\cdot\big(\min(\tfrac{10}{om+10^{-4}},1) - 1\big) + 1,\ 0.1\Big)$$

**Quruq "dry" temperatura chegarasi** (hot va cold piksellar bo'yicha ekstrapolyatsiya, ETrF = 0 nuqtasi):

$$T_{dry} = T_{hot,dem} + K_{c,hot}\frac{T_{hot,dem} - T_{cold,dem}}{K_{c,cold} - K_{c,hot}},\qquad T_{thr} = T_{dry} + 2$$

$$m_{final} = 1 + (m_0 - 1)\cdot\mathrm{clamp}\!\left(1 + \frac{T_{s,dem}^{tv} - T_{thr}}{5},\ 0,\ 1\right)$$

$T_{s,dem}^{tv}$ = `_surface_temperature_dem_tall_veg` (delapsed + tall-veg tuzatilgan).

> Kod: `om_g_multiplier_final.expression('1.0+b()-int(b()+0.95)')`. Bu qism: $b \ge 0.05$ bo'lsa $\to b$, $b < 0.05$ bo'lsa $\to 1 + b$. Amalda $m_{final} \in [0.1, 1]$ bo'lgani uchun **$M_{om} = m_{final}$**.

---

## 3. Maxsus yuzalar

| Yuza | Shart | Formula | Manba |
|---|---|---|---|
| **Suv** | `snow_water_flag == 2` | $G = (-1.25 + 0.0217J - 5.87\times10^{-5}J^2)R_n$ | Manual Eq. 11.5b |
| **Qor** | `snow_water_flag == 1` | $G = 0.5R_n$ | Eq. 11.7 |
| **Wetland** | NLCD 90 / 95 | $G = \mathrm{clamp}\big((0.05 + 0.6e^{-0.8LAI})R_n,\ 0.05R_n,\ -51 + 0.41R_n\big)\cdot M_{om}$ | Table 11.1 |
| **Bazalt** | $LAI<0.5 \land$ NLCD 31 $\land\ \alpha < 0.1$ | $G = \min(2\max(0.4H, 0.15R_n),\ 0.7R_n)\cdot M_{om}$ | — |
| **Muzlagan tuproq** | $T_s < 279$ K, suv/qor/wetland emas | $G \times 1.5\cos s$ (flat: $\times 1.5$) | — |

> ⚠️ **Bazalt G** sensible heat flux $H$ ga bog'liq. Aylanma bog'liqlik (G → H → G) **yo'q**, chunki: (1) pikselli $H$ formulasi $G$ ni ishlatmaydi ($H = \rho c_p dT/r_{ah}$), (2) kalibratsiyada (`gridded_dT.py`) hot/cold piksellar uchun $G$ **alohida**, faqat $G = (0.1 + 0.17e^{-0.55LAI})R_n$ bilan hisoblanadi — `self.soil_heat_flux` chaqirilmaydi. (Batafsil [09](09_sensible_heat_flux.md).)

---

## 4. Juda issiq piksellar uchun G kamaytirish

$$G_{adj} = G - 5\,(T_{s,dem}^{tv} - T_{thr}),\qquad T_{s,dem}^{tv} > T_{thr}$$

Flat versiyada $T_{s,dem}^{tv}$ o'rniga `ts_dem_latlon`.

> Fizik ma'no: hot pikseldan ham issiq yuzalar (asfalt, tosh) — METRIC energiya balansini "yopish" uchun G ni pasaytiradi (aks holda ETrF manfiy).

---

## 5. Suv va qor uchun aerodinamik G (residual)

Suv/qor piksellarida G **qoldiq** sifatida hisoblanadi:

$$G_{aero} = R_n - H - E_{aero}\cdot\frac{\lambda}{3600},\qquad \lambda = (2.501 - 0.002361(T_s - 273))\times10^6\ \mathrm{J/kg}$$

$E_{aero}$ — `_evapor_water` (mm/soat), sensible heat flux modulidan ([09](09_sensible_heat_flux.md)).

```python
Gadj = Gadj.where(self._snow_water_flag.neq(0), G_Aero)
G = Gadj.where(ee.Image.constant(GAdjustmentFlag).eq(0), G_org)   # GAdjustmentFlag = 1 → Gadj
```

> 🧠 Suvda bug'lanish to'g'ridan-to'g'ri aerodinamik formula (Penman tipidagi) bilan hisoblanadi, G esa "qolgan energiya". Bu suv havzalarida (Orol, Chordara, Tuyamuyun) ETrF ni realistik qiladi.

---

## 6. Kod tuzilishi (pseudo)

```python
G_land    = (0.1 + 0.17*exp(-0.55*LAI)) * Rn * M_om
G         = G_land
G         = where(water,   Rn*(-1.25 + 0.0217*doy - 0.0000587*doy²))
G         = where(snow,    0.5*Rn)
G         = where(wetland, clamp((0.05+0.6*exp(-0.8*LAI))*Rn, 0.05*Rn, -51+0.41*Rn)*M_om)
G         = where(basalt,  min(2*max(0.4*H, 0.15*Rn), 0.7*Rn)*M_om)
G         = where(Ts<279 & land, G*1.5*cos(slope))
G         = where(TsDEM_tv > T_thr, G - 5*(TsDEM_tv - T_thr))
G         = where(water|snow, Rn - H - E_aero*λ/3600)
```
