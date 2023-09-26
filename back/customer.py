from flask import jsonify
from sqlalchemy.orm import Session
from .models import Customer  # Import your Customer model

def add_customer(session: Session, name: str, city: str, age: int):
    # Check if a customer with the same name already exists
    existing_customer = session.query(Customer).filter_by(name=name).first()
    if existing_customer:
        return jsonify({"message": "Customer with the same name already exists"}), 400

    # Create a new customer    
    new_customer = Customer(name=name, city=city, age=age)
    session.add(new_customer)
    session.commit()
    return jsonify({"message": "Customer added successfully"}), 201

def display_all_customers(session: Session):
    customers = session.query(Customer).all()
    customer_list = [{"id": customer.id, "name": customer.name, "city": customer.city, "age": customer.age} for customer in customers]
    return jsonify({"customers": customer_list})

def find_customer_by_name(session: Session, name: str):
    customer = session.query(Customer).filter_by(name=name).first()
    if customer:
        return jsonify({"customer": {"id": customer.id, "name": customer.name, "city": customer.city, "age": customer.age}})
    else:
        return jsonify({"message": "Customer not found"}), 404

def remove_customer(session: Session, customer_id: int):
    customer = session.query(Customer).filter_by(id=customer_id).first()
    if customer:
        # Unactivate the customer to prevent from removing customer that have active loan
        customer.active = False
        session.commit()
        return jsonify({"message": "Customer removed successfully"}), 200
    else:
        return jsonify({"message": "Customer not found"}), 404
