"""Customer CRUD service."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.utils.logger import get_logger
from app.utils.pagination import paginate

logger = get_logger(__name__)


def create_customer(db: Session, data: CustomerCreate) -> Customer:
    """Create a new customer."""
    if data.phone:
        existing = db.query(Customer).filter(Customer.phone == data.phone).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Customer with phone '{data.phone}' already exists")
    if data.email:
        existing = db.query(Customer).filter(Customer.email == data.email).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Customer with email '{data.email}' already exists")

    customer = Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    logger.info(f"Created customer: {customer.name} (id={customer.id})")
    return customer


def get_customer(db: Session, customer_id: int) -> Customer:
    """Get a customer by ID."""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with id {customer_id} not found")
    return customer


def get_all_customers(
    db: Session,
    page: int = 1,
    per_page: int = 20,
    search: str | None = None,
) -> dict:
    """Get all customers with optional search and pagination."""
    query = db.query(Customer).order_by(Customer.name)
    if search:
        query = query.filter(
            Customer.name.ilike(f"%{search}%")
            | Customer.phone.ilike(f"%{search}%")
            | Customer.email.ilike(f"%{search}%")
        )
    return paginate(query, page, per_page)


def get_customer_orders(db: Session, customer_id: int) -> list:
    """Get all orders for a specific customer."""
    customer = get_customer(db, customer_id)
    return customer.orders


def update_customer(db: Session, customer_id: int, data: CustomerUpdate) -> Customer:
    """Update an existing customer."""
    customer = get_customer(db, customer_id)
    update_data = data.model_dump(exclude_unset=True)

    if "phone" in update_data and update_data["phone"]:
        existing = db.query(Customer).filter(Customer.phone == update_data["phone"], Customer.id != customer_id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Phone '{update_data['phone']}' already in use")

    if "email" in update_data and update_data["email"]:
        existing = db.query(Customer).filter(Customer.email == update_data["email"], Customer.id != customer_id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{update_data['email']}' already in use")

    for field, value in update_data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    logger.info(f"Updated customer: {customer.name} (id={customer.id})")
    return customer


def delete_customer(db: Session, customer_id: int) -> None:
    """Delete a customer."""
    customer = get_customer(db, customer_id)
    db.delete(customer)
    db.commit()
    logger.info(f"Deleted customer: {customer.name} (id={customer_id})")
