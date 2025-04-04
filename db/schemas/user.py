### User schema ###

# Esta función toma un documento de MongoDB (un dict con _id) y lo convierte a un formato que FastAPI pueda usar
def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),  # Convierte el ObjectId a string
        "username": user["username"],  # Mantiene el username
        "email": user["email"]  # Mantiene el email
    }

# Esta función toma una lista de usuarios y aplica user_schema a cada uno
def users_schema(users) -> list:
    return [user_schema(user) for user in users]  # Devuelve una lista de usuarios en formato dict
