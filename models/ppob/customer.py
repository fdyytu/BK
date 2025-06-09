from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True)
    customer_number = Column(String(50), unique=True, nullable=False)
    name = Column(String(100))
    service_type = Column(String(50))  # PLN, PDAM, BPJS, etc
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)