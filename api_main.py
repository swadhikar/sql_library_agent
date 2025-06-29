# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from library import (
    create_database, add_user, add_book, borrow_book,
    get_users, get_books
)
from sql_agent import ask_question

app = FastAPI()
session = create_database()


# Dependency
def get_db():
    yield session


@app.get("/")
def root():
    return {"message": "Library API is running"}


@app.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    return get_users(db)


@app.get("/books/")
def get_all_books(db: Session = Depends(get_db)):
    return get_books(db)


@app.post("/users/")
def api_add_user(name: str, db: Session = Depends(get_db)):
    add_user(name, db)
    return {"message": f"User '{name}' added"}


@app.post("/books/")
def api_add_book(title: str, db: Session = Depends(get_db)):
    add_book(title, db)
    return {"message": f"Book '{title}' added"}


@app.post("/borrow/")
def api_borrow_book(username: str, title: str, db: Session = Depends(get_db)):
    try:
        borrow_book(username, title, db)
        return {"message": f"User '{username}' borrowed '{title}'"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/question")
def api_get_answer(question: str, db: Session = Depends(get_db)):
    return {
        'question': question,
        'answer': ask_question(question)
    }
