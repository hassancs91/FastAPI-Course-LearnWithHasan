from fastapi import FastAPI


app = FastAPI()


app = FastAPI(
    title="Shopping Mall API",
    description="A super simple API with products, users and orders",
    docs_url="/swagger" 
)

# --- Dummy Data using simple dictionaries ---
products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Phone", "price": 499.99},
    {"id": 3, "name": "Headphones", "price": 99.99}
]

users = [
    {"id": 1, "username": "john_doe", "email": "john@example.com"},
    {"id": 2, "username": "jane_smith", "email": "jane@example.com"}
]

orders = [
    {
        "id": 1,
        "user_id": 1,
        "items": ["Laptop", "Headphones"],
        "total": 1099.98
    },
    {
        "id": 2,
        "user_id": 2,
        "items": ["Phone"],
        "total": 499.99
    }
]

# --- Product Routes ---
@app.get(
    "/products/",
    tags=["Products"],
    description="Get all products in the store"
)
def get_products():
    return products

@app.get(
    "/products/{product_id}",
    tags=["Products"],
    description="Get a single product by its ID"
)
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return {"message": "Product not found"}

# --- User Routes ---
@app.get(
    "/users/",
    tags=["Users"],
    description="Get all users"
)
def get_users():
    return users

@app.get(
    "/users/{user_id}",
    tags=["Users"],
    description="Get a single user by their ID"
)
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    return {"message": "User not found"}

# --- Order Routes ---
@app.get(
    "/orders/",
    tags=["Orders"],
    description="Get all orders"
)
def get_orders():
    return orders

@app.get(
    "/orders/{order_id}",
    tags=["Orders"],
    description="Get a single order by its ID"
)
def get_order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return order
    return {"message": "Order not found"}