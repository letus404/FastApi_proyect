from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:test@cluster0.bllczxy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0').test
#LOCAL
#client = MongoClient("mongodb://localhost:27017/")
db_client = client["users"]  # Aquí "users" es el nombre de tu base de datos