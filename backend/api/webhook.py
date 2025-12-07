"""
Docstring for helper-bot-.backend.api.webhook
to be properlu described later
"""

from fastapi import APIRouter, Request, Depends
from backend.api.dependencies import get_session
from backend.utils.logger import logger

router = APIRouter(prefix="/webhook")

@router.post("/telegram/{token}")
async def telegram_webhook(token: str, request: Request, session=Depends(get_session)):
    # webhook receiver, shojld delegate to bot (Dev1)
    # Actual webhook processing should be handled by bot or forwarded to bot service.
    body = await request.json()
    logger.info("Received webhook for token=%s payload_keys=%s", token, list(body.keys()))
    return {"ok": True}
