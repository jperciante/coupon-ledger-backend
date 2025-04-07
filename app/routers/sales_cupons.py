from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database, security

router = APIRouter()

@router.post("/",
           response_model=schemas.SalesCouponCreate,
           status_code=status.HTTP_201_CREATED)
def create_sales_coupon(
    coupon: schemas.SalesCouponCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    db_coupon = models.SalesCoupon(
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
            detail=f"Error creating coupon: {str(e)}"
        )

@router.get("/", response_model=list[schemas.SalesCouponCreate])
def get_sales_coupons(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    return db.query(models.SalesCoupon)\
           .filter(models.SalesCoupon.user_id == current_user.id)\
           .all()