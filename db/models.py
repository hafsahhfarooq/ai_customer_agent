from sqlalchemy import Column, Integer, String, Date, func, VARCHAR
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(VARCHAR, unique=True, index=True, nullable=False)
    customer_name = Column(VARCHAR, nullable=False)
    customer_phone = Column(VARCHAR, nullable=True)
    customer_address = Column(VARCHAR, nullable=False)
    status = Column(String, nullable=False)
    estimated_delivery = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())