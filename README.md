# 🚀 Proyecto FastAPI + MongoDB

Este proyecto es una API REST construida con **FastAPI** y conectada a una base de datos **MongoDB**. Utiliza `pymongo` para operaciones de base de datos, y `Pydantic` para validación de datos.

---

## 📦 Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [Motor o PyMongo](https://pymongo.readthedocs.io/)
- [Uvicorn](https://www.uvicorn.org/) (para correr el servidor)

---

## 🚀 Cómo ejecutar el proyecto

1. **Clona el repositorio:**

2. **Crear un entorno virtual**
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Crea un archivo .env y agrega tu URI de MongoDB:
   MONGO_URI=mongodb+srv://<usuario>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority

4. Corre el servidor:
  uvicorn main:app --reload


📁 Estructura del Proyecto
.
├── main.py                # Punto de entrada FastAPI
├── db/
│   ├── client.py          # Cliente de conexión MongoDB
│   ├── models/            # Modelos Pydantic
│   └── schemas/           # Serializadores (dict <-> modelo)
├── routers/               # Rutas divididas por módulos
├── .env                   # Variables de entorno (no subir a Git)
├── requirements.txt       # Dependencias
└── README.md


📮 Endpoints de ejemplo
GET    /userdb/               -> Lista todos los usuarios
GET    /userdb/{id}           -> Busca usuario por ID
POST   /userdb/               -> Crea un nuevo usuario
PUT    /userdb/               -> Actualiza un usuario
DELETE /userdb/{id}           -> Elimina un usuario


🧪 Pruebas
Puedes probar fácilmente la API desde:

http://localhost:8000/docs → Swagger UI

http://localhost:8000/redoc → ReDoc


📌 Créditos
Desarrollado con por Letus404.
