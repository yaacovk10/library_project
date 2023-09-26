from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Customer , Book, Loan # Import your model classes
from customer import add_customer, display_all_customers, find_customer_by_name, remove_customer
from book import add_book, display_all_books, find_book_by_name, remove_book
from loan import loan_book, return_book, display_all_loans, display_late_loans

app = Flask(__name__)

# Create a SQLite database engine
engine = create_engine('sqlite:///library.db')

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def home():
    return "Welcome to the Library Management System"

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    name = data.get('name')
    city = data.get('city')
    age = data.get('age')
    
    # Call the add_customer function
    response, status_code = add_customer(session, name, city, age)
    
    # Return the response and status code directly
    return response, status_code

@app.route('/customers', methods=['GET'])
def get_all_customers():
    # Call the display_all_customers function to get all customers
    return display_all_customers(session)

@app.route('/customers/<name>', methods=['GET'])
def find_customer(name):
    # Call the find_customer_by_name function to find a customer by name
    return find_customer_by_name(session, name)

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def remove_customer_by_id(customer_id):
    # Call the remove_customer function to remove a customer by ID
    return remove_customer(session, customer_id)

# Routes for managing books
@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    name = data.get('name')
    author = data.get('author')
    year_published = data.get('year_published')
    book_type = data.get('book_type')
    
    # Call the add_book function
    response, status_code = add_book(session, name, author, year_published, book_type)
    
    # Return the response and status code directly
    return response, status_code

@app.route('/books', methods=['GET'])
def get_all_books():
    # Call the display_all_books function to get all books
    return display_all_books(session)

@app.route('/books/<name>', methods=['GET'])
def find_book(name):
    # Call the find_book_by_name function to find a book by name
    return find_book_by_name(session, name)

@app.route('/books/<int:book_id>', methods=['DELETE'])
def remove_book_by_id(book_id):
    # Call the remove_book function to remove a book by ID
    return remove_book(session, book_id)

# Routes for managing loans
@app.route('/loans', methods=['POST'])
def loan_a_book():
    data = request.json
    cust_id = data.get('cust_id')
    book_id = data.get('book_id')
    
    # Call the loan_book function
    response, status_code = loan_book(session, cust_id, book_id)
    
    # Return the response and status code directly
    return response, status_code

@app.route('/loans/<int:loan_id>', methods=['PUT'])
def return_a_book(loan_id):
    # Call the return_book function to return a book by loan ID
    return return_book(session, loan_id)

@app.route('/loans', methods=['GET'])
def get_all_loans():
    # Call the display_all_loans function to get all loans
    return display_all_loans(session)

@app.route('/loans/late', methods=['GET'])
def get_late_loans():
    # Call the display_late_loans function to get late loans
    return display_late_loans(session)

if __name__ == '__main__':
    app.run(debug=True)
