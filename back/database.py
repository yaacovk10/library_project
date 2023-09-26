from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

# Create a SQLite database file (or use an existing one)
engine = create_engine('sqlite:///library.db')

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Define the base class for our models
Base = declarative_base()

# Define an Enum for book types
class BookType(enum.Enum):
    TYPE1 = 1
    TYPE2 = 2
    TYPE3 = 3

# Define the Books table
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    year_published = Column(Integer)
    type = Column(Integer, default=BookType.TYPE1)

# Define the Customers table
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    age = Column(Integer)

# Define the Loans table
class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey('customers.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    loan_date = Column(Date, default=datetime.now())
    return_date = Column(Date, nullable=True)

    # Establish a relationship with the Customer and Book tables
    customer = relationship('Customer', back_populates='loans')
    book = relationship('Book', back_populates='loans')

# Establish a bidirectional relationship between Customers and Loans
Customer.loans = relationship('Loan', order_by=Loan.id, back_populates='customer')

# Establish a bidirectional relationship between Books and Loans
Book.loans = relationship('Loan', order_by=Loan.id, back_populates='book')

# Create the tables in the database
Base.metadata.create_all(engine)
