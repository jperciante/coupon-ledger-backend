from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from .. import models, schemas, database, security

router = APIRouter(tags=["creditCardCouponsAPI"])

@router.post("/",
           response_model=schemas.CardCouponCreate,
           status_code=status.HTTP_201_CREATED)
def create_card_coupon(
    coupon: schemas.CardCouponCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    # Validate credit card last 4 digits
    if not coupon.credit_card_last4.isdigit() or len(coupon.credit_card_last4) != 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credit card last 4 digits"
        )

    db_coupon = models.CardCoupon(
        **coupon.model_dump(),
        user_id=current_user.id,
        is_used=False
    )
    
    try:
        db.add(db_coupon)
        db.commit()
        db.refresh(db_coupon)
        return db_coupon
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating card coupon: {str(e)}"
        )

@router.get("/", response_model=list[schemas.CardCouponCreate])
def get_card_cupons(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    return db.query(models.CardCoupon)\
           .filter(models.CardCoupon.user_id == current_user.id)\
           .all()