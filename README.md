# metric-ee

**METRIC** energiya balansi modelining turli Python implementatsiyalari bo'yicha kod tahlillari: formulalar, funksiyalar va algoritmlar O'zbek tilida, Feynman uslubida.

Har bir model **alohida papkada** joylashgan va alohida git tag bilan belgilangan. Formulalar va belgilashlar bir-biriga aralashmaydi: har papka o'zicha to'liq.

| Papka | Model | Manba | Platforma | Git tag |
|---|---|---|---|---|
| [`openet-eemetric/`](openet-eemetric/README.md) | **OpenET eeMETRIC** v0.21.0 | [Open-ET/openet-eemetric](https://github.com/Open-ET/openet-eemetric) | Google Earth Engine | `openet-eemetric-v0.21.0` |
| [`pymetric-nieto/`](pymetric-nieto/README.md) | **pyMETRIC** (Hector Nieto, IRTA) v1.0 | [hectornieto/pyMETRIC](https://github.com/hectornieto/pyMETRIC) | Lokal raster (GDAL + pyTSEB) | `pymetric-nieto-v1.0` |
| [`pymetric-wswup/`](pymetric-wswup/README.md) | **pymetric** (WSWUP / DRI) v0.2.3 | [WSWUP/pymetric](https://github.com/WSWUP/pymetric) | Lokal Landsat pipeline (GDAL + NumPy) | `pymetric-wswup-v0.2.3` |

> 📜 Umumiy ilmiy asos: Allen, R.G., Tasumi, M., Trezza, R. (2007). *Satellite-Based Energy Balance for Mapping Evapotranspiration with Internalized Calibration (METRIC) — Model*. J. Irrig. Drain. Eng., 133(4), 380–394.

## Tag bo'yicha yuklab olish

```bash
git clone https://github.com/fazogird/metric-ee.git
```

```bash
git checkout openet-eemetric-v0.21.0
```

## Litsenziya eslatmasi

Tahlil qilingan kodlarning litsenziyalari har xil: eeMETRIC **AGPL-3.0**, pyMETRIC (Nieto) **GPL-3.0**, WSWUP pymetric **Apache-2.0**. Batafsilini har papkaning README sidan qarang. Bu repozitoriyada faqat tahliliy hujjatlar va qisqa kod iqtiboslari bor.
