from fastapi import FastAPI
from .routers import (
    users,
    card_cupons,
    sales_cupons,
    conciliados_cupons
)
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coupon Ledger API",
            version="1.0.0",
            docs_url="/api/docs")

app.include_router(users.router, prefix="/api/v1/auth")
app.include_router(
    card_cupons.router,
    prefix="/api/v1/credit-cards",
    tags=["Credit Card Coupons"]
)
app.include_router(
    sales_cupons.router,
    prefix="/api/v1/sales",
    tags=["Sales Coupons"]
)
app.include_router(
    conciliados_cupons.router,
    prefix="/api/v1/reconciliation",
    tags=["Reconciliation"]
)

# In app/main.py
from .routers import card_cupons  # Ensure this import exists

app.include_router(
    card_cupons.router,
    prefix="/api/v1/credit-cards",
    tags=["creditCardCouponsAPI"]
)