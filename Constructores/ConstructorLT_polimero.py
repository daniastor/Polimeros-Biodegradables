# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 13:44:39 2021

@author: Daniela F. Lopez-Astorquiza
"""
# No utilizar tildes
import moltemplate # MOLTEMPLATE libreria
import math
from math import cos, sin, pi
import numpy as np
import matplotlib.pyplot as plt
import sys

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

# LA función de este codigo es la construción de cadenas poliemericas, ->
# permite a partir las salidas del codigo ConstructorLT_monomero.py, ->
# constuir una cadena con los distintos monómeros siguiendo una curva.

# El átomo de la molecula que se encuentre en el origen de coordendas (0,0,0)
# sera posicionado en el punto sobre la curva.

# Es conveniente mantener Avogadro abierto he ir rotando o variando la
# posición de la molécula desde Avogadro, cuando se le da ejecuar 
# e este codigo ira leyendo el .pdb modificado

# Lo que se debe ingresar se encuentra marcado con ***

Npol = 'polimero' # Le damos un nombre al polimero ***

stdout_fileno = sys.stdout
sys.stdout = open(Npol+str('.lt'), "w") # Guardamos el archivo .LT

# El campo de fuerza esta indirectamente importado desde los archivos de la moleculas
CampoFnombre = 'Campo' # De acuerdo al nombre del campo de fuerza ***

print('# Este archivo contiene la definicion para el polimero', Npol)
print(' ')

# Importamos los archivos de moleculas entre comillas como una lista 
# aquí el orden no resulta importante.

Moleculasarchivos  = ['"mole1.lt"','"mole2.lt"','"mole3.lt"'] # ***

for i in range(len(Moleculasarchivos)):
    print('import',Moleculasarchivos[i])

print('')
print(Npol,'inherits',CampoFnombre,'{')
print(' ')
print('  create_var {$mol}') # Opcional: obligar a todos los monómeros a ->
                             # compartir el mismo ID de molécula, recuerde que ->
                             # en el codigo ConstructorLT_monomero.py se ->
                             # emplea por defecto molID = '...', de manera que ->
                             # esto resulta necesario.

# -o- Generamos la curva que van a seguir los monomeros -o-
#Conviene primero realizar el desarrollo con un monomero pequeño
#siguiendo una linea recta, una vez alineados, luego cambiar al cambiar
# la curva las moleculas la seguiran

# Defino un numero de puntos para dar forma a la curva
N = 20  #Minimo poner 4 puntos ***

# Defino la distancia entre monomeros en nanometros (nm)
Dmonomero = 12 # ***  #Revisar la información extra del constructor monomero

# Mover el polimero (la curva) dentro de la caja (para el final del código)
xm = 5 # ***
ym = 60 # ***
zm = 60 # ***

# Ingresar la forma de la curva de tal manera que este en 3 dimensiones

## -o-o-o-o-o-o-   Curva como linea recta -o-o-o-o-o-o-o-
x_i = np.array([[i+xm, ym, zm] for i in range(0,N*Dmonomero)]) 
# -o-o-o-o-o-o-o-o-o-o-o-o-o-o-

## -o-o-o-o-o-   Curva en forma de espiral   -o-o-o-o-o-o-o-
#zline = np.linspace(0, 20, N)
#xline = np.sin(zline)
#yline = np.cos(zline)

#x_i = np.array([[xline[i]+xm,yline[i]+ym,zline[i]+zm] for i in range(len(xline))])
## -o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-

# -o-o-o-o-o-o- Rotar curvas -o-o-o-o-o-o-o-o-o-
# Angulos de rotacion
angle_x = 0 #quiero realizar una rotacion de 45 en x
angle_y = 0
angle_z = 0

# Conversion a radianes
theta_x = angle_x*pi/180
theta_y = angle_y*pi/180
theta_z = angle_z*pi/180

# Matriz de rotacion
R_x = np.array([[1, 0           ,  0           ],
                [0, cos(theta_x), -sin(theta_x)],
                [0, sin(theta_x),  cos(theta_x)]])
R_y = np.array([[ cos(theta_y), 0, sin(theta_y)],
                [ 0           , 1, 0           ],
                [-sin(theta_y), 0, cos(theta_y)]])
R_z = np.array([[cos(theta_z), -sin(theta_z), 0],
                [sin(theta_z),  cos(theta_z), 0],
                [0           ,  0           , 1]])


# Coordenadas de la curva incial
X = x_i[:,0]
Y = x_i[:,1]
Z = x_i[:,2]

# Roto las coordendas
rotated_x = np.array([np.dot(R_x, vect) for vect in zip(X, Y, Z)])
X = rotated_x[:, 0]
Y = rotated_x[:, 1]
Z = rotated_x[:, 2]
rotated_y = np.array([np.dot(R_y, vect) for vect in zip(X, Y, Z)])
X = rotated_y[:, 0]
Y = rotated_y[:, 1]
Z = rotated_y[:, 2]
rotated_z = np.array([np.dot(R_z, vect) for vect in zip(X, Y, Z)])

xxx = []
for i in range(len(rotated_x[:, 0])):
    fff = [rotated_z[i, 0], rotated_z[i, 1],rotated_z[i, 2]]
    xxx.append(fff)

x_i = np.array(xxx)
#-o-o-o-o-o-o-o-o-o-o-o-o-o




# ## -o- Gráfico -o-
# fig0 = plt.figure()
# ax = plt.axes(projection='3d')
# x = x_i[:,0]
# y = x_i[:,1]
# z = x_i[:,2]
# ax.plot3D(x, y, z, '.-')
# ax.set_title('Curva')
# plt.show()
# ##

# Definimos el numero de monomeros de nuestro polímero.
# Para cadenas de miles o cientos de monomeros
# se recomienda primero simular cadadenas cortas y luego cuando
# se observe que las moleculas estan siguiendo de la forma deseada
# la curva, armar las cadenas largas  quitado los plot de esferas 'Plot con esferas'
# solo tabajar con la visualización de la curva o el modelo de alambres

Nmonomeros = 5 #***

# Suavizamos la curva y redefinimos su número de puntos ->
# para que estos puntos me representen los monomeros.
x_s = moltemplate.interpolate_curve.ResampleCurve(x_i, Nmonomeros, 0.5)

# ## -o- Gráfico -o-

# fig1 = plt.figure()
# ax = plt.axes(projection='3d')
# x = x_s[:,0]
# y = x_s[:,1]
# z = x_s[:,2]
# ax.plot3D(x, y, z, '.-')
# ax.set_title('Curva suavizada')
# plt.show()
#

# Redefinimos el espacio de acuerdo a la distancia que queremos ->
# que exista entre los monomeros
x_s *= Dmonomero / ((math.sqrt(1+0.5**2)*len(x_i)) / (len(x_s)-1))

# ## -o- Grafico -o- #####
# fig2 = plt.figure()
# ax = plt.axes(projection='3d')
x = x_s[:,0]
y = x_s[:,1]
z = x_s[:,2]
# ax.plot3D(x, y, z, '.-')
# ax.set_title('Curva con las posiciones de los monomeros del polimero')
# plt.show()
#


# Controlar la hubicación de las moleculas a los extremos de los polímeros

mover_moleInicial = 8.5  # ***
mover_moleFinal = 0    # ***

x[0] = x[0] + mover_moleInicial
x[len(x)-1] = x[len(x)-1] + mover_moleFinal

# Vamos a emplear moltemplate.genpoly_lt.GenPoly() solo para asociar las -> 
# coordenadas de los nodos (o puntos) de nuestra curva con los monomeros, ->
# los cuales, queremos armar nuestra cadena, adelante definiremos la ->
# secuencia.

gp = moltemplate.genpoly_lt.GenPoly()
gp.coords_multi = [x_s]

# De acuerdo a los nombres las moleculas importadas (omitir poner el .LT), ->
# defino de forma ordenada la secuencia de los monomeros, recuerde que ->
# arriba se definió el numero de monomeros que contiene el polímero.

# Los comandos que se imprimen en la consola como: ->
# move(), rot(), y rotvv(), controlan la posicion de cada monomero, por favor,
# revisar el manual de moltemplate.

# Es posible adicionar estos comandos en la secuencia, para realizar ->
# la rotacion de una molecula en particular, sin embargo, debe  ->
# desabilitar la sección del visualizador debido a que no ->
# se encuentra programado para mostrar estas rotaciones adicionales, ->
# se recomienda rotar la molecula desde avogadro y guardar nuevamente.

Minicial = ['mole1'] # Molecula extermo inicial de la cadena ***
# mole 2 cuenta por 2 uniades de glucosa
Mrepetida =   ['mole2']*(Nmonomeros-2) #  Molecula que se repite***
Mfinal =  ['mole3']   # Molecula extremo final de la cadena***

gp.name_sequence_multi =[Minicial + Mrepetida + Mfinal]  

# Imprimimos en la consola las posiciones de los monomeros ya localizados ->
# en la curva
gp.WriteLTFile(sys.stdout)

# En este código vamos a definir "Data Bond List", que es acorde a la ->
# construcción y estructura del conjunto de códigos desarrollados y dejados -> 
# libres en este repositorio ConstructorLT_campo.py y ->
# ConstructorLT_monomero-py, por favor revisar el manual de Moltemplate.
print(' ')
print('  write("Data Bond List") {')
print(' ')
# Para eso necesitamos definir:
    # EnlaceID  AtomoMonomeroInicial  AtomoMonomerofinal

secu = gp.name_sequence_multi
secuencia = secu[0]
  

EnlaceID = [] # A parti de la secuencia ingresada vamos a definir el EnlaceID

# Ingrese en las lista los nombres de los átomos que se desea conectar, ->
# respetando la secuencia.
#
# Se recomienda tener la visualización 3d generada desde  ->
# ConstructorLT_monomero.py para tener presente los átomos  ->
# que se desean conectar.
#
# Ejemplo: Si queremos enlazar dos moleculas 'CH2' y 'CH3' ->
#          supongamos que el monomero inicial es CH2, entonces busco ->
#          el atomID del atomo que quiero conectar con el monomero final CH3 ->
#          de igual manera busco el atomID del atomo del CH3, con ->
#          el que quiero conectar el CH2.
# En ambos casos el carbono que quiero conectar se llama 'C1', luego
#
# # AtomoMonomeroInicial = ['C1']  y AtomoMonomerofinal = ['C1']
#


Enlace_Minicial_Mrepetida = ['O5','C17'] # O5_mole1 conecta C17_mole2 # ***

AMIMi = [Enlace_Minicial_Mrepetida[0]]
AMFMi = [Enlace_Minicial_Mrepetida[1]]


Enlace_Mrepetida_Mrepetida = ['O8','C17'] # ***

AMIMr = [Enlace_Mrepetida_Mrepetida[0]]*(len(Mrepetida)-1)
AMFMr = [Enlace_Mrepetida_Mrepetida[1]]*(len(Mrepetida)-1)


Enlace_Mrepetida_Mfinal = ['O8','C6'] # ***

AMIMf = [Enlace_Mrepetida_Mfinal[0]]
AMFMf = [Enlace_Mrepetida_Mfinal[1]]

#Atomo monomero inicial 
AtomoMonomeroInicial = AMIMi + AMIMr + AMIMf 

#Atomo monomero final
AtomoMonomerofinal = AMFMi + AMFMr + AMFMf

for i in range(len(secuencia)-1):
    ide1 = secuencia[i][:3] # Reconozco el monomero usalmente esta dado por ->
                           # las 3 primeras letras.
    ide2 = secuencia[i+1][:3]
    EnlacesID = ide1+'_'+ide2
    EnlaceID.append(EnlacesID)

for i in range(len(EnlaceID)):
    print('    $bond:%s_'%i+str(EnlaceID[i]),
          '$atom:mon[%s]/'%i+str(AtomoMonomeroInicial[i]),
          '$atom:mon[%s]/'%(i+1)+str(AtomoMonomerofinal[i]))
print(' ')
print('  } # End Data Bond List')
print(' ')
print('}', '# ', Npol)

sys.stdout.close()
sys.stdout = stdout_fileno

LT = open(Npol+str('.lt'), "r")
print(LT.read())

# Este código fue realizado gracias a la implementación de la libreria de ->
# Moltemplate, existen otras maneras de implementar estas herramientas, esta ->
# forma permite programar directamente con las herramientas por lo que ->
# se puede obrar con mayor libertad y tambien resulta ser la mejor manera.
# para divulgar.

#                    -o-o-o-o- SYSTEM.LT -o-o-o-o-o-o-o

# Finalmente vamos a escribir el archivo del sistema como 'sistema.lt'

# En este parte del código vamos a definir la caja que contiene ->
# nuestro polímero "Data Boundary" (por favor revisar el manual de ->
# Moltemplate) y a construir el archivo final donde queda ->
# importado todo nuestro sistema.

xorigen = '0.0' 
yorigen = '0.0' 
zorigen = '0.0' 

xfinal = '50.0' # ***
yfinal = '20.0' # ***
zfinal = '20.0' # ***

file = open('sistema.lt', "w") #Nombre del archivo ***
file.write('# SYSTEM.LT - Descripcion del sistema \n')
file.write('\n')
file.write('import '+Npol+'.lt'+'\n') # Importar el polimero ***
file.write('\n')
file.write('polymer = new '+ Npol+'\n')
file.write('\n')
file.write('write_once("Data Boundary") { \n')
file.write('   '+xorigen+' '+xfinal+' xlo '+' xhi \n')
file.write('   '+yorigen+' '+yfinal+' ylo '+' yhi \n')
file.write('   '+zorigen+' '+zfinal+' zlo '+' zhi \n')
file.write('} \n')
file.close() 

LT = open('sistema.lt', "r")
print(LT.read())

# Al escribir: 
    # moltemplate.sh -vmd sistema.lt 
# se obtendrá la visualización de nuestra cadena armada en VMD.

##############################################################################
###-----------------Visualizacion del polimero construido------------------###
# Se observa a las moleculas siguiendo la curva y el espacio que las contiene

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

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
#ax.view_init(azim=60, elev=45)
#ax.set_axis_off()

# -o- Visaulización de la caja -o-
# Vamos a definir una función que construya un cubo

xorigen = float(xorigen)
yorigen = float(yorigen)
zorigen = float(zorigen)
xfinal = float(xfinal)
yfinal = float(yfinal)
zfinal = float(zfinal)

def plot_cube(cube_definition):
    cube_definition_array = [
        np.array(list(item))
        for item in cube_definition
    ]

    points = []
    points += cube_definition_array
    vectors = [
        cube_definition_array[1] - cube_definition_array[0],
        cube_definition_array[2] - cube_definition_array[0],
        cube_definition_array[3] - cube_definition_array[0]
    ]
    
    points += [cube_definition_array[0] + vectors[0] + vectors[1]]
    points += [cube_definition_array[0] + vectors[0] + vectors[2]]
    points += [cube_definition_array[0] + vectors[1] + vectors[2]]
    points += [cube_definition_array[0] + vectors[0] + vectors[1] + vectors[2]]

    points = np.array(points)

    edges = [
        [points[0], points[3], points[5], points[1]],
        [points[1], points[5], points[7], points[4]],
        [points[4], points[2], points[6], points[7]],
        [points[2], points[6], points[3], points[0]],
        [points[0], points[2], points[4], points[1]],
        [points[3], points[6], points[7], points[5]]
    ]

   # fig = plt.figure()
   # ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-1,xfinal+1)
    ax.set_ylim(-1,yfinal+1)
    ax.set_zlim(-1,zfinal+1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    #ax.set_title('Curva con las moleculas y la caja contenedor')

    faces = Poly3DCollection(edges, linewidths=1, edgecolors='k')
    faces.set_facecolor((0,0,1,0.1))

    ax.add_collection3d(faces)
    ax.scatter(points[:,0], points[:,1], points[:,2], s=0)
    ax.plot3D(x, y, z, 'r.-') # Plot Curva
    
    #ax.set_xlim(0, 2000)
    #ax.set_ylim(0, 2000) 
    #ax.set_zlim(0, 2000) 

cube_definition = [(xorigen,yorigen,zorigen),(xfinal,0,0),(0,yfinal,0),(0,0,zfinal)]
plot_cube(cube_definition)

# plot de todas las moleculas

for h in range(len(secuencia)):
                
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
    
    for line in open(secuencia[h]+str('.pdb')): # Ingresamos la molécula
        abc = line.split()
        id = abc[0]
        
        if id =='HETATM' or id == 'ATOM':
    
            atomIDG = abc[2] + str(abc[1])
            atomID.append(atomIDG)
            coordXG = abc[5] 
            coordX.append(coordXG)
            coordYG = abc[6]
            coordY.append(coordYG)
            coordZG = abc[7]
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


    
        # Para construir el espacio, entre mas grande la molecula aumentar
    spe = 4  # ***
    (xs,ys,zs) = Esfera(spe,spe,spe,0.5)
    #ax.plot_surface(xs, ys, zs, color="b",alpha=0.0) # Plot con esferas
    (xs,ys,zs) = Esfera(-spe,-spe,-spe,0.5)
    #ax.plot_surface(xs, ys, zs, color="b",alpha=0.0) # Plot con esferas
    
    xc = []
    yc = []
    zc = []
    
    
    for i in range(len(coordX)): # plot de cada punto
    
      xabc = float(coordX[i])+x[h]
      xc.append(xabc)
      yabc = float(coordY[i])+y[h]
      yc.append(yabc)
      zabc = float(coordZ[i])+z[h]
      zc.append(zabc)
      
      
      #Para poner los rotulos
      #ax.text(xabc, yabc, zabc, '%s' % (atomID[i]), va='center', ha='center',zorder=80 ,size=8, color='k') 
    
      ide = atomID[i][:1] 
      
      if ide == 'C':
          T1 = 0.3 #Tamaño de la esfera
          (xs,ys,zs) = Esfera(xabc,yabc,zabc,T1)
          ax.plot_surface(xs, ys, zs, color="grey") # Plot con esferas
              
      if ide == 'H':
          T2 = 0.2 #Tamaño de la esfera
          (xs,ys,zs) = Esfera(xabc,yabc,zabc,T2)
          ax.plot_surface(xs, ys, zs, color="silver") # Plot con esferas
           
      if ide == 'O':
         T3 = 0.2
         (xs,ys,zs) = Esfera(xabc,yabc,zabc,T3)
         ax.plot_surface(xs, ys, zs, color="red") # Plot con esferas
    
    for i in range(len(bondID)):
        da = atomID.index(atomID1[i]) 
        ni = atomID.index(atomID2[i])
        ax.plot3D([xc[da],xc[ni]], [yc[da],yc[ni]], [zc[da],zc[ni]], 'black') # Modelo de alambres




