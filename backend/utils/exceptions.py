"""
PURPOSE:
Exceptions that can be raised throughout the
application and will be caught by the global exception handlers in main.py.

EXCEPTIONS:
NotEnoughCredits 402: User lacks sufficient credits for operation
UserNotFound  404: Requested user does not exist in the system
PaymentValidationError 400: Payment data failed validation checks
AIServiceError  500: AI provider service failed or returned an error
"""

from fastapi import HTTPException, status

class NotEnoughCredits(HTTPException):
    def __init__(self, detail: str = "Not enough credits"):
        super().__init__(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=detail)

class UserNotFound(HTTPException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class PaymentValidationError(HTTPException):
    def __init__(self, detail: str = "Payment validation failed"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class AIServiceError(HTTPException):
    def __init__(self, detail: str = "AI service error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)