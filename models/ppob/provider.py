from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Provider(Base):
    __tablename__ = "providers"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    api_url = Column(String(255))
    api_key = Column(String(255))
    is_active = Column(Boolean, default=True)
    
    products = relationship("PPOBProduct", back_populates="provider")