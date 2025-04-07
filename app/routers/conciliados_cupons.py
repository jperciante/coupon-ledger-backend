from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database, security

router = APIRouter(tags=["Conciliados Cupons"])

@router.post("/", 
           response_model=schemas.ConciliadosCuponsResponse,
           status_code=status.HTTP_201_CREATED)
def create_conciliados(
    conciliados_data: schemas.ConciliadosCuponsCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    # Validate at least one coupon provided
    if not conciliados_data.card_coupon_id and not conciliados_data.sales_coupon_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar al menos un cupón"
        )

    # Calculate final amount
    final_amount = conciliados_data.original_amount
    status = "pending"
    
    try:
        # Create reconciliation record
        db_conciliados = models.ConciliadosCupons(
            **conciliados_data.model_dump(),
            user_id=current_user.id,
            final_amount=final_amount,
            status=status
        )
        
        db.add(db_conciliados)
        db.commit()
        db.refresh(db_conciliados)
        
        return db_conciliados
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en conciliación: {str(e)}"
        )

@router.get("/", response_model=list[schemas.ConciliadosCuponsResponse])
def get_conciliados_history(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    return db.query(models.ConciliadosCupons)\
           .filter(models.ConciliadosCupons.user_id == current_user.id)\
           .all()