from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID  # Correct UUID import

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

class CardCouponCreate(BaseModel):
    code: str
    credit_card_last4: str
    discount_value: float
    valid_until: datetime
    
    @field_validator('credit_card_last4')
    def validate_credit_card(cls, v):
        if len(v) != 4 or not v.isdigit():
            raise ValueError("Must be 4 digits")
        return v

class CardCouponResponse(CardCouponCreate):
    id: str
    is_used: bool
    user_id: str
    valid_from: datetime

class SalesCouponCreate(BaseModel):
    code: str
    merchant: str
    discount_percent: float
    valid_until: datetime

    @field_validator('discount_percent')
    def validate_discount(cls, v):
        if not 0 < v <= 100:
            raise ValueError("Discount must be between 1-100%")
        return v

class SalesCouponResponse(SalesCouponCreate):
    id: str
    is_used: bool
    user_id: str
    valid_from: datetime

class ConciliadosCuponsBase(BaseModel):
    original_amount: float
    card_coupon_id: Optional[UUID] = None
    sales_coupon_id: Optional[UUID] = None

class ConciliadosCuponsCreate(ConciliadosCuponsBase):
    pass

class ConciliadosCuponsResponse(ConciliadosCuponsBase):
    id: UUID
    transaction_date: datetime
    final_amount: float
    status: str
    user_id: UUID