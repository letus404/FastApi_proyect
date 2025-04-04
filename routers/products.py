from fastapi import APIRouter

# 🔹 Crear un router para modularizar el código
router = APIRouter(prefix="/products", tags=["products"], responses={404: {"mensaje": "PAILAS"}})  
#📌 `prefix="/products"` → Define un prefijo en la URL, lo que significa que todas las rutas dentro de este router comenzarán con `/products` | tags=es para la documentacion para dividir las apis..
# Esto ayuda a organizar y estructurar la API de manera más clara.

# 🔹 Lista de productos simulada (base de datos en memoria)
products_list = ["Product 1", "Product 2", "Product 3", "Product 4", "Product 5"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id : int):
    return products_list[id] 