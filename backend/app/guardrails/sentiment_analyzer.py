"""
Sentiment Analyzer — Lightweight heuristic-based sentiment scoring.

Tracks per-call sentiment history and detects when user frustration
is rising, triggering supervisor alerts.
"""

import re
from dataclasses import dataclass, field
from app.core.config import settings


# ==================================================
# SENTIMENT RESULT
# ==================================================

@dataclass
class SentimentResult:
    """Result of sentiment analysis on a customer message."""
    score: float = 0.0          # -1.0 (angry) to +1.0 (positive)
    label: str = "NEUTRAL"      # POSITIVE | NEUTRAL | NEGATIVE | ANGRY
    should_alert: bool = False  # True if supervisor should be notified
    trigger_phrase: str = ""    # The phrase that triggered the alert


# ==================================================
# SENTIMENT KEYWORD DICTIONARIES
# ==================================================

POSITIVE_INDICATORS = {
    # (pattern, score_boost)
    r"(?<!not\s)\b(interested|yes|sure|great|perfect|wonderful|awesome|fantastic|good|nice|lovely|excellent)\b": 0.3,
    r"\b(tell me more|sounds good|i('d)? like|please|thank you|thanks)\b": 0.2,
    r"\b(when can i|how (do|can) i|i want to|sign me up|let'?s do it|book it)\b": 0.4,
    r"\b(amazing|love it|exactly|that'?s what i need)\b": 0.4,
}

NEGATIVE_INDICATORS = {
    r"\b(not interested|no thanks|don'?t (call|bother|want)|stop calling|remove (me|my number))\b": -0.4,
    r"\b(busy|not now|bad time|call (me )?later|another time)\b": -0.2,
    r"\b(expensive|too (much|costly|high)|can'?t afford|out of (my )?budget)\b": -0.2,
    r"\b(waste (of|my) time|useless|pointless|stupid|annoying|irritating)\b": -0.5,
    r"\b(fraud|scam|fake|cheat|liar|lying|dishonest)\b": -0.6,
    r"\b(shut up|go away|leave me alone|get lost|hang up)\b": -0.7,
    r"\b(idiot|fool|dumb|pathetic)\b": -0.8,
    r"\b(fuck|shit|damn|hell|ass|bastard|bitch)\b": -0.9,
    r"\b(i('ll| will) (complain|report|sue)|police|consumer (court|forum))\b": -0.8,
    r"\b(no|nope|nah|never)\b": -0.2,
}

# Pre-compile all patterns
_POSITIVE_PATTERNS = [
    (re.compile(pattern, re.IGNORECASE), boost)
    for pattern, boost in POSITIVE_INDICATORS.items()
]

_NEGATIVE_PATTERNS = [
    (re.compile(pattern, re.IGNORECASE), boost)
    for pattern, boost in NEGATIVE_INDICATORS.items()
]


# ==================================================
# PER-CALL SENTIMENT HISTORY
# ==================================================

_call_sentiment_history: dict[str, list[float]] = {}


# ==================================================
# ANALYSIS FUNCTION
# ==================================================

def analyze_sentiment(
    customer_message: str,
    call_id: str = None,
) -> SentimentResult:
    """
    Analyze the sentiment of a customer message using keyword heuristics.

    Tracks history per call_id to detect escalating frustration.
    """

    if not settings.AI_ENABLE_SENTIMENT_ALERTS:
        return SentimentResult(score=0.0, label="NEUTRAL")

    if not customer_message or len(customer_message.strip()) < 2:
        return SentimentResult(score=0.0, label="NEUTRAL")

    score = 0.0
    trigger_phrase = ""

    # Score positive indicators
    for pattern, boost in _POSITIVE_PATTERNS:
        match = pattern.search(customer_message)
        if match:
            score += boost

    # Score negative indicators
    for pattern, boost in _NEGATIVE_PATTERNS:
        match = pattern.search(customer_message)
        if match:
            score += boost  # boost is already negative
            if not trigger_phrase or boost < -0.5:
                trigger_phrase = match.group()

    # Clamp to [-1.0, 1.0]
    score = max(-1.0, min(1.0, score))

    # Determine label
    if score >= 0.3:
        label = "POSITIVE"
    elif score >= -0.2:
        label = "NEUTRAL"
    elif score >= -0.5:
        label = "NEGATIVE"
    else:
        label = "ANGRY"

    # Track history for trend detection
    should_alert = False
    if call_id:
        if call_id not in _call_sentiment_history:
            _call_sentiment_history[call_id] = []
        _call_sentiment_history[call_id].append(score)

        history = _call_sentiment_history[call_id]

        # Alert if current message is ANGRY
        if label == "ANGRY":
            should_alert = True

        # Alert if sentiment has been declining for 3+ consecutive turns
        if len(history) >= 3:
            recent = history[-3:]
            if all(s <= -0.2 for s in recent):
                should_alert = True

        # Alert if average sentiment over last 5 turns is very negative
        if len(history) >= 5:
            avg = sum(history[-5:]) / 5
            if avg < -0.3:
                should_alert = True

    return SentimentResult(
        score=round(score, 2),
        label=label,
        should_alert=should_alert,
        trigger_phrase=trigger_phrase,
    )


def get_call_sentiment_trend(call_id: str) -> dict:
    """Get the sentiment trend for a specific call."""
    history = _call_sentiment_history.get(call_id, [])
    if not history:
        return {"call_id": call_id, "trend": "UNKNOWN", "scores": []}

    avg = sum(history) / len(history)
    if avg >= 0.2:
        trend = "POSITIVE"
    elif avg >= -0.2:
        trend = "NEUTRAL"
    else:
        trend = "DECLINING"

    return {
        "call_id": call_id,
        "trend": trend,
        "average_score": round(avg, 2),
        "scores": history,
        "total_turns": len(history),
    }


def clear_call_sentiment(call_id: str):
    """Clean up sentiment history when a call ends."""
    _call_sentiment_history.pop(call_id, None)
