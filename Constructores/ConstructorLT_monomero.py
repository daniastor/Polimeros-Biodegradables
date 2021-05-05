"""
Created on Thu Mar 11 11:26:15 2021

@author: Dani Astor
"""
# No utilizar tildes
import sys

# Este codigo fue realizado y verificado (mediante los datos disponibles al 
# simular una molecula en Avogadro) para moleculas de enlace simple.

# Lo que se debe ingresar se encuentra marcado con ***

NMol = 'mole1' #Nombre del archivo de la molecula sin el .pbd ***

stdout_fileno = sys.stdout
sys.stdout = open(NMol+str('.lt'), "w") # Guardamos el archivo .LT

print('#Este archivo contiene la definicion para la unidad molecular', NMol)
print('')

# Primero se debe importar los parametros del campo de fuerza empleado, ->
# es de resaltar que este campo tambien debe localizarse en la carpeta ->
# de Moltemplate, donde están el resto de archivos construidos.

# En el caso de emplear el campo OPLSAA por defecto en moltemplate ->
# simplente se nombra, Molteplate lo busca automaticamente en la carpeta ->
# de campos de fuerza.

# Este codigo fue verificado para el campo de fuerza por defecto de ->
# moltemplate OPLSAA, si se desea importar otro campo se recomienda que  ->
# tenga la misma estructura del ejemplo "build_your_own_force_field"  ->
# disponible en los archivos de Moltemplate.

CampoFnombre = 'Campo'   # De acuerdo al nombre del campo de fuerza ***
CampoF = '"Campo.lt"' #Importamos el archivo de campo de fuerza entre comillas ***

print('import',CampoF)
print('')
print('# Ahora definamos la molecula de', NMol)
print('')

# En este código solo vamos a definir "Data Atoms" y "Data Bond List",
# por favor dirigirse al manual de Moltemplate, el resto de parámetros son 
# configurados desde el archivo de campo de fuerza.

# Para eso necesario definir: 
  # atomID   molID   atomType   charge   coordX   coordY   coordZ
# al igual que la conectividad entre los átomos:
  # bondID atomID1 atomID2

#    -o- de Avogadro .PBD a .LT -o-

# Es conveniente que las moléculas leidas, tengan un átomo en el ->
# origen de coordenadas (0,0,0), puede ser el que conecta con otro monomero,->
# para ello en avogadro se puede emplear "Align Molecules" tool ->
# antes de exportar el .pbd

# Mediante el archivo .PDB, de la molecula exportada desde Avogadro podemos:->
# conocer las coordXYZ [en Angstroms] y la secuencia en que van concetados ->
# los átomos, tambien emplearemos la infomación disponible para definir ->
# el nombre del átomo atomID y el nombre del enlace bondID. 
                      
atomID = []
coordX = []
coordY = []
coordZ = []

bondID = []
atomID1 = []
atomID2 = []

# Todos estos datos extraidos del .pdb pueden ser cooroborados con los ->
# diponibles en el display de Avogadro "view -> properties"

aa1 = []
enlaces = []

for line in open(NMol+str('.pdb')): # Ingresamos la molécula
    list = line.split()
    id = list[0]
    
    if id =='HETATM' or id == 'ATOM':

        atomIDG = list[2] + str(list[1])
        atomID.append(atomIDG)
        coordXG = list[5] 
        coordX.append(coordXG)
        coordYG = list[6]
        coordY.append(coordYG)
        coordZG = list[7]
        coordZ.append(coordZG)
        #print(atomIDG, coordXG, coordYG, coordZG)
        
    
    # Encuentro todos los enlaces [atomID1, atomID2], luego borro las tuplas
    #  repetidas y las equivalente ([atomID1, atomID2] = [atomID2, atomID1])
    if id == 'CONECT':
        
        con = line.split()
        #print(con)
        
        lcon = len(con)
        
        if lcon  > 3:
            for i in range(2,lcon):
                a1 = [atomID[int(con[1])-1],atomID[int(con[i])-1]]
                aa1.append(a1)
        
        if lcon == 3 :
            b1 = [atomID[int(con[1])-1],atomID[int(con[2])-1]]
            aa1.append(b1)
            
# Borrar tuplas repetidas
for i in aa1: 
    if i not in enlaces: 
        enlaces.append(i)
        
#Borrar tuplas equivalentes 
atomID1_atomID2, k = [], set()
for item in enlaces:
    t1 = tuple(item)
    if t1 not in k and tuple(reversed(item)) not in k:
        k.add(t1)
        atomID1_atomID2.append(item)

#print(atomID1_atomID2)
for i in range(len(atomID1_atomID2)):
    
    atom = atomID1_atomID2[i]
    atomID1.append(atom[0])
    atomID2.append(atom[1])
    
    bond = atom[0]+'-'+atom[1]
    bondID.append(bond)


# Respecto al nombre de la molécula molID se nombra por defecto como " ... "->
molID = '...'
# La carga " charge " por defecto queda como 0.0 para emplear el campo -> 
# generado por el ConstructorLT_campo.py, el campo OPLSAA tambien funciona ->
# de esta manera.
charge = 0.0
#atomType
atomType = '...' #*** Ingrese de forma manual en los archivos salida
                 # de acuerdo con su Campo de fuerza

# El atomType depende de como se encuentre rotulado en el archivo de campo-> 
# de fuerza empleado, en nuestro caso este código se encarga de rotular ->
# de manera automatica para los archivos de campo generdos ->
# con el constructor ConstructorLT_campo.py 

