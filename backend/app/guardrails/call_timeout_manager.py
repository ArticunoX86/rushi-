"""
Call Timeout Manager — Enforces hard time and turn limits on AI calls.

Prevents calls from running indefinitely due to:
- Looping conversations
- Trolling users
- System malfunctions
"""

import time
from dataclasses import dataclass, field
from app.core.config import settings


# ==================================================
# CALL SESSION TRACKER
# ==================================================

@dataclass
class CallSession:
    """Tracks timing and turn data for a single active call."""
    call_id: str
    start_time: float = field(default_factory=time.time)
    turn_count: int = 0
    max_duration: int = 600     # seconds (overridden from config)
    max_turns: int = 30         # (overridden from config)
    is_forcefully_ended: bool = False


# ==================================================
# GLOBAL CALL REGISTRY
# ==================================================

_active_sessions: dict[str, CallSession] = {}


# ==================================================
# MANAGEMENT FUNCTIONS
# ==================================================

def register_call(call_id: str) -> CallSession:
    """Register a new call and start the timer."""
    session = CallSession(
        call_id=call_id,
        start_time=time.time(),
        max_duration=settings.AI_MAX_CALL_DURATION,
        max_turns=settings.AI_MAX_TURNS_PER_CALL,
    )
    _active_sessions[call_id] = session
    return session


def increment_turn(call_id: str) -> int:
    """Increment the turn counter for a call. Returns new turn count."""
    session = _active_sessions.get(call_id)
    if session:
        session.turn_count += 1
        return session.turn_count
    return 0


def is_call_expired(call_id: str) -> tuple[bool, str]:
    """
    Check if a call has exceeded its time or turn limits.

    Returns:
        (is_expired: bool, reason: str)
    """
    session = _active_sessions.get(call_id)
    if not session:
        return False, ""

    # Check time limit
    elapsed = time.time() - session.start_time
    if elapsed >= session.max_duration:
        return True, f"Call exceeded maximum duration ({session.max_duration}s). Elapsed: {elapsed:.0f}s"

    # Check turn limit
    if session.turn_count >= session.max_turns:
        return True, f"Call exceeded maximum turns ({session.max_turns}). Turns used: {session.turn_count}"

    return False, ""


def get_remaining_time(call_id: str) -> float:
    """Get remaining time in seconds for a call."""
    session = _active_sessions.get(call_id)
    if not session:
        return 0.0
    elapsed = time.time() - session.start_time
    return max(0.0, session.max_duration - elapsed)


def get_session_info(call_id: str) -> dict:
    """Get full session info for logging/debugging."""
    session = _active_sessions.get(call_id)
    if not session:
        return {"call_id": call_id, "status": "NOT_FOUND"}

    elapsed = time.time() - session.start_time
    return {
        "call_id": call_id,
        "elapsed_seconds": round(elapsed, 1),
        "remaining_seconds": round(max(0, session.max_duration - elapsed), 1),
        "turn_count": session.turn_count,
        "max_turns": session.max_turns,
        "max_duration": session.max_duration,
        "is_forcefully_ended": session.is_forcefully_ended,
    }


def force_end_call(call_id: str):
    """Mark a call as forcefully ended (by supervisor or guardrail)."""
    session = _active_sessions.get(call_id)
    if session:
        session.is_forcefully_ended = True


def unregister_call(call_id: str):
    """Clean up when a call ends."""
    _active_sessions.pop(call_id, None)


# ==================================================
# GRACEFUL TIMEOUT MESSAGES
# ==================================================

TIMEOUT_MESSAGE = (
    "Hey, I really appreciate your time today! I've shared a lot of information, "
    "so let me send you a quick summary on WhatsApp so you can review everything "
    "at your convenience. Thank you and have a great day!"
)

TURN_LIMIT_MESSAGE = (
    "I've really enjoyed our conversation! I think the best next step would be "
    "for me to send you all the details we discussed, and you can take your time "
    "going through them. Sound good? Thank you!"
)

def get_timeout_message(call_id: str) -> str:
    """Get the appropriate graceful exit message based on expiry reason."""
    session = _active_sessions.get(call_id)
    if not session:
        return TIMEOUT_MESSAGE

    elapsed = time.time() - session.start_time
    if elapsed >= session.max_duration:
        return TIMEOUT_MESSAGE

    if session.turn_count >= session.max_turns:
        return TURN_LIMIT_MESSAGE

    return TIMEOUT_MESSAGE
