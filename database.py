#CONNECTING TO A DATABASE

from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

connection_string = "mongodb+srv://hasan:Ozv8VNjAIv71EYbv@hasanfree0.qumut.mongodb.net/?retryWrites=true&w=majority&appName=HASANFREE0"
my_client = MongoClient(connection_string)
db = my_client["test"]  # database name
collection = db["books"]  # collection name


# Pydantic model for Book
class Book(BaseModel):
    title: str
    author: str
    price: float

# Create a new book
@app.post("/add-book/")
async def create_book(book: Book):
    book_dict = book.model_dump()
    collection.insert_one(book)
    return {"message": "Book added successfully"}


@app.get("/get-all-books/")
async def get_all_books():
    books = []
    for book in collection.find():
        # Convert MongoDB's _id to string
        book["_id"] = str(book["_id"])
        books.append(book)
    return books



@app.get("/books/{title}")
async def get_book(title: str):
    book = collection.find_one({"title": title})
    if book:
        book["_id"] = str(book["_id"])
        return book
        
    return {"message": "Not Found!"}


