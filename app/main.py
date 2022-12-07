from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def read_root():
    return {'Máxima duración según tipo de film get_max_duration(año, plataforma, [min o season])\n Cantidad de películas y series (separado) por plataforma: get_count_plataform(plataforma)\n Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo:get_listedin(genero)\n Actor que más se repite según plataforma y año: get_actor(plataforma, año) '
    }

@app.get("/user/{user_id}{}")
def mensaje(user_id):
    return f"El id del ususrio es: {user_id}"