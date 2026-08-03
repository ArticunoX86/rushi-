from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.call import StartCallRequest
from app.services.call_dispatcher import start_ai_call


router = APIRouter(
    prefix="/call-dispatch",
    tags=["Call Dispatcher"],
)


@router.post("/start")
async def dispatch_call(
    request: StartCallRequest,
    db: Session = Depends(get_db),
):
    return await start_ai_call(
        db,
        request.lead_id,
    )