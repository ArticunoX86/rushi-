from fastapi import APIRouter, Request, HTTPException
from app.core.logger import logger

# We already have logger from app.core.logger

router = APIRouter()

@router.post("/webhook")
async def handle_tata_webhook(request: Request):
    """
    TATA Smartflo will send event updates here (Ringing, Answered, Completed).
    """
    try:
        payload = await request.json()
        logger.info(f"Received TATA Webhook: {payload}")
        
        call_id = request.query_params.get("call_id")
        event = payload.get("event")
        
        if event == "call.answered":
            logger.info(f"Call {call_id} was answered. Streaming audio...")
            # Here we would initialize the LiveKit WebRTC bridge or Audio socket
            pass
            
        elif event == "call.completed":
            logger.info(f"Call {call_id} completed. Generating insights...")
            # Mocking AI summarization and scoring
            mock_lead_score = payload.get("lead_score", 95)
            
            if mock_lead_score > 90:
                logger.info(f"🔥 HOT LEAD DETECTED on call {call_id} with score {mock_lead_score}! Broadcasting push notification.")
                from app.services.device_connection_manager import device_manager
                import asyncio
                
                asyncio.create_task(device_manager.broadcast_all({
                    "action": "HOT_LEAD_ALERT",
                    "event": "HOT_LEAD_ALERT",
                    "payload": {
                        "call_id": call_id,
                        "lead_score": mock_lead_score,
                        "message": f"Hot Lead Alert! Customer scored {mock_lead_score}/100. Call back immediately!"
                    }
                }))
            
        elif event == "sentiment_update":
            sentiment = payload.get("sentiment", "neutral")
            if sentiment == "highly_negative":
                logger.warning(f"🚨 Negative sentiment detected on call {call_id}! Triggering Supervisor Handover! 🚨")
                from app.services.tata_telephony_service import tata_telephony_service
                tata_telephony_service.transfer_call(str(call_id))

        return {"status": "success"}

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")
