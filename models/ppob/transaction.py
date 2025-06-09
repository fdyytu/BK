from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class TransactionStatus(enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class PPOBTransaction(Base):
    __tablename__ = "ppob_transactions"
    
    id = Column(Integer, primary_key=True)
    reference_id = Column(String(50), unique=True, nullable=False)
    product_id = Column(Integer, ForeignKey('ppob_products.id'), nullable=False)
    customer_id = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    admin_fee = Column(Float, default=0)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    product = relationship("PPOBProduct", back_populates="transactions")