print(NMol,'inherits',CampoFnombre,'{')
print('')
print('  write("Data Atoms") {')
print('  # atomID   molID   atomType  charge   x      y     z')
for i in range(len(atomID)):
    print('    $atom:'+str(atomID[i]),
          '$mol:'+str(molID),
          '@atom:'+str(atomType),
          ' '+str(charge),
          ' '+str(coordX[i]),
          ' '+str(coordY[i]),
          ' '+str(coordZ[i]))
print('  }')
print()
print('  write("Data Bond List") {')
for i in range(len(bondID)):
    print('    $bond:'+str(bondID[i]),
          '$atom:'+str(atomID1[i]),
          '$atom:'+str(atomID2[i]))
print('  }')
print('} #', NMol)

sys.stdout.close()
sys.stdout = stdout_fileno

LT = open(NMol+str('.lt'), "r")
print(LT.read())

# -o- Representación de la molecula en el modelo de esferas duras -o-

# Esta representación resulta útil para visualizar como quedaron rotulados (atomID)
# los átomos en la molécula y mediante su observación conocer el tipo de átomo, 
# por ejemplo, si se trata de un carbono primario o secundario o ... y así 
# establecer con mayor facilidad el atomType.
# Tambien resulta útil en la construcción del polimero para conocer los átomos
# con los que se desea crear el enlace.

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# -o-
def Esfera(xCi, yCri, zCi, ri):
    #Dbujar esfera
    N = 10
    u = np.linspace(0, 2 * np.pi, N)
    v = np.linspace(0, np.pi, N)
    xi = np.outer(np.cos(u), np.sin(v))
    yi = np.outer(np.sin(u), np.sin(v))
    zi = np.outer(np.ones(np.size(u)), np.cos(v))
    # Centrar
    xi = ri*xi + xCi
    yi = ri*yi + yCri
    zi = ri*zi + zCi
    return (xi,yi,zi)
#-o-

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Para construir el espacio, entre mas grande la molecula aumentar
spe = 2
(xs,ys,zs) = Esfera(spe,spe,spe,0.5)
ax.plot_surface(xs, ys, zs, color="b",alpha=0.0)
(xs,ys,zs) = Esfera(-spe,-spe,-spe,0.5)
ax.plot_surface(xs, ys, zs, color="b",alpha=0.0)

ax.set_axis_off()

xc = []
yc = []
zc = []

for i in range(len(coordX)): # plot each point + it's index as text above

  x = float(coordX[i])
  xc.append(x)
  y = float(coordY[i])
  yc.append(y)
  z = float(coordZ[i])
  zc.append(z)
  
  ax.text(x, y, z, '%s' % (atomID[i]), va='center', ha='center',zorder=50 ,size=8, color='k') #Rotulos
  
  #coord = str(x) + ', ' + str(y) + ', ' + str(z)
  #ax.text(x, y, z-0.1, coord, size=10, zorder=7, color='k') #coordenadas asociadas
  
  #Esferas en general
  #ax.scatter(x, y, z,s=40, color='b') 
  
  # Colorear las esferas identificando elementos
  # Se ha programado solo para carbonos, hidrogenos y oxigenos
  
  ide = atomID[i][:1] # Reconozco el elemento del atomID (es dado ->
                      # por la primera letra)
  

  #print(ide) # ejemplo, me muestra la H de hidrogeno o la C de carbono
  if ide == 'C':
      T1 = 0.3 #Tamaño de la esfera
      (xs,ys,zs) = Esfera(x,y,z,T1)
      ax.plot_surface(xs, ys, zs, color="grey")
          
  if ide == 'H':
      T2 = 0.2 #Tamaño de la esfera
      (xs,ys,zs) = Esfera(x,y,z,T2)
      ax.plot_surface(xs, ys, zs, color="silver")
       
  if ide == 'O':
     T3 = 0.2
     (xs,ys,zs) = Esfera(x,y,z,T3)
     ax.plot_surface(xs, ys, zs, color="red")
      
# Los atomID1 me contienen los atomos que por decirlo así me marcan el ->
# comienzo del enlace, mientras que los atomos atomID2 son lo que ->
# me marcan el final, de manera que los enlaces los puedo grafiacar ->
# como pares de puntos unidos.

for i in range(len(bondID)):
    da = atomID.index(atomID1[i]) # Esto es un buscador dentro del atomID, ->
                                  # por ejemplo, atomID1[i] = 'C1' ->
                                  # entonces .index me busca la posición ->
                                  # del elemento 'C1' en atomID y ->
                                  # a esa misma posición en las listas de ->
                                  # coordenasdas estaran asociadas ->
                                  # coordenadas xyz.
    ni = atomID.index(atomID2[i])
    ax.plot3D([xc[da],xc[ni]], [yc[da],yc[ni]], [zc[da],zc[ni]], 'black')
    
ax.view_init(60, 35)
plt.show()

# Información extra de la molecula

# Dimensiones de la molecula
LongitudEnX = abs(min(xc)) + abs(max(xc))
LongitudEnY = abs(min(yc)) + abs(max(yc))
LongitudEnZ = abs(min(zc)) + abs(max(zc))

print('# Informacion extra de la molecula')
print('#la distancia entre el primer atomo y el ultimo en "x" es: ', LongitudEnX, 'Angstroms')
print('#la distancia entre el primer atomo y el ultimo en "y" es: ', LongitudEnY, 'Angstroms')
print('#la distancia entre el primer atomo y el ultimo en "z" es: ', LongitudEnZ, 'Angstroms')

