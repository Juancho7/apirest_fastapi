from fastapi import FastAPI, HTTPException, status
from models import Book

app = FastAPI()

books: list[Book] = [
    Book(
        id=0, title="The Catcher in the Rye", author="J.D. Salinger", release_year=1951
    ),
    Book(id=1, title="To Kill a Mockingbird", author="Harper Lee", release_year=1960),
    Book(id=2, title="1984", author="George Orwell", release_year=1949),
]


@app.get("/books", response_model=list[Book])
def get_books():
    return books


@app.post("/books", response_model=Book)
def add_book(book: Book):
    if any(existing_book.title == book.title for existing_book in books):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists!"
        )

    book.id = len(books)
    books.append(book)
    return book


@app.get("/books/{id}", response_model=Book)
def get_single_book(id: int):
    for book in books:
        if book.id == id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The book could not be fetched",
    )


@app.put("/books/{id}", response_model=Book)
def update_book(id: int, updated_book: Book):
    for existent_book in books:
        if existent_book.id == id:
            existent_book.title = updated_book.title
            existent_book.author = updated_book.author
            existent_book.release_year = updated_book.release_year
            return existent_book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The book does not exists",
    )


@app.delete("/books/{id}", response_model=dict)
def delete_book(id: int):
    for i, book in enumerate(books):
        if book.id == id:
            books.pop(i)
            return {"message": "Book deleted succesfully!"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The book does not exists",
    )
