from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.utils import get_openapi
from typing import List
import secrets

# Create FastAPI app
app = FastAPI(
    title="Shopping Mall API",
    description="A super simple API with password-protected documentation",
    version="1.0.0",  # Add API version
    # Disable default docs
    docs_url=None,
    redoc_url=None
)

# Setup basic auth
security = HTTPBasic()

# Define username and password for docs
USERNAME = "admin"
PASSWORD = "secret123"

# Custom OpenAPI schema with version
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        openapi_version="3.0.2"  # Explicitly set OpenAPI version
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Security function to check credentials
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Custom docs endpoint with authentication
@app.get("/swagger", include_in_schema=False)
async def get_documentation(username: str = Depends(get_current_user)):
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Documentation",
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui.min.css",
    )

# Protect the OpenAPI JSON schema too
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_json(username: str = Depends(get_current_user)):
    return app.openapi()



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

# --- Product Routes or Endpoints ---
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