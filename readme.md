# MCP LEDAPI Intent Controller 

This project implements a **Model Context Protocol (MCP)**-style server using **FastAPI** to control an Arduino-based LED system via a RESTful interface.
For best results, use this together with the MCPForLedAPI project.
It interprets high-level **intents** like `TurnOnLed`, `SetMood`, or `GetStatus`, and translates them into commands for the Arduino LED API.

---

## Features

- Supports contextual LED control via structured intents
- Communicates with an Arduino LED controller API (`/setLedStatus`, `/status`)
- Automatically exposes Swagger UI for testing
- Extensible architecture for adding new devices or control logic

---

## Intents Supported

| Intent       | Description                            | Parameters                    |
|--------------|----------------------------------------|-------------------------------|
| TurnOnLed    | Turns on a specific LED                | `{ "color": "red" }`          |
| TurnOffLed   | Turns off all LEDs                     | `none`                        |
| SetPattern   | Sets specific LED pattern              | `{ "pattern": "1100" }`       |
| SetMood      | Uses predefined mood pattern           | `{ "mood": "calm" }`          |
| PowerDown    | Alias for turning everything off       | `none`                        |
| GetStatus    | Queries the current LED state          | `none`                        |

---

## Example Requests

```json
POST /intent
{
  "intent": "TurnOnLed",
  "parameters": {
    "color": "green"
  }
}
```

```json
POST /intent
{
  "intent": "SetMood",
  "parameters": {
    "mood": "calm"
  }
}
```

---

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Requests

Install via:

```bash
pip install fastapi uvicorn requests
```

---

## Running the Server

```bash
uvicorn mcp_server:app --reload
```

Then open your browser at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc UI: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Architecture Overview

```
[ User or System ]
        ↓
  MCP Intent Server (FastAPI)
        ↓
Arduino LED API (Flask)
        ↓
      Arduino Nano (via USB)
```

---

## File Overview

- `MCPForLedAPI.py`: Main FastAPI server with intent handling logic
- `requirements.txt`: Python dependencies
- `README.md`: Project overview and usage

---


## License

MIT License
