"""
dev2 to be implement description later
crud functions should be provided by dev3 in backend.database.crud
"""

from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import crud 
from backend.utils.logger import logger
from backend.utils.exceptions import PaymentValidationError
# crud functions should be provided by dev3 in backend.database.crud

async def create_invoice(session: AsyncSession, user, amount: int, provider: str = "telegram"):
    tx = await crud.create_transaction(session, user, amount, provider)
    await session.flush()
    logger.info("Created transaction %s for user %s amount=%s", tx.id, user.telegram_id, amount)
    return tx


async def confirm_payment(session: AsyncSession, tx, status: str):
    tx = await crud.complete_transaction(session, tx, status)
    if status.lower() == "successful" or status.lower() == "succeeded":
        await crud.change_credits(session, tx.user, tx.amount)
        logger.info("Applied %s credits to user %s via tx %s", tx.amount, tx.user.telegram_id, tx.id)
    else:
        logger.info("Transaction %s completed with status %s", tx.id, status)
    return tx


async def validate_payment_payload(payload: dict) -> bool:
    # Basic validation, more complex checks should be doneby dev4
    if "transaction_id" not in payload or "status" not in payload:
        raise PaymentValidationError("Missing transaction_id or status")
    return True
