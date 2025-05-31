from fastapi import FastAPI, Depends, HTTPException, Query
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

DATABASE_URL = "sqlite:///./orders.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="Order Retrieval API")

# Database Model
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    product = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Float)
    order_date = Column(Date)

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/orders", response_model=List[dict])
def get_orders(
    customer_name: Optional[str] = Query(None, description="Filter by customer name"),
    product: Optional[str] = Query(None, description="Filter by product"),
    min_quantity: Optional[int] = Query(None, ge=1, description="Minimum quantity"),
    max_quantity: Optional[int] = Query(None, ge=1, description="Maximum quantity"),
    min_price: Optional[float] = Query(None, ge=0.0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0.0, description="Maximum price"),
    start_date: Optional[datetime] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    filters = []
    if customer_name:
        filters.append(Order.customer_name.ilike(f"%{customer_name}%"))
    if product:
        filters.append(Order.product.ilike(f"%{product}%"))
    if min_quantity is not None:
        filters.append(Order.quantity >= min_quantity)
    if max_quantity is not None:
        filters.append(Order.quantity <= max_quantity)
    if min_price is not None:
        filters.append(Order.price >= min_price)
    if max_price is not None:
        filters.append(Order.price <= max_price)
    if start_date:
        try:
            start = datetime.strptime(start_date.strftime('%Y-%m-%d'), '%Y-%m-%d').date()
            filters.append(Order.order_date >= start)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format")
    if end_date:
        try:
            end = datetime.strptime(end_date.strftime('%Y-%m-%d'), '%Y-%m-%d').date()
            filters.append(Order.order_date <= end)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format")

    orders = db.query(Order).filter(and_(*filters)).all()
    return [
        {
            "id": order.id,
            "customer_name": order.customer_name,
            "product": order.product,
            "quantity": order.quantity,
            "price": order.price,
            "order_date": order.order_date.isoformat(),
        }
        for order in orders
    ]