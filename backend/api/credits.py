
"""
dev3 to provide crud 
dev2 to add a proper description later 
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.dependencies import get_session
from backend.models.schemas import UserProfile
from backend.utils.logger import logger
from backend.database import crud
from backend.utils.exceptions import UserNotFound


router = APIRouter(prefix="/api/v1")

@router.get("/get_credits", response_model=UserProfile)
async def get_credits(telegram_id: str, session: AsyncSession = Depends(get_session)):
    user = await crud.get_user_by_telegram(session, telegram_id)
    if not user:
        raise UserNotFound()
    return UserProfile(
        telegram_id=user.telegram_id,
        credits=int(user.credits or 0),
        is_trial_active=bool(user.is_trial_active),
        trial_remaining=int(user.trial_remaining or 0),
    )


@router.post("/update_credits")
async def update_credits(telegram_id: str, delta: int, session: AsyncSession = Depends(get_session)):
    user = await crud.get_or_create_user(session, telegram_id)
    await crud.change_credits(session, user, delta)
    await session.flush()
    logger.info("Updated credits for %s by %s -> now %s", telegram_id, delta, user.credits)
    return {"ok": True, "credits": int(user.credits or 0)}