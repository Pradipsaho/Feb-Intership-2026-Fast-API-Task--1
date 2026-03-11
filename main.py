from fastapi import FastAPI

app = FastAPI()

# Temporary data acting as our database
products = [
    {
        "id": 1,
        "name": "Wireless Mouse",
        "price": 499,
        "category": "Electronics",
        "in_stock": True
    },
    {
        "id": 2,
        "name": "Notebook",
        "price": 99,
        "category": "Stationery",
        "in_stock": True
    },
    {
        "id": 3,
        "name": "USB Hub",
        "price": 799,
        "category": "Electronics",
        "in_stock": False
    },
    {
        "id": 4,
        "name": "Pen Set",
        "price": 49,
        "category": "Stationery",
        "in_stock": True
    },
    {
        "id": 5,
        "name": "Bluetooth Speaker",
        "price": 199,
        "category": "Electronics",
        "in_stock": True
    },
    {
        "id": 6,
        "name": "Desk Organizer",
        "price": 299,
        "category": "Office Supplies",
        "in_stock": False

    },
    {
        "id": 7,
        "name": "Water Bottle",
        "price": 149,
        "category": "Accessories",
        "in_stock": True
    },
    {
        "id": 8,
        "name": "Laptop Stand",
        "price": 399,
        "category": "Electronics",
        "in_stock": True
    },
    {
        "id": 9,
        "name": "Sticky Notes",
        "price": 29,
        "category": "Stationery",
        "in_stock": True
    },
    {
        "id": 10,
        "name": "Headphones",
        "price": 999,
        "category": "Electronics",
        "in_stock": False   
    },
    {
        "id": 11,
        "name": "Coffee Mug",
        "price": 199,
        "category": "Accessories",
        "in_stock": True
    }
]

# Endpoint 0 - Home
@app.get("/")
def home():
    return {"message": "Welcome to our E-commerce API"}

# Endpoint 1 - Return all products
@app.get("/products")
def get_all_products():
    return {"products": products, "total": len(products)}

# Endpoint 2 - Return one product by its ID
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    return {"error": "Product not found"}