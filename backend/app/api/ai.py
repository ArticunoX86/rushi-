from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session


from app.database.session import get_db


from app.schemas.ai import (
    AIChatRequest,
    AIChatResponse,
)


from app.services.ai_service import (
    process_customer_message,
)



router = APIRouter(
    prefix="/ai",
    tags=["AI Brain"],
)



# ==================================================
# AI CHAT SIMULATION
# ==================================================

@router.post(
    "/chat",
    response_model=AIChatResponse,
)
def ai_chat(
    request: AIChatRequest,
    db: Session = Depends(get_db),
):

    response = process_customer_message(
        db,
        request,
    )


    return response