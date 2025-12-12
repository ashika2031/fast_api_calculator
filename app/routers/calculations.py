from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Calculation, User
from app.schemas import CalculationCreate, CalculationRead, CalculationUpdate, CalculationStats, OperationBreakdown
from app.auth import get_current_user
import math

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
    elif operation == "power":
        try:
            return operand1 ** operand2
        except (OverflowError, ValueError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Power calculation error: {str(e)}"
            )
    elif operation == "modulus":
        if operand2 == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Modulus by zero is not allowed"
            )
        return operand1 % operand2
    elif operation == "sqrt":
        # For sqrt, we use operand1 as the value and ignore operand2
        if operand1 < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Square root of negative number is not allowed"
            )
        return math.sqrt(operand1)
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


@router.get("/stats", response_model=CalculationStats)
def get_calculation_statistics(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get statistics and metrics for the current user's calculations.
    
    Returns:
    - total_calculations: Total number of calculations
    - operations_breakdown: Count and percentage for each operation type
    - average_operand1: Average value of first operand
    - average_operand2: Average value of second operand
    - most_used_operation: The most frequently used operation
    - recent_calculations: Most recent calculations (limited by limit parameter)
    """
    # Get all calculations for current user
    all_calculations = db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).all()
    
    total_calculations = len(all_calculations)
    
    # If no calculations, return empty stats
    if total_calculations == 0:
        return CalculationStats(
            total_calculations=0,
            operations_breakdown=[],
            average_operand1=None,
            average_operand2=None,
            most_used_operation=None,
            recent_calculations=[]
        )
    
    # Calculate operations breakdown
    operation_counts = db.query(
        Calculation.operation,
        func.count(Calculation.id).label('count')
    ).filter(
        Calculation.user_id == current_user.id
    ).group_by(Calculation.operation).all()
    
    operations_breakdown = [
        OperationBreakdown(
            operation=op,
            count=count,
            percentage=round((count / total_calculations) * 100, 2)
        )
        for op, count in operation_counts
    ]
    
    # Find most used operation
    most_used = max(operation_counts, key=lambda x: x.count) if operation_counts else None
    most_used_operation = most_used[0] if most_used else None
    
    # Calculate averages
    avg_stats = db.query(
        func.avg(Calculation.operand1).label('avg_operand1'),
        func.avg(Calculation.operand2).label('avg_operand2')
    ).filter(
        Calculation.user_id == current_user.id
    ).first()
    
    average_operand1 = round(float(avg_stats.avg_operand1), 2) if avg_stats.avg_operand1 else None
    average_operand2 = round(float(avg_stats.avg_operand2), 2) if avg_stats.avg_operand2 else None
    
    # Get recent calculations
    recent_calculations = db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).order_by(Calculation.created_at.desc()).limit(limit).all()
    
    return CalculationStats(
        total_calculations=total_calculations,
        operations_breakdown=operations_breakdown,
        average_operand1=average_operand1,
        average_operand2=average_operand2,
        most_used_operation=most_used_operation,
        recent_calculations=recent_calculations
    )


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
