# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Data Engineering`**</h1>

## Introducción:

Mi nombre es Leonel Facundo Balleis, al momento de hacer este proyecto me encuentro cursando la etapa de Labs para la carrera de Data Science de SoyHenry. 

EN este proyecto vamos a relizar trabajo  de  Data Engineer, y para ello se nos entregan 4 datasets de distintas plataformas de streaming como amazon, disney, hulu y netflix y debemos realizar un EDA sobre cada uno y corregir imperfecciones como diferencias en el tipo de los datos, valores nulos, duplicados, etc.

## Objetivo: 

Realizar un trabajo de ETL sobre los datasets recibidos y levantar una API con esos datos limpios a la que se le puedan realizar diferentes consultas.

Las consultas a realizar son:

+ Máxima duración según tipo de film (película/serie), por plataforma y por año.
    El request debe ser: get_max_duration(año, plataforma, [min o season])

+ Cantidad de películas y series (separado) por plataforma.
    El request debe ser: get_count_plataform(plataforma)  
  
+ Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.
    El request debe ser: get_listedin('genero')  

+ Actor que más se repite según plataforma y año.
    El request debe ser: get_actor(plataforma, año)

Plus: Realizar un deployment de la API en una plataforma "code to cloud" como por ejemplo, Mogenius.

## Explicación de los contenidos del Repositorio:

+ En el notebook `ETL.ipynb` se encuentra el código comentado paso por paso, explicando las decisiones tomadas a la hora de encarar este proyecto de ETL con esto espero documentar y demostrar cada paso del desarrollo.

+ En la carpeta `app` se encuentran los datasets analizados, el archivo `main.py` que es el archivo en el cual se configura FastAPI y se instancian los decoradores de la API y además, el archivo `Etl.py` en el cual se encuentra el mismo código del notebook `ETL.ipynb` pero más optimizado y sin comentarios. 

+ En el archivo `dockerfile` se encuentra el entorno containerizado de Docker con FastAPI.

## Herramientas utilizadas:

+ Python.

+ Pandas.

+ Docker.

+ FastAPI.

+ HTML.