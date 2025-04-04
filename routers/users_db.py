# Importaciones necesarias de FastAPI y otras utilidades
from fastapi import APIRouter, HTTPException, status
from db.models.user import User  # Modelo de usuario (Pydantic)
from db.schemas.user import user_schema, users_schema  # Serializadores
from db.client import db_client  # Conexión a la base de datos
from bson import ObjectId  # Manejo de ObjectId de MongoDB
from fastapi.responses import JSONResponse

# Inicialización del router
router = APIRouter(
    prefix="/userdb",
    tags=["userdb"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

# Obtener todos los usuarios
@router.get("/", response_model=list[User])
async def get_all_users():
    return users_schema(db_client.users.find())

# Obtener un usuario por ID (query param)
@router.get("/search", response_model=User)
async def get_user_by_query(id: str):
    user = search_user("_id", ObjectId(id))
    if not isinstance(user, User):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Obtener un usuario por ID (path param)
@router.get("/{id}", response_model=User)
async def get_user_by_id(id: str):
    user = search_user("_id", ObjectId(id))
    if not isinstance(user, User):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Crear un nuevo usuario
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if isinstance(search_user("email", user.email), User):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe"
        )
    
    user_dict = user.dict(exclude={"id"})
    inserted_id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.users.find_one({"_id": inserted_id}))
    return User(**new_user)

# Actualizar un usuario existente
@router.put("/", response_model=User)
async def update_user(user: User):
    user_dict = user.dict()
    user_id = user_dict.pop("id")

    updated_user = db_client.users.find_one_and_replace(
        {"_id": ObjectId(user_id)}, user_dict
    )

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el usuario para actualizar"
        )

    return search_user("_id", ObjectId(user_id))

# Eliminar un usuario por ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    deleted_user = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el usuario para eliminar"
        )
    return JSONResponse(content={"message": "Usuario borrado con éxito!"}, status_code=status.HTTP_200_OK)

# Función auxiliar para buscar un usuario por campo
def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        if user:
            return User(**user_schema(user))
    except:
        pass
    return None
