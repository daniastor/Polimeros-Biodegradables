# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 08:45:48 2021

@author: Usuario Acer
"""

import sys

CampoFnombre = 'Campo' # Nombre el Campo ***

stdout_fileno = sys.stdout
sys.stdout = open(CampoFnombre+str('.lt'), "w") # Guardamos el archivo .LT

# Los archivos .txt con los distintos parametros deben estar escritos así:

#Ejemplo: angulos planos

#linea 1: Secuencia de conexión entre átomos (e.g. atm1-atm2-atm3)
#liena 2: Parametro 1
#   .
#   .
#   .
#liena n: Parametro n
#linea n+1: Otra secuencia de conexión entre átomos (e.g. atm4-atm2-atm3)
#liena n+2: Parametro 1
#   .
#   .
#   .
#liena m: Parametro m
#liena m+1: Secuencia n de conexión entre átomos (e.g. atmi-atmj-atmk)
#   .
#   .
#   .


### LEER parametros de los Archivos

with open('NoEnlazadas_parametros.txt') as f:
    Reporte = f.read().splitlines()
    
s = []
n = 4 #número de parámetros + nombre
for x in range(n):
    s.append(Reporte[x::n])
#print(s)

TipoAtomo = s[0]
ProfundidadLJ = s[1]
DistanciaLJ = s[2]
CargasParciales = s[3]

##

with open('Estiramiento_parametros.txt') as f:
    Reporte1 = f.read().splitlines()
    
s1 = []
l = 3 #número de parámetros + nombre
for x in range(l):
    s1.append(Reporte1[x::l])

Enlace = s1[0]
Kestiramiento = s1[1]
r0 = s1[2]


AtomType1 = []
AtomType2 = []

for i in range(len(Enlace)):
    x = Enlace[i]
    f = x.split("-") 
    AtomType1.append(f[0])
    AtomType2.append(f[1])

##

with open('Flexion_parametros.txt') as f:
    Reporte2 = f.read().splitlines()
    
s2 = []
m = 3 #número de parámetros + nombre
for x in range(m):
    s2.append(Reporte2[x::m])

Angulo = s2[0]
Kflexion = s2[1]
theta0 = s2[2]

StartA = []
Vert = []
EndA = []

for i in range(len(Angulo)):
    x = Angulo[i]
    f = x.split("-") 
    StartA.append(f[0])
    Vert.append(f[1])
    EndA.append(f[2])

##

with open('Torsion_parametros.txt') as f:
    Reporte3 = f.read().splitlines()
    
s3 = []
f = 10 #número de parámetros + nombre
for x in range(f):
    s3.append(Reporte3[x::f])

Dihedros = s3[0]

K1 = s3[1]
n1 = s3[2]
d1 = s3[3]

K2 = s3[4]
n2 = s3[5]
d2 = s3[6]

K3 = s3[7]
n3 = s3[8]
d3 = s3[9]

D1 = []
D2 = []
D3 = []
D4 = []

for i in range(len(Dihedros)):
    x = Dihedros[i]
    f = x.split("-") 
    D1.append(f[0])
    D2.append(f[1])
    D3.append(f[2])
    D4.append(f[3])

###########-----------------Datos de ingreso maual *** ------------##########

# Ingrese la elección de estilos de interaccion LAMMPS ***
# Por favor consulte los estilos en el manual de LAMMPS, ahí le diran ->
# los parametros que necesita definir en las distintas secciones, en  ->
# este caso el codigo lee y escribe los parametros de acuerdo a estos ->
# comandos.

units = 'real'
atom_style = 'full'
bond_style = 'harmonic'
angle_style = 'harmonic'
dihedral_style = 'fourier'

cut1 = ' 12.0' 
#cut2 = ' 8.0'
pair_stylecomand = 'lj/cut/coul/cut'
pair_style = pair_stylecomand + cut1 #+ cut2

##############################################################################

# Ahora el codigo escribira el archivo de campo.lt

# Acontinuación cada sección me representa un "modulo" con datos, por favor,->
# revisar el manual de moltemplate de acuerdo a los titulos de cada sección ->
# y el manual de LAMMPS de acuerdo a los estilos.
# En este codigo solo se programo el reconocimiento (son los condiconales if) ->
# de atomos de Carbono (C), Hidrogeno (H) y Oxigeno (O).

print(CampoFnombre,' {')
print('')
#-----------------------------------------------------------------------------
#                           -o-
#                    Seccion: Estilos de interaccion LAMMPS
print('# -o--- LAMMPS styles ---o-')
print('  write_once("In Init") {')
print('    units',units)
print('    atom_style',atom_style)
print('    bond_style',bond_style)
print('    angle_style',angle_style)
print('    dihedral_style',dihedral_style)
print('    pair_style',pair_style)
print('  } # End of init parameters')
print('')
#                           -o-
##############################################################################
##    
#                       -o-
##                   -o- Seccion: "In Charges" -o-
print('# -o--- Partial Charges ---o-')
# Vamos a asignar las cargas de atomo por tipo de atomo
# Es necesario definir:
    # atomType  charge

atomType = TipoAtomo
charge = CargasParciales

#print
print('  write_once("In Charges") {')
for i in range(len(atomType)):
    print('    set type @atom:'+str(atomType[i]),
          '   charge  ',charge[i])
print('  } # End of atom Partial Charges')
print('')
##                              -o-

##############################################################################
##                              -o-
#  #                -o- Seccion: "Data Masses" -o-
print('# -o--- Data Masses ---o-') 
# Vamos a asignar las masas por tipo de átomo
# Es necesario definir:
    # atomType   mass
print('  # atomType  mass')
  
    # Agregar la masa del elemento: ***
Om = 15.9994 # Oxigeno
Hm = 1.008   # Hidrogeno
Cm = 12.0107 # Carbono

mass = []

for i in range(len(atomType)):
 
    primerl = atomType[i][:1]  #Reconozco el elemento del atomType (es dado ->
                             #por la primera letra)
                             
    # Asigno la masa en orden
    
    if primerl == 'c':  # Reconozco que es un carbonp
        masaC = Cm
        mass.append(masaC)
        
    if primerl == 'h':  # Reconozco que es un hidrogeno
        masaH = Hm
        mass.append(masaH)
        
    if primerl == 'o':  # Reconozco que es un oxigeno
        masaO = Om
        mass.append(masaO)
      
# print:
print('  write_once("Data Masses") {')   
for i in range(len(atomType)):
    print('    @atom:'+str(atomType[i]), mass[i])

print('  } # End of atom Data Masses')
print('')
####                          -o-

##############################################################################
#####                          -o-
##                Seccion: Pairwise (non-bonded) interactions
print('#-o-----Non-Bonded Interactions-----o-')     
##                         "In Settings"
## Ademas de las interacciones enlazadas entre atomos los campos de fuerza ->
## tambien presentan interacciones no enlazadas.
# Es necesario definir:
    #  atomType1  atomType2  epsilon  sigma 
    
epsilon = ProfundidadLJ
sigma = DistanciaLJ
print('#   atomType1     atomType2    epsilon   sigma  charge')
# print
print('  write_once("In Settings") {')
for i in range(len(atomType)):
    print('    pair_coeff',
          ' @atom:'+str(atomType[i]), 
          '@atom:'+str(atomType[i]), ' ',
          epsilon[i], '   ',
          sigma[i], '   ',
          CargasParciales[i])
print('  } # End of pair_coeffs (mixing rules determine interactions between different atoms types)')
print('')
##                         -o-

##############################################################################
##                         -o-
###           Seccion: Bonded Interactions
print('# -o------ Bonded Interactions: ------o-')
##                       "In Settings"
# Buscar más información sobre esto ...   BUSCAR
# Es necesario definir:
    # BondTypeName   k   r0
    
BondTypeName = Enlace 
kb  = Kestiramiento
r_0 = r0

print('#  BondTypeName   BondStyle   k   r0')

print('  write_once("In Settings") {')
for i in range(len(BondTypeName)):
    print('    bond_coeff @bond:'+str(BondTypeName[i]), ' ',
          kb[i], ' ', r_0[i])
    
print('  } # End of bond_coeffs')
print(' ')
###                  "Data Bonds By Type"
# Reglas para asignar tipos de enlaces por tipo de átomo
# Necesitamos definir:
    # BondTypeName      AtomType1         AtomType2
    
print('# BondTypeName      AtomType1         AtomType2')
print('  write_once("Data Bonds By Type") {')
for i in range(len(BondTypeName)):
    print('    @bond:'+str(BondTypeName[i]), 
          '@atom:'+str(AtomType1[i]),
          '@atom:'+str(AtomType2[i]))
print('  } # End of bonds by type')
print(' ')
##                         -o-

##############################################################################
##                         -o-
##                 Section: Angle Interactions
print('# -o----- Angle Interactions -----o-')
#                     "In Settings"
# Necesitamos definir:
      # angle_coeff AngleTypeName     k->kang   theta0
print('# AngleTypeName   AngleStyle  k->kang   theta0')
 
AngleTypeName = Angulo
kang = Kflexion
theta_0 = theta0

print('  write_once("In Settings") {')
for i in range(len(AngleTypeName)):
    print('    angle_coeff @angle:'+str(AngleTypeName[i]),' ',
          kang[i],' ',
          theta_0[i])
print('  } # End of angle_coeffs')
print('')

StartAtom = StartA
Vertex = Vert
EndAtom = EndA

##                "Data Angles By Type"
# Necesitamos definir:
   #   AngleTypeName   StartAtom   Vertex   EndAtom
print('# AngleTypeName     StartAtom    Vertex     EndAtom')
print('  write_once("Data Angles By Type") {')
for i in range(len(AngleTypeName)):
    print('    @angle:'+str(AngleTypeName[i]),' ',
          '@atom:'+str(StartAtom[i]), ' ',
          '@atom:'+str(Vertex[i]),' ',
          '@atom:'+str(EndAtom[i]))
print('  } # End of angles by type')
print('')
#                         -o-

##############################################################################

DihedralTypeName = Dihedros


if len(DihedralTypeName) != 0:
#                         -o-
    #              Seccion: Dihedral Interactions
    ###            Recuerde: dihedral_style = 'charmm' (Consulte en LAMMPS)
    print('# -o---------- Dihedral Interactions  -----------o-')
    
    #                        "In Settings"
    # Necesitamos definir:
          #  DihedralTypeName  k->Kdi  n->ndi d->d_angle
    print('#DihedralTypeName ki ni di')    
    
    mFourier = 3 # numero de terminos que se toman de la serie de Fourier

    print('  write_once("In Settings") {')
    for i in range(len(DihedralTypeName)):
        print('    dihedral_coeff @dihedral:'+str(DihedralTypeName[i]),' ',
              mFourier, ' ',
              K1[i], ' ',
              n1[i], ' ',
              d1[i], ' ',
              K2[i], ' ',
              n2[i], ' ',
              d2[i], ' ',
              K3[i], ' ',
              n3[i], ' ',
              d3[i])
    print('  } # End of dihedral_coeffs')
    print('')
    
    DAtomType1 = D1
    DAtomType2 = D2
    DAtomType3 = D3
    DAtomType4 = D4

    #                   "Data Dihedrals By Type"
    # Necesitamos definir:
        #   DihedralTypeName  DAtomType1  DAtomType2  DAtomType3  DAtomType4
    print('# DihedralTypeName  DAtomType1  DAtomType2  DAtomType3  DAtomType4')
    print('  write_once("Data Dihedrals By Type") {')
    for i in range(len(DihedralTypeName)):
        print('    @dihedral:'+str(DihedralTypeName[i]),' ',
              '@atom:'+str(DAtomType1[i]),' ',
              '@atom:'+str(DAtomType2[i]),' ',
              '@atom:'+str(DAtomType3[i]),' ',
              '@atom:'+str(DAtomType4[i]),' ',)
    print('  } # End of dihedrals by type')
print('')
#                         -o-

#-----------------------------------------------------------------------------

print('')
print('}', '#', CampoFnombre)

sys.stdout.close()
sys.stdout = stdout_fileno

LT = open(CampoFnombre+str('.lt'), "r")
print(LT.read())
