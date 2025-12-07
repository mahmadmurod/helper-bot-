"""
Docstring for helper-bot-.backend.api.trial
to be properly decribe later 
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.dependencies import get_session
from backend.services.subscription_service import start_trial
from backend.utils.logger import logger

router = APIRouter(prefix="/api/v1")

@router.post("/start_trial")
async def start_trial_endpoint(telegram_id: str, session: AsyncSession = Depends(get_session)):
    user = await start_trial(session, telegram_id)
    await session.flush()
    logger.info("Trial started for %s", telegram_id)
    return {"ok": True, "trial_remaining": int(user.trial_remaining or 0)}
