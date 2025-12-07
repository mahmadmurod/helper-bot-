
"""
To be done: 
get dev3 to complete crud
proper description to be added later
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.dependencies import get_session
from backend.models.schemas import ProcessMessageRequest, ProcessMessageResponse
from backend.services.ai_service import get_default_adapter
from backend.utils.logger import logger
from backend.database import crud
from backend.utils.exceptions import NotEnoughCredits, AIServiceError

router = APIRouter(prefix="/api/v1")


@router.post("/process_message", response_model=ProcessMessageResponse)
async def process_message(payload: ProcessMessageRequest, session: AsyncSession = Depends(get_session)):
    user = await crud.get_user_by_telegram(session, payload.telegram_id)
    if not user:
        user = await crud.get_or_create_user(session, payload.telegram_id)

    if not ((user.is_trial_active and (user.trial_remaining or 0) > 0) or (user.credits or 0) > 0):
        raise NotEnoughCredits("No credits or active trial")

    charged_trial = False
    if user.is_trial_active and (user.trial_remaining or 0) > 0:
        user.trial_remaining = (user.trial_remaining or 0) - 1
        if user.trial_remaining <= 0:
            user.is_trial_active = False
        session.add(user)
        await session.flush()
        charged_trial = True
    else:
        user.credits = (user.credits or 0) - 1
        session.add(user)
        await session.flush()

    ai = get_default_adapter()
    try:
        reply = await ai.generate(payload.text)
    except Exception as exc:
        logger.exception("AI error for user=%s", payload.telegram_id)
        try:
            if charged_trial:
                user.trial_remaining = (user.trial_remaining or 0) + 1
                user.is_trial_active = True
                session.add(user)
                await session.flush()
            else:
                user.credits = (user.credits or 0) + 1
                session.add(user)
                await session.flush()
        except Exception:
            logger.exception("Failed to refund after AI error for user=%s", payload.telegram_id)
        raise AIServiceError()

    await crud.log_message(session, user, payload.text, reply)
    await session.flush()

    remaining = int(user.credits or 0)
    return ProcessMessageResponse(reply=reply, remaining_credits=remaining)
