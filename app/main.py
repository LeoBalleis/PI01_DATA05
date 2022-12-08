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
    <title>Proyecto Individual N°1 - Data Engineering Henry</title>
</head>
<style>
  body {  background-color: #22272e;
          font-family: verdana;
          font-size: 75%;}
  h1   {  color: #cdd9e5;
          font-family: verdana;
          font-size: 250%;}
  h3   {  color: #539bf5;
          font-family: verdana;
          font-size: 150%;}
  p    {  color: #cdd9e5;
          font-family: verdana;
          font-size: 200%;}
  a    {  display: block;
          width: 130px;
          font-family: verdana
          font-weight: 700;
          background-color: #AD0306;
          border-radius:10px;
          color: #cdd9e5;
          text-decoration: none;
          margin: 15px 20px}
 a:hover {background-color: transparent;
          border: 2px solid #539bf5
          color: #539bf5}
</style>
<body>
    <h1>Guía de Usuario de la API</h1>
    <h1>IMPORTANTE: Los textos ponerlos entre comillas "" </h1>
    <p>Devuelve la película/serie con mayor duración por plataforma, año y tipo de duración (min o seasons).</p>
    <h3>ej: /get_max_duration/2020/"netflix"/"min"</h3> 
    <p>Devuelve la cantidad de películas y de series por plataforma</p>
    <h3>ej: /get_count_platform/"disney"</h3>
    <p>Devuelve la cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.</p>
    <h3>ej: /get_listedin/"Comedy"</h3>
    <p>Devuelve al actor/actriz con mayor número de apariciones según año y plataforma.</p>
    <h3>ej: /get_actor/"netflix"/2018</h3>
    <h3>Luego de realizar alguna consulta, si desea volver a esta guía, elimine los decoradores.</h3>
</body>
</html>"""




@app.get("/get_max_duration/{ano}/{plataforma}/{tipo}")
def get_max_duration(ano, plataforma, tipo):
  dftest=df_completo.query(f'release_year == {ano} and Plataforma == {plataforma} and unit== {tipo}').sort_values(by=['duration'],ascending=False)
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
    return f'El género {genero} aparece {cantidad} veces en {nombre}'




@app.get("/get_actor/{plataforma}/{ano}")
async def get_actor(plataforma,ano):
    df04=df_completo.query(f'release_year == {ano} and Plataforma == {plataforma}' )
    new_df = pd.DataFrame(df04["cast"].str.split(',', expand=True).stack(), columns=["cast"])
    resultado=new_df.groupby(["cast"])["cast"].count().sort_values(ascending=False)
    dfx=pd.DataFrame(resultado)
    nombre=dfx.iloc[0].name
    cantidad=dfx['cast'].iloc[0]
    return f'El actor/actriz con mayor número de apariciones en la plataforma {plataforma} el año {ano} es {nombre} con {cantidad} apariciones.'






