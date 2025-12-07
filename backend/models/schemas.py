"""
to be implemented at a latter time 
"""

from pydantic import BaseModel, Field
from typing import Optional

class RegisterRequest(BaseModel):
    telegram_id: str = Field(..., min_length=1)

class UserProfile(BaseModel):
    telegram_id: str
    credits: int
    is_trial_active: bool
    trial_remaining: int

class ProcessMessageRequest(BaseModel):
    telegram_id: str
    text: str = Field(..., min_length=1)

class ProcessMessageResponse(BaseModel):
    reply: str
    remaining_credits: int

class PaymentCreateRequest(BaseModel):
    telegram_id: str
    amount: int = Field(..., gt=0)
    currency: Optional[str] = "RUB"

class PaymentCompleteRequest(BaseModel):
    telegram_id: str
    transaction_id: str
    provider: str
    amount: int
    status: str