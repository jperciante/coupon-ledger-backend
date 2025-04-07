from sqlalchemy import Column, String, DateTime, Numeric, Boolean, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), 
              primary_key=True, 
              default=uuid.uuid4,
              index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    card_cupons = relationship("CardCoupon", back_populates="user")
    sales_cupons = relationship("SalesCoupon", back_populates="user")
    conciliados = relationship("ConciliadosCupons", back_populates="user")

class SalesCoupon(Base):
    __tablename__ = "sales_cupons"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, index=True)
    merchant = Column(String(100))
    discount_percent = Column(Numeric(5, 2))
    valid_until = Column(DateTime)
    is_used = Column(Boolean, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationship
    user = relationship("User", back_populates="sales_cupons")

class CardCoupon(Base):
    __tablename__ = "card_cupons"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, index=True)
    credit_card_last4 = Column(String(4))
    discount_value = Column(Numeric(10, 2))
    valid_from = Column(DateTime, server_default=func.now())
    valid_until = Column(DateTime)
    is_used = Column(Boolean, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationship
    user = relationship("User", back_populates="card_cupons")

class ConciliadosCupons(Base):
    __tablename__ = "conciliados_cupons"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_date = Column(DateTime, server_default=func.now())
    original_amount = Column(Numeric(10, 2))
    final_amount = Column(Numeric(10, 2))
    status = Column(String(20), default="pending")
    
    # Foreign Keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    card_coupon_id = Column(UUID(as_uuid=True), ForeignKey("card_cupons.id"))
    sales_coupon_id = Column(UUID(as_uuid=True), ForeignKey("sales_cupons.id"))
    
    # Relationships
    user = relationship("User", back_populates="conciliados")
    card_coupon = relationship("CardCoupon")
    sales_coupon = relationship("SalesCoupon")