from flask import jsonify
from sqlalchemy.orm import Session
from .models import Book  # Import your Book model

def add_book(session: Session, name: str, author: str, year_published: int, book_type: int):
    # Create a new book
    new_book = Book(name=name, author=author, year_published=year_published, type=book_type)
    session.add(new_book)
    session.commit()
    return jsonify({"message": "Book added successfully"}), 201

def display_all_books(session: Session):
    books = session.query(Book).all()
    book_list = [{"id": book.id, "name": book.name, "author": book.author, "year_published": book.year_published, "type": book.type} for book in books]
    return jsonify({"books": book_list})

def find_book_by_name(session: Session, name: str):
    book = session.query(Book).filter_by(name=name).first()
    if book:
        return jsonify({"book": {"id": book.id, "name": book.name, "author": book.author, "year_published": book.year_published, "type": book.type}})
    else:
        return jsonify({"message": "Book not found"}), 404

def remove_book(session: Session, book_id: int):
    book = session.query(Book).filter_by(id=book_id).first()
    if book:
        session.delete(book)
        session.commit()
        return jsonify({"message": "Book removed successfully"}), 200
    else:
        return jsonify({"message": "Book not found"}), 404
