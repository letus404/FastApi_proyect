from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles #para importar la clase de archivos estáticos



# Creamos una instancia de la aplicación FastAPI
app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static") #montamos la ruta para servir archivos estáticos, especificamos a StaticFiles el directorio donde se encuentran los archivos y le damos un nombre al recurso.

# Definimos una ruta GET en "/" (la raíz de la API) | GET = peticion
@app.get("/")
async def root(): #asíncrono, se pueden ejecutar varias tareas al mismo tiempo, mientras que la sincronía debe esperar una tarea para iniciar otra
    return "Hola Papaaaa! Estamos desde FastAPI" # Respuesta de la API

# AHORA LEVANTAR EL SERVIDOR UVICORN
# uvicorn main:app --reload


@app.get("/url") #estoy llamando a otra página
async def url():
    return { "url_curso":"https://mouredev.com/python" } #clave-valor, se van a entender con el front.


#PETICIONES GET = OBTENER/LEER DATOS
#CRUD = Create, Read, Update, Delete
#CREATE = POST | READ = GET |UPDATE = PUT | DELETE = DELETE

