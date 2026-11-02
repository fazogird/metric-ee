"""Uchta METRIC implementatsiyasidagi umumiy formulalarni bir xil kirimda hisoblash.

Formulalar har bir kod bazasida qanday yozilgan bo'lsa, shunday qayta yozilgan:
  eeMETRIC  - Open-ET/openet-eemetric v0.21.0
  Nieto     - hectornieto/pyMETRIC v1.0 (+ pyTSEB)
  WSWUP     - WSWUP/pymetric v0.2.3

Ishga tushirish:  python formulalar_taqqoslash.py   (faqat numpy kerak)
"""
import numpy as np
np.set_printoptions(precision=3)
ndvi = np.array([0.2, 0.4, 0.6, 0.8])
rho_r = np.array([0.15, 0.10, 0.06, 0.04]); rho_n = rho_r*(1+ndvi)/(1-ndvi)
savi = 1.1*(rho_n-rho_r)/(0.1+rho_n+rho_r)
lai_ee = np.minimum(10*np.maximum(ndvi,0)**3.5, 6)
lai_ws_savi = np.clip(11*savi**3, 0, 6)
lai_ws_ndvi = np.clip(7*ndvi**3, 0, 6)
print("NDVI", ndvi); print("SAVI(L=0.1)", savi)
print("LAI eeMETRIC 10*NDVI^3.5", lai_ee); print("LAI WSWUP 11*SAVI^3", lai_ws_savi); print("LAI WSWUP 7*NDVI^3", lai_ws_ndvi)
lai = np.array([0.0, 0.5, 1.0, 2.0, 3.0, 5.0])
print("LAI", lai)
print("G/Rn eeMETRIC 0.1+0.17e^-0.55L", 0.1+0.17*np.exp(-0.55*lai))
Ts, Rn = 305.0, 550.0
ws = np.where(lai>=0.5, 0.05+0.18*np.exp(-0.521*lai), (1.8*(Ts-273.16)+0.084*Rn)/Rn)
print(f"G/Rn WSWUP Tasumi2003 (Ts={Ts},Rn={Rn})", ws)
print("G/Rn Nieto G_form=4: tall 0.04, short 0.10 (LAI-independent)")
fc = np.array([0.0,0.5,1.0]); a=0.2
print("G/Rn Bastiaanssen (Nieto G_form=5), NDVI=",fc, (Ts-273.15)*(0.0038+0.0074*a)*(1-0.98*fc**4))
print("eps0 eeMETRIC 0.95+0.01L", np.where(lai>3,0.98,0.95+0.01*lai))
print("eps0 WSWUP    0.95+L/100", np.where(lai>3,0.98,0.95+lai/100))
print("epsNB WSWUP   0.97+L/300", np.where(lai>3,0.98,0.97+lai/300))
# stability: Paulson vs Brutsaert psi_m at z/L
zl = np.array([-2.0,-0.5,-0.1,0.1,0.5])
def paulson_m(zl):
    out=np.zeros_like(zl)
    u=zl<0; x=(1-16*zl[u])**0.25
    out[u]=2*np.log((1+x)/2)+np.log((1+x**2)/2)-2*np.arctan(x)+np.pi/2
    out[~u]=-5*zl[~u]; return out
def paulson_h(zl):
    out=np.zeros_like(zl); u=zl<0; x=(1-16*zl[u])**0.25
    out[u]=2*np.log((1+x**2)/2); out[~u]=-5*zl[~u]; return out
def brut_m(zl):
    out=np.zeros_like(zl); s=zl>=0
    out[s]=-6.1*np.log(zl[s]+(1+zl[s]**2.5)**(1/2.5))
    y=-zl[~s]; a,b=0.33,0.41; x=(y/a)**(1/3); p0=-np.log(a)+3**0.5*b*a**(1/3)*np.pi/6
    y=np.minimum(y,b**-3)
    out[~s]=np.log(a+y)-3*b*y**(1/3)+b*a**(1/3)/2*np.log((1+x)**2/(1-x+x**2))+3**0.5*b*a**(1/3)*np.arctan((2*x-1)/3**0.5)+p0
    return out
def brut_h(zl):
    out=np.zeros_like(zl); s=zl>=0
    out[s]=-6.1*np.log(zl[s]+(1+zl[s]**2.5)**(1/2.5)); y=-zl[~s]
    out[~s]=((1-0.057)/0.78)*np.log((0.33+y**0.78)/0.33); return out
print("z/L", zl)
print("psi_m Paulson (eeMETRIC, WSWUP)", paulson_m(zl)); print("psi_m Brutsaert (Nieto)", brut_m(zl))
print("psi_h Paulson", paulson_h(zl)); print("psi_h Brutsaert", brut_h(zl))
# cold Kc
for n in [0.6,0.7,0.8,0.9]:
    print(f"NDVI={n}: Kc_cold eeMETRIC={np.clip((n-0.15)/0.65,0.11,1):.3f}  WSWUP=1.05  Nieto(VI=fc~NDVI)={1.05*min(n/0.95,1):.3f}")
