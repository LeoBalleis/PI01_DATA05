from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from Etl import df_completo
import pandas as pd
app=FastAPI()
@app.get("/",response_class=HTMLResponse)
async def index():
    return """<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proyecto Individual N°1 - Data Engineering</title>
</head>
<body>
    <h1>Guía de Usuario de la API</h1>
    <h3>/get_max_duration/AÑO/PLATAFORMA/TIPO Por ej: /get_max_duration/2020/"netflix"/"min"</h3>
    <p>Devuelve la película/serie con mayor duración por plataforma, año y tipo de duración (min o seasons).</p>
    <h3>/get_count_platform/PLATAFORMA Por ej: /get_count_platform/disney</h3>
    <p>Devuelve la cantidad de películas y de series por plataforma</p>
    <h3>/get_listedin/GENERO Por ej: /get_listedin/comedy</h3>
    <p>Devuelve la cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.</p>
    <h3>/get_actor/PLATAFORMA/AÑO Por ej: /get_actor/"amazon"/2020</h3>
    <p>Devuelve al actor/actriz con mayor número de apariciones según año y plataforma.</p>
    <h3>Luego de realizar alguna consulta, si desea volver a esta guía, elimine los decoradores.</h3>
</body>
</html>"""




@app.get("/get_max_duration/{ano}/{plataforma}/{tipo}")
def get_max_duration(ano, plataforma, min_o_season):
  dftest=df_completo.query(f'release_year == {ano} and Plataforma == {plataforma} and unit== {min_o_season}').sort_values(by=['duration'],ascending=False)
  respuesta=dftest[['title','duration','unit']].iloc[0]
  respuesta=respuesta.to_dict()
  return respuesta


@app.get("/get_count_platform/{plataforma}")
def get_count_plataform(plataforma):
   dfq2=df_completo.query(f'Plataforma == {plataforma}')
   variable02=dfq2['type'].value_counts()
   variable02=variable02.to_dict()
   variable02['Plataforma']= plataforma
   return variable02


@app.get("/get_listedin/{genero}")
def get_listedin(genero):
    df03=df_completo.query (f'listed_in.str.contains({genero})')
    dtftest=df03[['Plataforma','listed_in']].groupby(['Plataforma']).count()
    nombre=dtftest.iloc[0].name
    cantidad=dtftest['listed_in'].iloc[0]
    diccionario={'plataform':nombre,'cantidad':cantidad}
    return diccionario

@app.get("/get_actor/{plataforma}/{ano}")
def get_actor(plataforma,ano):
    df04=df_completo.query(f'release_year == {ano} and Plataforma == {plataforma}' )
    new_df = pd.DataFrame(df04["cast"].str.split(',', expand=True).stack(), columns=["cast"])
    resultado=new_df.groupby(["cast"])["cast"].count().sort_values(ascending=False)
    dfx=pd.DataFrame(resultado)
    nombre=dfx.iloc[0].name
    cantidad=dfx['cast'].iloc[0]
    diccionario={'plataform': plataforma,'cantidad': cantidad,'actores':nombre}
    return diccionario






