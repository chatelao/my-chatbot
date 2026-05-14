import os
import json
import httpx
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from .schemas import ChatCompletionRequest

# Load environment variables
load_dotenv()

INFERENCE_API_BASE = os.getenv("INFERENCE_API_BASE", "http://localhost:11434/v1")
INFERENCE_API_KEY = os.getenv("INFERENCE_API_KEY", "ollama")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")
APP_API_KEY = os.getenv("APP_API_KEY", "dev-key")

API_KEY_NAME = "X-App-Api-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(header_key: str = Security(api_key_header)):
    if header_key == APP_API_KEY:
        return header_key
    else:
        raise HTTPException(
            status_code=401, detail="Could not validate API Key"
        )

app = FastAPI(title="AI Web Chatbot Backend")

@app.post("/api/chat/completions")
async def chat_completions(request: ChatCompletionRequest, api_key: str = Depends(get_api_key)):
    """
    OpenAI-compatible chat completions endpoint that proxies to a vLLM/Ollama engine.
    """
    # Use the model from request if provided, otherwise use default
    model = request.model if request.model != "stub-model" else MODEL_NAME

    payload = {
        "model": model,
        "messages": [m.model_dump() for m in request.messages],
        "stream": request.stream
    }

    headers = {
        "Authorization": f"Bearer {INFERENCE_API_KEY}",
        "Content-Type": "application/json"
    }

    async def stream_generator():
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream(
                    "POST",
                    f"{INFERENCE_API_BASE}/chat/completions",
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status_code != 200:
                        error_detail = await response.aread()
                        yield f"data: {json.dumps({'error': 'Inference engine error', 'detail': error_detail.decode()})}\n\n"
                        yield "data: [DONE]\n\n"
                        return

                    async for line in response.aiter_lines():
                        if line:
                            yield f"{line}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    if request.stream:
        return StreamingResponse(stream_generator(), media_type="text/event-stream")
    else:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{INFERENCE_API_BASE}/chat/completions",
                json=payload,
                headers=headers
            )
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            return response.json()

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "config": {
            "inference_api_base": INFERENCE_API_BASE,
            "model_name": MODEL_NAME
        }
    }

# Serve Frontend static files
FRONTEND_BUILD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "build")

if os.path.exists(FRONTEND_BUILD_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_BUILD_DIR, html=True), name="static")
else:
    @app.get("/")
    async def serve_index():
        return {"message": "Frontend build not found. Please run 'npm run build' in src/frontend."}
