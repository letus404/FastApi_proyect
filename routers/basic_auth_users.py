from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #la forma en la que se envía y captura el usuario y contraseña, dentro del modulo de seguridad de fastapi
router = APIRouter()

# OAuth2PasswordBearer especifica que los tokens se enviarán en la URL "/login"
oauth2 = OAuth2PasswordBearer(tokenUrl="login") 

# Definimos un modelo de usuario bas
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

# Modelo para la base de datos con contraseña (no se expone directamente)
class UserDB(User):
    password: str

# Simulamos una base de datos de usuarios
users_db = {
    "letus": {
        "username": "letus",
        "full_name": "Mariano Quinteros",
        "email": "letus@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "tripygruv": {
        "username": "tripygruv",
        "full_name": "Alejandro Quinteros",
        "email": "tripygruv@gmail.com",
        "disabled": True,  # Usuario deshabilitado
        "password": "654321"
    }
}

# Función para buscar un usuario en la base de datos
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) # Retorna el usuario con su contraseña

# Función para buscar un usuario sin exponer la contraseña
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) # Retorna solo los datos públicos del usuario

# Dependencia para obtener el usuario actual a partir del token
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas", 
            headers={"www-Authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user

# Endpoint para autenticación (login)
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}

# Endpoint protegido que devuelve la información del usuario autenticado
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user 


"""
🔥 Explicación de la autenticación con OAuth2 y PasswordBearer

1️⃣ OAuth2PasswordBearer(tokenUrl="login")
Define el esquema de autenticación OAuth2 con password.
tokenUrl="login" indica que los usuarios deben autenticarse en la ruta /login.
Espera un token de tipo Bearer en cada solicitud protegida.

2️⃣ Login (/login)
Recibe credenciales mediante OAuth2PasswordRequestForm.
Busca al usuario en users_db.
Si el usuario y la contraseña son correctos, retorna un token de acceso.

3️⃣ Protección de rutas (/users/me)
Usa Depends(current_user) para verificar el token.
Si el usuario no existe o está deshabilitado, lanza un HTTPException.

✅ Este método de autenticación es la base para implementar JWT Tokens en FastAPI. 🚀
"""