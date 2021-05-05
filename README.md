# Construcción de largas cadenas poliméricas para LAMMPS

Es posible emplear [Moltemplate](https://www.moltemplate.org/) para construir, organizar y almacenar una base de datos que describa un modelo molecular en archivos de formato LT, los cuales pueden ser posteriormente convertidos por el algoritmo Moltemplate en archivos de entrada para [LAMMPS](https://lammps.sandia.gov/).

En este trabajo se deja de libre acceso un conjunto de códigos llamados “constructores” en python, lo cuales, permiten llenar los archivos de formato LT de Moltemplate con la información geométrica y de campos de fuerza de las moléculas del polímero, a partir del procesamiento de datos de las unidades representativas. Nombramos unidades representativas a todas las unidades moleculares diferentes (se encuentren repetidas o no) que conforman el polímero, en el caso de la amilosa (Fig. 1).

<p align="center">
<img src="https://github.com/daniastor/Polimeros-Biodegradables/blob/main/Imagenes/Estructura_Amilosa.PNG" width="600" height="">
</p>
<p align="center">
Figura 1. Estructura química de la amilosa.
</p>

Podemos tomar como unidades representativas: las moléculas que se encuentran a los extremos del polímeros (Figs. 2a y 2c) y la unidad molecular que se repite a lo largo de la cadena (Fig. 2b). El ConstructorLT_ monomero.py se encarga de escribir los archivos LT con la información de las unidades moleculares representativas, para su uso solamente requiere el ingreso del archivo PDB de cada unidad molecular, por ejemplo, exportada desde Avogadro. Además, permite la visualización de las moléculas en el modelo de esferas duras y muestra los rótulos asociados a los átomos dentro de las moléculas (Fig. 2).

<p align="center">
<img src="https://github.com/daniastor/Polimeros-Biodegradables/blob/main/Imagenes/Unidades_repre.PNG" width="600" height="">
</p>
<p align="center">
Figura 2. Unidades representativas del polímero de amilosa. Las visualizaciones fueron generadas
desde el constructor: “ConstructorLT_ monomero.py”.
</p>

El ConstructorLT_ polimero.py permite escribir el archivo LT con la información espacial y las conexiones entre las unidades representativas, en otras palabras, construye el polímero. Además, también genera el archivo LT del sistema, con el cual se define el espacio que va a contener al polímero, en forma de caja. Para su uso solamente requiere el ingreso del archivo PDB de cada unidad molecular, el grado de polimerización y el ingreso de los rótulos de los átomos específicos de las moléculas que se desea conectar, los cuales, pueden ser fácilmente identificados con la salida gráfica del ConstructorLT_ monomero. Como tal el trabajo del ConstructorLT_polimero.py es genera una curva y distribuir unidades moleculares a lo largo de la curva, al igual que posicionar la curva dentro de un espacio,
como se muestra en la Fig. (Fig. 3).

<p align="center">
<img src="https://github.com/daniastor/Polimeros-Biodegradables/blob/main/Imagenes/Camilosa.svg" width="400" height="">
</p>
<p align="center">
Figura 3. Cadena corta de amilosa, generada desde el constructor: “ConstructorLT_polimero.py”.
</p>

El ConstructorLT_ campo.py permite escribir el archivo LT con toda la información del campo de fuerza del sistema molecular polimérico desarrollado con el “ConstructorLT_ polimero.py” a partir de datos disponibles en la literatura, es importante mencionar que la información contenida en los archivos .txt pertenece a la investigación de [Olsson et al., 2019](https://www.sciencedirect.com/science/article/pii/S0264127519308251) (https://doi.org/10.1016/j.matdes.2019.108387). 

Finalmente en la Fig. 4, se observa la pequeña cadena de amilosa (con 8 unidades de glucosa) elaborada a partir de los constructores despues de ser leída por LAMMPS.

<p align="center">
<img src="https://github.com/daniastor/Polimeros-Biodegradables/blob/main/Imagenes/U8_EstadoInicial.png" width="400" height="">
</p>
<p align="center">
Figura 3. Estado inicial de la cadena corta de amilosa configurada con los constructres, implementada en LAMMPS y lista para simulaciones de dinámica molecular, visualización generada desde [OVITO](https://www.ovito.org/).
</p>
