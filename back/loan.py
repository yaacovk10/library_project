from flask import jsonify
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .models import Loan  # Import your Loan model

def loan_book(session: Session, customer_id: int, book_id: int):
    # Create a new loan record
    loan = Loan(cust_id=customer_id, book_id=book_id, loan_date=datetime.now())
    session.add(loan)
    session.commit()
    return jsonify({"message": "Book loaned successfully"}), 201

def return_book(session: Session, loan_id: int):
    loan = session.query(Loan).filter_by(id=loan_id).first()
    if loan:
        loan.return_date = datetime.now()
        session.commit()
        return jsonify({"message": "Book returned successfully"}), 200
    else:
        return jsonify({"message": "Loan record not found"}), 404

def display_all_loans(session: Session):
    loans = session.query(Loan).all()
    loan_list = [{"id": loan.id, "cust_id": loan.cust_id, "book_id": loan.book_id, "loan_date": loan.loan_date.strftime("%Y-%m-%d"), "return_date": loan.return_date.strftime("%Y-%m-%d") if loan.return_date else None} for loan in loans]
    return jsonify({"loans": loan_list})


def display_late_loans(session: Session):
    # Define a time threshold, for example, loans that are more than 7 days overdue
    threshold_date = datetime.now() - timedelta(days=1)
    
    # Query for late loans based on the threshold date
    late_loans = session.query(Loan).filter(Loan.return_date < threshold_date).all()

    # Serialize the data and return a JSON response
    late_loan_list = [{"id": loan.id, "cust_id": loan.cust_id, "book_id": loan.book_id, "loan_date": loan.loan_date.strftime("%Y-%m-%d"), "return_date": loan.return_date.strftime("%Y-%m-%d") if loan.return_date else None} for loan in late_loans]
    
    return jsonify({"late_loans": late_loan_list})
