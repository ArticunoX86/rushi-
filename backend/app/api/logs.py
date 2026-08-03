from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel

from app.database.session import get_db
from app.models.app_log import AppLog
from app.core.logger import logger

router = APIRouter(
    prefix="/logs",
    tags=["logs"],
)

class LogEntry(BaseModel):
    log_level: str
    message: str
    timestamp: str

class BatchLogsRequest(BaseModel):
    device_identifier: str
    logs: List[LogEntry]

@router.post("/batch", status_code=status.HTTP_201_CREATED)
def submit_logs_batch(
    request: BatchLogsRequest,
    db: Session = Depends(get_db)
):
    """
    Submit a batch of logs from the Flutter application.
    """
    try:
        app_logs = []
        for log in request.logs:
            try:
                # Handle isoformat with potential timezone 'Z' 
                dt_str = log.timestamp.replace('Z', '+00:00')
                dt = datetime.fromisoformat(dt_str)
            except ValueError:
                dt = datetime.utcnow()
                
            app_log = AppLog(
                device_identifier=request.device_identifier,
                log_level=log.log_level,
                message=log.message,
                timestamp=dt
            )
            app_logs.append(app_log)
        
        db.add_all(app_logs)
        db.commit()
        return {"status": "success", "count": len(app_logs)}
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to submit logs batch: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save logs"
        )
