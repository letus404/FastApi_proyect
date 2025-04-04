from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError   # Manejo de JWT
from passlib.context import CryptContext # Cifrado de contraseñas con bcrypt
from datetime import datetime, timedelta  # Manejo de fechas para expiración de tokens

# Algoritmo de cifrado para JWT
ALGORITHM = "HS256"
# Duración del token en minutos
ACCESS_TOKEN_DURATION = 1
# Clave secreta para firmar los tokens (¡NO usar esta en producción!)
SECRET = "asdasdasdasdholaasdlkasdlajsdslakjdtransalskdasdljkasdricosasdlkasjdalsdkjal"

# Creación del router para separar rutas de autenticación
router = APIRouter()

# OAuth2PasswordBearer define el mecanismo para obtener el token (debe enviarse en "Authorization: Bearer <token>")
oauth2 = OAuth2PasswordBearer(tokenUrl="login") 

# Configuración del contexto de PassLib para cifrado de contraseñas (bcrypt)
crypt = CryptContext(schemes=["bcrypt"])

# Modelo de usuario sin contraseña (para devolver en respuestas)
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool # Indica si el usuario está activo o no

# Modelo de usuario con contraseña (para manejar en la base de datos)
class UserDB(User):
    password: str

# Base de datos simulada (diccionario con usuarios)
users_db = {
    "letus": {
        "username": "letus",
        "full_name": "Mariano Quinteros",
        "email": "letus@gmail.com",
        "disabled": False,
        "password": "$2a$12$WWPyKCLC5WlhGrX49MGb0eB.zhS5E4ZMsFV65D2KI5gKN2BWZdOOi"
    },
    "tripygruv": {
        "username": "tripygruv",
        "full_name": "Alejandro Quinteros",
        "email": "tripygruv@gmail.com",
        "disabled": True,
        "password": "$2a$12$AjwNojWPh/U1RqhouGQGAe.XXCwIAoKvDaEKeUsSvoTzFC2.Chpsa"
    }
}

# 🔍 **Buscar usuario en la "base de datos" con contraseña**
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) 

# 🔍 **Buscar usuario sin devolver la contraseña**    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) 

# ✅ **Autenticar usuario con JWT**    
async def auth_user(token: str = Depends(oauth2)):

    exception =  HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas", 
            headers={"www-Authenticate": "Bearer"})
    
    # Decodificar el token JWT
    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        # Si el username no existe en el token, lanzar excepción
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    return search_user(username)

# ✅ **Verificar si el usuario está activo**
async def current_user(user: str = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user

# 🔑 **Login y generación de token**
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Buscar usuario en la base de datos
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "El usuario no es correcto")
    
    # Obtener el usuario con contraseña cifrada
    user = search_user_db(form.username)

    # Verificar la contraseña ingresada contra la almacenada (bcrypt)
    if not crypt.verify(form.password, user.password): 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "La contraseña no es correcta")
    
    # Crear tiempo de expiración del token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    # Crear el token con el username y la expiración
    access_token = {"sub":user.username,  # Identificación del usuario
                    "exp":  datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
     # Retornar el token firmado
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

# 🆔 **Obtener datos del usuario autenticado**
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user 