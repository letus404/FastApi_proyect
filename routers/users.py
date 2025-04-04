from fastapi import APIRouter, HTTPException

# Importamos BaseModel de Pydantic para definir nuestras entidades
from pydantic import BaseModel

#levantar server: uvicorn users:app --reload

router = APIRouter(tags=["users"]) #el tag me sirve para la documentacion para poder separar 

# Definir ENTIDAD- el objeto de la vida real, con caracteristicas específicas
class User(BaseModel):
    id : int
    name : str
    aliasTechno : str
    aliasHouse : str
    edad : int

# 📌 Lista de usuarios simulando una base de datos
users_list = [User(id=1, name="Mariano", aliasTechno="Letus", aliasHouse="Tripygruv", edad=31),
         User(id=2, name="Sergio",aliasTechno="OZM",aliasHouse="Humano", edad= 25),
         User(id=3, name="Julian",aliasTechno="Josho",aliasHouse="Kramer", edad= 33)]

# 📌 Ruta que devuelve una lista de usuarios en formato JSON (sin usar el modelo User)
@router.get("/usersjson")
async def usersjson():
    return [{"name":"Mariano","aliasTechno":"Letus","aliasHouse":"Tripygruv", "edad": 31},
            {"name":"Sergio","aliasTechno":"OZM","aliasHouse":"Humano", "edad": 25},
            {"name":"Julian","aliasTechno":"Josho","aliasHouse":"Kramer", "edad": 33}]

# 📌 Ruta que devuelve la lista de usuarios usando la entidad User
@router.get("/users") 
async def users():
    return users_list

# 📌 Definir una nueva ruta que reciba un parámetro "id"
@router.get("/user/{id}")  # Ruta dinámica que recibe un ID como parámetro en la URL
async def user(id: int):  # Se define el tipado del parámetro como entero
    return search_user(id) #Buscar el usuario en la lista, funcion definida abajo

@router.get("/userquery") # La ruta NO usa parámetros en la URL, sino en la consulta (?id=)
async def user(id: int):  # Se define el parámetro "id" como entero (Query Parameter)
    return search_user(id)

"""
✅ Diferencias entre Query Parameter y Path Parameter
Tipo - Ejemplo de URL - Uso
Path Parameter |	/user/1	 |Se usa cuando el ID es parte de la estructura de la URL.
Query Parameter	|   /userquery?id=1	 | Se usa cuando el ID es un valor opcional o parte de una búsqueda dinámica. """

# 📌 Definir una ruta para agregar un nuevo usuario con el método POST
@router.post("/user/", status_code=201)  #Se usa POST porque estamos enviando datos al servidor | el status_code= es para cambiar el codigo que quiero generar
async def user(user: User):  # Recibe un objeto "User" como parámetro del cuerpo de la petición
#Agrega un nuevo usuario a la lista si no existe previamente.

   # 📌 Verifica si el usuario ya existe usando la función "search_user"
    if type(search_user(user.id)) == User:
        raise HTTPException(404, detail="No se ha creado porque el usuario ya existe") #📌 Lanza una excepción HTTP si ocurre un error en la solicitud.
    users_list.append(user)  # Agrega el usuario a la lista si no está repetido
    return {"message": "Usuario agregado con éxito"}  # Retorna un mensaje de éxito si lo agrega

# 📌 Definir una ruta para actualizar un usuario con el método PUT
@router.put("/user/")  # Se usa PUT para actualizar datos existentes
async def user(user: User):
    """
    Busca un usuario por ID y actualiza sus datos.
    """

    found = False  # Variable para verificar si el usuario fue encontrado

    # 📌 Se recorre la lista con "enumerate()" para obtener índice y objeto usuario
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:  # Si el ID coincide con el usuario recibido
            users_list[index] = user  # Se reemplaza el usuario en la lista
            found = True  # Se marca como encontrado

    # 📌 Si no se encontró el usuario, se retorna un error
    if not found:
        return {"error": "No se ha actualizado el usuario"}  

    return user  # Se devuelve el usuario actualizado

@router.delete("/user/{id}") # Ruta dinámica que recibe un ID como parámetro en la URL
async def user(id: int):

    found = False  # 📌 Variable para verificar si el usuario existe

    # 📌 Recorremos la lista de usuarios con `enumerate()` para obtener el índice y el usuario
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:  # 📌 Si encontramos el usuario con el ID especificado...
            del users_list[index]  # 📌 Lo eliminamos de la lista con `del`
            found = True # 📌 Confirmamos que el usuario fue encontrado y eliminado

    if not found:
        return {"error": "No se ha borrado el usuario"}
    return {"message" : "Se ha borrado el usuario con éxito" }      # 📌 Si el usuario fue eliminado, enviamos un mensaje de éxito

#Busca un usuario en la lista filtrando por su ID.
#Retorna una lista con el usuario encontrado o vacía si no hay coincidencias.    
def search_user(id : int): #defino el buscador en una funcion
    users = filter(lambda user: user.id == id, users_list)  # Filtra la lista de usuarios por ID
    try: # Intenta devolver el primer usuario encontrado en la lista filtrada
        return list(users)[0]  # Convierte el resultado en una lista y devuelve solo el primer resultado
    except:  # Si no hay coincidencia
        return {"error": "No se encontró el usuario"} 
    
    # Ejemplo de consulta | http://127.0.0.1:8000/userquery?id=1