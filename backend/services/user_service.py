"""
dev2 to be implement proper description later
dev3 to add crud functions 
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from backend.utils.logger import logger
from backend.models.schemas import RegisterRequest, UserProfile
from backend.utils.exceptions import UserNotFound
from backend.database import crud


async def register_user(session: AsyncSession, telegram_id: str):
    user = await crud.get_or_create_user(session, telegram_id)
    logger.info("Registered user %s", telegram_id)
    return user


async def get_profile(session: AsyncSession, telegram_id: str) -> UserProfile:
    user = await crud.get_user_by_telegram(session, telegram_id)
    if not user:
        raise UserNotFound()
    return UserProfile(
        telegram_id=user.telegram_id,
        credits=int(user.credits or 0),
        is_trial_active=bool(user.is_trial_active),
        trial_remaining=int(user.trial_remaining or 0),
    )


async def change_user_credits(session: AsyncSession, telegram_id: str, delta: int):
    user = await crud.get_or_create_user(session, telegram_id)
    await crud.change_credits(session, user, delta)
    await session.flush()
    logger.info("Changed credits for %s by %s -> now %s", telegram_id, delta, user.credits)
    return user
