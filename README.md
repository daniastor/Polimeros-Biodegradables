# Construcción de largas cadenas poliméricas para LAMMPS

Es posible emplear la arquitectura de [Moltemplate](https://www.moltemplate.org/) para construir una base de datos que describa un modelo molecular, a su vez Moltemplate permite convertir esta base de datos en una entrada para [LAMMPS](https://lammps.sandia.gov/).

En este tuturial se explica el desarrollo de un conjunto de códigos llamados “constructores” que me permiten llenar los archivos de formato LT de Moltemplate con la información geométrica y de campos de fuerza de las moléculas del polímero, a partir del procesamiento de datos de las unidades representativas. Nombramos unidades representativas a todas las unidades moleculares diferentes (se encuentren repetidas o no) que conforman el polímero, en el caso de la amilosa (Fig. 1).

<p align="center">
<img src="https://github.com/daniastor/Polimeros-Biodegradables/blob/main/Imagenes/Estructura_Amilosa.PNG" width="600" height="">
</p>
<p align="center">
Figura 1. Estructura química de la amilosa.
</p>

Podemos tomar como unidades representativas: las moléculas que se encuentran a los extremos del polímeros (Figs. 2a y 2c) y la unidad molecular que se repite a lo largo de la cadena (Fig. 2b).

<p align="center">
<img src="https://github.com/daniastor/Polimeros-Biodegradables/blob/main/Imagenes/Unidades_repre.PNG" width="400" height="">
</p>
<p align="center">
Figura 2. Unidades representativas del polímero de amilosa. Las visualizaciones fueron generadas
desde el constructor: “ConstructorLT_ monomero.py”.
</p>

La ventaja de los constructores que tienen su propio sistema para rotular los átomos y moléculas, por lo que son capaces de escribir archivos LT que pueden llamarse entre sí dentro de la arquitectura de Moltemplate, y así realizar de manera automática la escritura del sistema completo iniciando desde el campo, además de la visualización de las moléculas (Fig. 2) y el polímero final construido (Fig. 3).

<p align="center">
<img src="https://github.com/daniastor/Polimeros-Biodegradables/blob/main/Imagenes/amilosa.PNG" width="600" height="">
</p>
<p align="center">
Figura 3. Cadena corta de unidades de D-glucosa, generada desde el constructor: “ConstructorLT_
polimero.py”.
</p>
