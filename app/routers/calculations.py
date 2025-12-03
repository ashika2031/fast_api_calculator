from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Calculation, User
from app.schemas import CalculationCreate, CalculationRead, CalculationUpdate
from app.auth import get_current_user

router = APIRouter(prefix="/calculations", tags=["calculations"])


def perform_calculation(operation: str, operand1: float, operand2: float) -> float:
    """Perform the calculation based on the operation."""
    if operation == "add":
        return operand1 + operand2
    elif operation == "subtract":
        return operand1 - operand2
    elif operation == "multiply":
        return operand1 * operand2
    elif operation == "divide":
        if operand2 == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Division by zero is not allowed"
            )
        return operand1 / operand2
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid operation"
        )


@router.post("/", response_model=CalculationRead, status_code=status.HTTP_201_CREATED)
def add_calculation(
    calculation: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new calculation (CREATE)."""
    # Perform the calculation
    result = perform_calculation(
        calculation.operation,
        calculation.operand1,
        calculation.operand2
    )
    
    # Create calculation record
    db_calculation = Calculation(
        operation=calculation.operation,
        operand1=calculation.operand1,
        operand2=calculation.operand2,
        result=result,
        user_id=current_user.id
    )
    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)
    
    return db_calculation


@router.get("/", response_model=List[CalculationRead])
def browse_calculations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Browse all calculations for the current user (BROWSE)."""
    calculations = db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return calculations


@router.get("/{calculation_id}", response_model=CalculationRead)
def read_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Read a specific calculation by ID (READ)."""
    calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    return calculation


@router.put("/{calculation_id}", response_model=CalculationRead)
def edit_calculation(
    calculation_id: int,
    calculation_update: CalculationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Edit an existing calculation (EDIT)."""
    calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    # Update fields if provided
    update_data = calculation_update.model_dump(exclude_unset=True)
    
    if update_data:
        for field, value in update_data.items():
            setattr(calculation, field, value)
        
        # Recalculate the result
        calculation.result = perform_calculation(
            calculation.operation,
            calculation.operand1,
            calculation.operand2
        )
        
        db.commit()
        db.refresh(calculation)
    
    return calculation


@router.delete("/{calculation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a calculation (DELETE)."""
    calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    db.delete(calculation)
    db.commit()
    
    return None
