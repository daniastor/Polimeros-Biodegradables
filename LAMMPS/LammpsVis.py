# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 20:54:48 2021

@author: Usuario Acer
"""

import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
import numpy as np
plt.rcParams.update({'font.size': 14})

with open("log.tension_ResultadoT") as f:
    Reporte = f.read().splitlines()
     
J = [r.split() for r in Reporte]
J[:] = [x for x in J if x]          # Eliminamos todas las string vacias

for i in range(len(J)):
    a = J[i]
    if a[0]=="Step":
        n = i
    if a[0]=="Loop":
        m =i

Datos = J[n:m]


v1 = []
v2 = []
v3 = []
v4 = []
v5 = []
v6 = []
v7 = []
v8 = []
v9 = []
v10 = []
v11 = []

for j in range(1,len(Datos)):
    rf = Datos[j]
    rff = []
    for i in range(len(rf)):
        t = float(rf[i])
        rff.append(t)
        
    v1.append(rff[0])
    v2.append(rff[1])
    v3.append(rff[2])
    v4.append(rff[3])
    v5.append(rff[4])
    v6.append(rff[5])
    v7.append(rff[6])
    v8.append(rff[7])
    v9.append(rff[8])
    v10.append(rff[9])
    v11.append(rff[10])
    
Step = v1
Time = v2
PotEng = v3
KinEng = v4
TotEng = v5
E_vdwl = v6
E_coul = v7
E_bond = v8
E_angle = v9
E_dihed = v10
Density = v11

Bb = []
# Convertir el tiempo de femtosegundos a nanosegundos
for i in range(len(Time)):
    T = Time[i]/(1*10**6)
    Bb.append(T)

Time = Bb


### Energías
plt.figure()
plt.tick_params(labelsize=14)

plt.plot(Time,TotEng,'c-.',label="Energía total",alpha=0.5)
plt.plot(Time,KinEng,'r-.',label="Energía cinética",alpha=0.5)
plt.plot(Time,PotEng,'b-.',label="Energía potencial total",alpha=0.5)
plt.plot(Time,E_vdwl,'-.',label="Energía Van der Waals",alpha=0.5)
plt.plot(Time,E_coul,'y-.',label="Energía electrostatica",alpha=0.5)
plt.plot(Time,E_bond,'m-.',label="Energía estiramiento",alpha=0.5)
plt.plot(Time,E_angle,'k-.',label="Energía flexión",alpha=0.5)
plt.plot(Time,E_dihed,'g-.',label="Energía torsión",alpha=0.5)



plt.xlabel("Tiempo [ns]")
plt.ylabel("Energía [Kcal/mole]")


#plt.ylim(-10, 700)
#plt.xlim(0,10)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

plt.show()


# Densidad

plt.figure()

plt.tick_params(labelsize=14)

plt.plot(Time, Density,'-')

plt.xlabel("Tiempo [ns]")
plt.ylabel("Densidad [g/cm$^3$]")

plt.show()


# ######## Tension en X

with open("tensiongraf_ResultadoT.dat") as f:
    ReporteTension = f.read().splitlines()

JR = [r.split() for r in ReporteTension]
#JR[:] = [x for x in JR if x]          # Eliminamos todas las string vacias   
JR = JR[1:]

Deformacion = []
Esfuerzo = []

for i in range(len(JR)):
    aR = JR[i]
    Deformacion.append(float(aR[0]))
    Esfuerzo.append(float(aR[1]))

fig, ax1 = plt.subplots()


ax1.plot(Deformacion, Esfuerzo, c='b', lw=2, alpha=0.5)
ax1.plot(Deformacion[4:40],Esfuerzo[4:40],'r', alpha=0.5)

ax1.set_xlabel("Deformación") #Strain
ax1.set_ylabel("Esfuerzo [MPa]") #stress

ax2 = plt.axes([0,0,1,1])
ip = InsetPosition(ax1, [0.45,0.12,0.5,0.5])
ax2.set_axes_locator(ip)
mark_inset(ax1, ax2, loc1=2, loc2=4, fc="none", ec='0.5')
ax2.plot(Deformacion, Esfuerzo, c='b', lw=2, alpha=0.5)
ax2.plot(Deformacion[4:40],Esfuerzo[4:40],'r', alpha=0.5)

# controla los timites de la cajita del plot chiquito
ax2.set_xlim(0,0.05)
ax2.set_ylim(0, 7.5)
#

ax2.set_yticks(np.arange(0,7.5,0.8))
ax2.set_xticklabels(ax2.get_xticks(), backgroundcolor='w')
ax2.tick_params(axis='x', which='major', pad=8)

plt.show()

# Young's Modulo stress/strain

Young = []

for i in range(len(Esfuerzo)):
    Y = Esfuerzo[i]/Deformacion[i]
    Young.append(Y)

asintotay = [200]*len(Deformacion[4:40])

plt.figure()
plt.plot(Deformacion[4:40],Young[4:40],'c-.',label='Módulo de Young')
plt.plot(Deformacion[4:40],asintotay,'k-', alpha=0.5,label='Recta horizontal')
plt.legend()

plt.xlabel("Deformación") #Strain
plt.ylabel("Módulo de Young [MPa]") #stress

plt.ylim(0,500)
plt.show()

