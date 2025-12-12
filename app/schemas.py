from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    username: str
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class UserPasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6, max_length=100)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Calculation Schemas
class CalculationBase(BaseModel):
    operation: str = Field(..., pattern="^(add|subtract|multiply|divide|power|modulus|sqrt)$")
    operand1: float
    operand2: float


class CalculationCreate(CalculationBase):
    pass


class CalculationUpdate(BaseModel):
    operation: Optional[str] = Field(None, pattern="^(add|subtract|multiply|divide|power|modulus|sqrt)$")
    operand1: Optional[float] = None
    operand2: Optional[float] = None


class CalculationRead(CalculationBase):
    id: int
    result: float
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Statistics/Reports Schemas
class OperationBreakdown(BaseModel):
    """Breakdown of calculations by operation type."""
    operation: str
    count: int
    percentage: float


class CalculationStats(BaseModel):
    """Statistics and metrics for user's calculations."""
    total_calculations: int
    operations_breakdown: List[OperationBreakdown]
    average_operand1: Optional[float] = None
    average_operand2: Optional[float] = None
    most_used_operation: Optional[str] = None
    recent_calculations: List[CalculationRead]
