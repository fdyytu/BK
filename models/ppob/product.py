from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class PPOBProduct(Base):
    __tablename__ = "ppob_products"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    provider_id = Column(Integer, ForeignKey('providers.id'), nullable=False)
    category = Column(String(50), nullable=False)  # PLN, PDAM, BPJS, etc
    type = Column(String(50), nullable=False)      # Prepaid, Postpaid
    is_active = Column(Boolean, default=True)
    
    provider = relationship("Provider", back_populates="products")
    transactions = relationship("PPOBTransaction", back_populates="product")