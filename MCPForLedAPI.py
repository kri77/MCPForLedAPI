from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="MCP LED Intent Controller for LedAPI")

LED_API_BASE = "http://localhost:5000"

# Context Model
class IntentRequest(BaseModel):
    intent: str
    parameters: dict = {}

# LED Pattern Translator
def set_led_pattern(pattern: str):
    if len(pattern) != 4 or any(c not in "01" for c in pattern):
        raise ValueError("Invalid LED pattern format.")
    res = requests.post(f"{LED_API_BASE}/setLedStatus", json={"pattern": pattern})
    return res.json()

def get_led_status():
    res = requests.get(f"{LED_API_BASE}/status")
    return res.json()

# Intent Dispatcher
def handle_intent(intent: str, parameters: dict):
    intent = intent.lower()

    if intent == "turnonled":
        color = parameters.get("color", "").lower()
        pattern = {
            "red": "1000",
            "yellow": "0100",
            "green": "0010",
            "blue": "0001"
        }.get(color)
        if not pattern:
            raise ValueError(f"Unsupported color: {color}")
        return set_led_pattern(pattern)

    elif intent == "turnoffled":
        return set_led_pattern("0000")

    elif intent == "setpattern":
        pattern = parameters.get("pattern", "")
        return set_led_pattern(pattern)

    elif intent == "powerdown":
        return set_led_pattern("0000")

    elif intent == "getstatus":
        return get_led_status()

    elif intent == "setmood":
        mood = parameters.get("mood", "").lower()
        mood_patterns = {
            "calm": "0001",       # blue
            "alert": "1111",      # all
            "focus": "0010",      # green
            "idle": "0000",        # off
             # Energy levels
            "energetic": "1100",  # red + yellow (warm, high energy)
            "relaxed": "0011",    # green + blue (cool, peaceful)
            "sleepy": "0001",     # blue (same as calm, or could be "0000")
            
            # Emotional states
            "happy": "0110",      # yellow + green (bright, positive)
            "excited": "1010",    # red + green (festive, christmas-y)
            "creative": "1001",   # red + blue (purple-ish, artistic)
            "warning": "1000",    # red only
            "caution": "0100",    # yellow only
            
            # Work modes
            "busy": "1110",       # all except blue (active but not overwhelming)
            "thinking": "0011",   # green + blue (cool, contemplative)
            "success": "0010",    # green (achievement, go)
            "error": "1000",      # red (problem)
            
            # Special
            "party": "1111",      # all (celebration) TODO: could be dynamic flashing
            "night": "0001",      # blue (gentle night light)
            "sunrise": "1100",    # red + yellow (warm awakening)
            "sunset": "1010"      # red + green (transitional)
        }
        pattern = mood_patterns.get(mood)
        if not pattern:
            raise ValueError(f"Unsupported mood: {mood}")
        return set_led_pattern(pattern)

    else:
        raise ValueError(f"Unknown intent: {intent}")

# API Endpoint
@app.post("/intent")
def intent_router(request: IntentRequest):
    try:
        result = handle_intent(request.intent, request.parameters)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# Swagger UI: http://localhost:8000/docs
# Redoc:      http://localhost:8000/redoc


