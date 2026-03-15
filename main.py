from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List

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



# day 2 - Q1 — Add min_price Query Parameter

from fastapi import Query

@app.get("/products/filter")
def filter_products(
    category: str = Query(None),
    max_price: int = Query(None),
    min_price: int = Query(None, description="Minimum price")
):
    result = products

    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]

    if max_price:
        result = [p for p in result if p["price"] <= max_price]

    if min_price:
        result = [p for p in result if p["price"] >= min_price]

    return {"filtered_products": result}

# Q2 — Product Price Endpoint

@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "price": product["price"]
            }

    return {"error": "Product not found"}

# 3️⃣ Q3 — Customer Feedback (Pydantic)

class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)
feedback = []

@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):

    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data.dict(),
        "total_feedback": len(feedback)
    }

# Q4 — Product Summary Dashboard

@app.get("/products/summary")
def product_summary():

    in_stock = [p for p in products if p["in_stock"]]
    out_stock = [p for p in products if not p["in_stock"]]

    expensive = max(products, key=lambda p: p["price"])
    cheapest = min(products, key=lambda p: p["price"])

    categories = list(set(p["category"] for p in products))

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive": {
            "name": expensive["name"],
            "price": expensive["price"]
        },
        "cheapest": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "categories": categories
    }

# Q5 — Bulk Order System


class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=50)

class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)

@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:

        product = next((p for p in products if p["id"] == item.product_id), None)

        if not product:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })

        elif not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })

        else:
            subtotal = product["price"] * item.quantity
            grand_total += subtotal

            confirmed.append({
                "product": product["name"],
                "qty": item.quantity,
                "subtotal": subtotal
            })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }

