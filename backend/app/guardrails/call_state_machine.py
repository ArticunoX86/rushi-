"""
Call State Machine — Graph-based conversation flow control.

Instead of giving the AI one open-ended prompt, the call is broken into
discrete states. At each state, the AI receives a narrow, focused prompt
that constrains its behavior to only the current goal.
"""

from enum import Enum
from dataclasses import dataclass, field


# ==================================================
# CALL STATES
# ==================================================

class CallState(str, Enum):
    """Discrete states in a sales call conversation flow."""
    INTRODUCTION = "INTRODUCTION"
    QUALIFICATION = "QUALIFICATION"
    PROPERTY_PITCH = "PROPERTY_PITCH"
    OBJECTION_HANDLING = "OBJECTION_HANDLING"
    BOOKING = "BOOKING"
    CLOSING = "CLOSING"


# ==================================================
# STATE-SPECIFIC PROMPT ADDITIONS
# ==================================================

STATE_PROMPTS = {
    CallState.INTRODUCTION: """
### CURRENT PHASE: INTRODUCTION
Your ONLY goal right now is to greet the customer warmly and confirm their identity.
- Introduce yourself by name (use the agent name from settings).
- Confirm: "Am I speaking with {lead_name}?"
- DO NOT pitch any properties yet.
- DO NOT ask about budget or requirements yet.
- Keep it to 1-2 sentences MAX.
""",

    CallState.QUALIFICATION: """
### CURRENT PHASE: QUALIFICATION
Your ONLY goal right now is to understand the customer's property requirements.
- Ask about their preferred city/location.
- Ask about their budget range.
- Ask about BHK preference (1/2/3/4 BHK).
- Ask about timeline (when do they plan to buy?).
- DO NOT pitch specific properties yet — you need their requirements first.
- DO NOT discuss prices of specific properties.
- Keep questions conversational, not interrogative.
""",

    CallState.PROPERTY_PITCH: """
### CURRENT PHASE: PROPERTY PITCH
Your ONLY goal right now is to present 1-2 matching properties from the Available Properties list.
- ONLY mention properties from the "Available Properties to Pitch" list below.
- NEVER invent or fabricate properties, prices, amenities, or locations.
- Highlight features that match their stated preferences.
- Use phrases like "based on what you told me" and "from what's available".
- Keep descriptions brief and enticing (1-2 key selling points per property).
- After pitching, ask if they'd like to schedule a visit.
""",

    CallState.OBJECTION_HANDLING: """
### CURRENT PHASE: OBJECTION HANDLING
The customer has raised an objection or concern. Handle it gracefully.
- Acknowledge their concern genuinely — DO NOT dismiss it.
- Address the specific objection with facts from the property data.
- You may attempt a maximum of 2 soft counter-objections.
- If they remain uninterested after 2 attempts, gracefully offer to follow up later.
- NEVER be aggressive, guilt-trip, or use high-pressure tactics.
- NEVER say "you're making a mistake" or "you'll regret this".
- If they say "not interested", respect it and move to CLOSING.
""",

    CallState.BOOKING: """
### CURRENT PHASE: BOOKING
The customer has shown interest in visiting a property. Help them schedule.
- Ask for their preferred date and time for a site visit.
- Confirm the property they want to visit.
- Tell them: "I'll set this up as a tentative appointment and our team will confirm shortly."
- NEVER guarantee a specific time slot — say "tentative" or "subject to confirmation".
- NEVER make commitments on behalf of the sales team.
- Collect their preferred contact method for confirmation (call/WhatsApp).
""",

    CallState.CLOSING: """
### CURRENT PHASE: CLOSING
The conversation is wrapping up. End it professionally.
- Thank the customer for their time.
- Summarize any next steps (e.g., "I'll send details on WhatsApp" or "Our team will confirm your visit").
- Wish them a good day.
- Keep it to 1-2 sentences MAX.
- DO NOT introduce new topics or properties.
- DO NOT try to re-pitch if they said no.
""",
}


# ==================================================
# INTENT → STATE TRANSITION MAP
# ==================================================

# Maps (current_state, detected_intent) → next_state
TRANSITION_MAP = {
    # From INTRODUCTION
    (CallState.INTRODUCTION, "greeting"): CallState.QUALIFICATION,
    (CallState.INTRODUCTION, "property_requirement"): CallState.QUALIFICATION,
    (CallState.INTRODUCTION, "not_interested"): CallState.CLOSING,
    (CallState.INTRODUCTION, "UNKNOWN"): CallState.QUALIFICATION,

    # From QUALIFICATION
    (CallState.QUALIFICATION, "property_requirement"): CallState.PROPERTY_PITCH,
    (CallState.QUALIFICATION, "not_interested"): CallState.OBJECTION_HANDLING,
    (CallState.QUALIFICATION, "callback_request"): CallState.CLOSING,
    (CallState.QUALIFICATION, "UNKNOWN"): CallState.QUALIFICATION,

    # From PROPERTY_PITCH
    (CallState.PROPERTY_PITCH, "interested"): CallState.BOOKING,
    (CallState.PROPERTY_PITCH, "not_interested"): CallState.OBJECTION_HANDLING,
    (CallState.PROPERTY_PITCH, "callback_request"): CallState.CLOSING,
    (CallState.PROPERTY_PITCH, "property_requirement"): CallState.PROPERTY_PITCH,
    (CallState.PROPERTY_PITCH, "question"): CallState.PROPERTY_PITCH,
    (CallState.PROPERTY_PITCH, "UNKNOWN"): CallState.PROPERTY_PITCH,

    # From OBJECTION_HANDLING
    (CallState.OBJECTION_HANDLING, "interested"): CallState.BOOKING,
    (CallState.OBJECTION_HANDLING, "not_interested"): CallState.CLOSING,
    (CallState.OBJECTION_HANDLING, "callback_request"): CallState.CLOSING,
    (CallState.OBJECTION_HANDLING, "property_requirement"): CallState.PROPERTY_PITCH,
    (CallState.OBJECTION_HANDLING, "UNKNOWN"): CallState.CLOSING,

    # From BOOKING
    (CallState.BOOKING, "interested"): CallState.CLOSING,
    (CallState.BOOKING, "not_interested"): CallState.CLOSING,
    (CallState.BOOKING, "UNKNOWN"): CallState.CLOSING,

    # CLOSING is terminal — no transitions out
}


# ==================================================
# STATE MACHINE CLASS
# ==================================================

class CallStateMachine:
    """
    Manages the conversation state for a single call.
    """

    def __init__(self, call_id: str):
        self.call_id = call_id
        self.current_state = CallState.INTRODUCTION
        self.turn_count = 0
        self.objection_count = 0
        self.state_history: list[CallState] = [CallState.INTRODUCTION]

    def get_state_prompt(self) -> str:
        """Get the prompt addition for the current state."""
        return STATE_PROMPTS.get(self.current_state, "")

    def transition(self, detected_intent: str) -> CallState:
        """
        Determine the next state based on detected intent.
        Returns the new state.
        """
        self.turn_count += 1

        # Track objection attempts
        if self.current_state == CallState.OBJECTION_HANDLING:
            self.objection_count += 1
            # Force close after 2 objection handling attempts
            if self.objection_count >= 2 and detected_intent in ("not_interested", "UNKNOWN"):
                self.current_state = CallState.CLOSING
                self.state_history.append(self.current_state)
                return self.current_state

        # Look up transition
        key = (self.current_state, detected_intent)
        next_state = TRANSITION_MAP.get(key)

        if next_state:
            self.current_state = next_state
        elif self.current_state != CallState.CLOSING:
            # Default: stay in current state if no explicit transition
            pass

        self.state_history.append(self.current_state)
        return self.current_state

    def is_terminal(self) -> bool:
        """Check if the call has reached a terminal state."""
        return self.current_state == CallState.CLOSING

    def get_summary(self) -> dict:
        """Get a summary of the state machine for logging."""
        return {
            "call_id": self.call_id,
            "current_state": self.current_state.value,
            "turn_count": self.turn_count,
            "objection_count": self.objection_count,
            "state_history": [s.value for s in self.state_history],
        }


# ==================================================
# GLOBAL STATE REGISTRY
# ==================================================

# Stores active call state machines in memory (keyed by call_id)
_active_call_states: dict[str, CallStateMachine] = {}


def get_or_create_state_machine(call_id: str) -> CallStateMachine:
    """Get existing state machine for a call or create a new one."""
    if call_id not in _active_call_states:
        _active_call_states[call_id] = CallStateMachine(call_id)
    return _active_call_states[call_id]


def remove_state_machine(call_id: str):
    """Clean up state machine when a call ends."""
    _active_call_states.pop(call_id, None)
