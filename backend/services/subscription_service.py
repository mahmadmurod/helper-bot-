"""
dev2 to be implement description later
crud functions should be provided by dev3 in backend.database.crud
"""

from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils.logger import logger
from backend.config import settings
from backend.database import crud
from backend.utils.exceptions import UserNotFound

async def start_trial(session: AsyncSession, telegram_id: str):
    user = await crud.get_or_create_user(session, telegram_id)
    if user.is_trial_active:
        logger.info("Trial already active for %s", telegram_id)
        return user
    user.is_trial_active = True
    user.trial_remaining = settings.TRIAL_DEFAULT_MESSAGES
    session.add(user)
    await session.flush()
    logger.info("Started trial for %s, remaining=%s", telegram_id, user.trial_remaining)
    return user


async def has_access(session: AsyncSession, user) -> bool:
    if user.is_trial_active and (user.trial_remaining and user.trial_remaining > 0):
        return True
    if (user.credits or 0) > 0:
        return True
    return False
