from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
app = FastAPI()

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file



secret_key = os.getenv("SECRET_KEY")


origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://learnwithhasan.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/key")
def get_key():
    return {
        "secret_key" : secret_key
    }


@app.get("/hello/{name}")
def read_root(name: str, api_key : str):
    if api_key != "123456":
        return JSONResponse(
        status_code=401,
        content={"message": f"Oops! Access Denied"},
    )

    return {"Hello": f"{name}"}

@app.get("/get-name")
def get_name(name: str):
    return {"name": f"{name}"}

@app.get("/data")
def get_data():
    return {
        "name": "John Doe",
        "age": 30,
        "cities": ["New York", "Paris", "Tokyo"],
        "is_active": True
    }

@app.get("/test-code")
def return_code():
    return JSONResponse(
        status_code=404,
        content={"message": f"Oops! Somthing Wrong Happened, try again later."},
    )

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    age: int = Field(..., ge=18, lt=100)

@app.post("/users")
def create_user(user: User):
    return user




