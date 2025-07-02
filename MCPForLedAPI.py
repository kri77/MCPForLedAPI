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
            "idle": "0000"        # off
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


