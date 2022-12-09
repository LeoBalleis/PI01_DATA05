#DF AMAZON 
import pandas as pd #Importo las librerías a utilizar
amazon_titles = pd.read_csv("amazon_prime_titles.csv",delimiter = ',',encoding = "utf-8")#Armo el dataset de amazon
amazon_titles.drop(columns=['show_id','director','country','rating','description','date_added'], inplace=True) #Elimino las columnas que no me servirán para las consultas indicadas.
amazon_titles.fillna( 'SinDatos',inplace=True)#Reemplazo mis valores nulos por "Sin datos" en lugar de eliminarlos para no perder información
amazon_titles = amazon_titles.assign(Plataforma="amazon") # Agrego una columna para identificar la Plataforma


#DF DISNEY

disney_plus_titles = pd.read_csv("disney_plus_titles.csv",delimiter = ',',encoding = "utf-8")
disney_plus_titles.drop(columns=['show_id','director','country','rating','description','date_added'], inplace=True)
disney_plus_titles.fillna( 'SinDatos',inplace=True)
disney_plus_titles=disney_plus_titles.assign(Plataforma="disney")

#DF Hulu

hulu_titles=pd.read_csv("hulu_titles.csv",delimiter = ',',encoding = "utf-8")
hulu_titles.drop(columns=['show_id','director','country','rating','description','date_added'], inplace=True)
hulu_titles.fillna( 'SinDatos',inplace=True)
hulu_titles=hulu_titles.assign(Plataforma="hulu")

#DF Netflix

netflix_titles=pd.read_json("netflix_titles.json")
netflix_titles.drop(columns=['show_id','director','country','rating','description','date_added'], inplace=True)
netflix_titles.fillna( 'SinDatos',inplace=True)
netflix_titles=netflix_titles.assign(Plataforma="netflix")

# Concatenamos las 4 tablas en un unico df

df_completo= pd.concat([netflix_titles,hulu_titles,disney_plus_titles,amazon_titles])
df_completo.reset_index(inplace=True)

# Separo mi columna 'duration' en 'duration' y 'unit'
dfextra=df_completo.duration.str.split(expand=True)
dfextra=dfextra.reset_index()
dfextra[1]=dfextra[1].replace({'Season': 'Seasons'})# Normalizo el str seasons
df_completo=pd.concat([df_completo,dfextra],axis=1)# concateno con el df principal
df_completo.drop(columns=['duration','index'],inplace=True)# dropeo las columnas sobrantes
df_completo=df_completo.rename(columns={0:'duration',1:'unit'})# Le doy un nombre logico a las columnas 

# Reeplazo por 0 el 'SinDatos' de la columna duration  y los none de unit 
df_completo['duration']=df_completo['duration'].replace({'SinDatos': 0})
df_completo['unit']=df_completo['unit'].replace({None: 0})

df_completo['duration']=df_completo['duration'].astype(int)# Convierto la columna duration a int para poder comparar 
df_completo['cast']=df_completo['cast'].replace({'SinDatos':None})# Reeplazo en la columna cast 'SinDatos' por None

# Armo las Querrys para que me devuelvan diccionarios y se me facilite el trabajo con la API

#querry 1 Máxima duración según tipo de film (película/serie), por plataforma y por año: El request debe ser: get_max_duration(año, plataforma, [min o season])
def get_max_duration(ano, plataforma, min_o_season):
  dftest=df_completo.query(f'release_year == {ano} and Plataforma == {plataforma} and unit== {min_o_season}').sort_values(by=['duration'],ascending=False)
  respuesta=dftest[['title','duration','unit']].iloc[0]
  respuesta=respuesta.to_dict()
  return respuesta

#querry 2 Cantidad de películas y series (separado) por plataforma El request debe ser: get_count_plataform(plataforma)

def get_count_plataform(plataforma):
   dfq2=df_completo.query(f'Plataforma == {plataforma}')
   variable02=dfq2['type'].value_counts()
   variable02=variable02.to_dict()
   variable02['Plataforma']= plataforma
   return variable02

#Querrry 3  Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo. El request debe ser: get_listedin('genero')
# Como ejemplo de género pueden usar 'comedy', el cuál deberia devolverles un cunt de 2099 para la plataforma de amazon.

def get_listedin(genero):
    df03=df_completo.query (f'listed_in.str.contains({genero})')
    dtftest=df03[['Plataforma','listed_in']].groupby(['Plataforma']).count()
    nombre=dtftest.iloc[0].name
    cantidad=dtftest['listed_in'].iloc[0]
    return f'El género {genero} aparece {cantidad} veces en {nombre}'


##4 Actor que más se repite según plataforma y año. El request debe ser: get_actor(plataforma, año)

def get_actor(plataforma,ano):
    df04=df_completo.query(f'release_year == {ano} and Plataforma == {plataforma} and ' )
    new_df = pd.DataFrame(df04["cast"].str.split(',', expand=True).stack(), columns=["cast"])
    resultado=new_df.groupby(["cast"])["cast"].count().sort_values(ascending=False)
    dfx=pd.DataFrame(resultado)
    nombre=dfx.iloc[0].name
    cantidad=dfx['cast'].iloc[0]
    return f'El actor/actriz con mayor número de apariciones en la plataforma {plataforma} el año {ano} es {nombre} con {cantidad} apariciones.'


  