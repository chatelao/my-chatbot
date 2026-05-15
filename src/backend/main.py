import os
import json
import httpx
import logging
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.security.api_key import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from dotenv import load_dotenv
from .schemas import ChatCompletionRequest, SessionResponse, SessionCreate
from .database import init_db, get_db, async_session
from .models import Session, Message

# Load environment variables
load_dotenv()

INFERENCE_API_BASE = os.getenv("INFERENCE_API_BASE", "http://localhost:11434/v1")
INFERENCE_API_KEY = os.getenv("INFERENCE_API_KEY", "ollama")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")
APP_API_KEY = os.getenv("APP_API_KEY", "dev-key")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="AI Web Chatbot Backend", lifespan=lifespan)

API_KEY_NAME = "X-App-Api-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == APP_API_KEY:
        return api_key
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key"
    )

@app.post("/api/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    api_key: str = Depends(get_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    OpenAI-compatible chat completions endpoint that proxies to a vLLM/Ollama engine.
    """
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages list cannot be empty")

    # Use the model from request if provided, otherwise use default
    model = request.model if request.model != "stub-model" else MODEL_NAME

    # Handle session persistence for the user message
    if request.session_id:
        result = await db.execute(select(Session).where(Session.id == request.session_id))
        session = result.scalar_one_or_none()
        if session:
            # Save the last user message
            user_msg = request.messages[-1]
            db.add(Message(session_id=session.id, role=user_msg.role, content=user_msg.content))
            await db.commit()

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
        full_response_content = ""
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
                            if line.startswith("data: ") and not line.endswith("[DONE]"):
                                try:
                                    data = json.loads(line[6:])
                                    if "choices" in data and len(data["choices"]) > 0:
                                        delta = data["choices"][0].get("delta", {})
                                        if "content" in delta:
                                            full_response_content += delta["content"]
                                except json.JSONDecodeError:
                                    logging.warning(f"Failed to decode JSON from stream line: {line}")
                                except Exception as e:
                                    logging.error(f"Unexpected error parsing stream line: {e}")

            # Save assistant message to session if session_id is provided
            if request.session_id and full_response_content:
                # We need a new session to avoid issues with the closed stream
                async with async_session() as db_session:
                    db_session.add(Message(session_id=request.session_id, role="assistant", content=full_response_content))
                    await db_session.commit()

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

            data = response.json()
            # Save assistant message to session
            if request.session_id:
                content = data["choices"][0]["message"]["content"]
                db.add(Message(session_id=request.session_id, role="assistant", content=content))
                await db.commit()

            return data

@app.post("/api/sessions", response_model=SessionResponse)
async def create_session(api_key: str = Depends(get_api_key), db: AsyncSession = Depends(get_db)):
    new_session = Session()
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    # Re-fetch with messages (though empty) to match schema
    result = await db.execute(
        select(Session).where(Session.id == new_session.id).options(selectinload(Session.messages))
    )
    return result.scalar_one()

@app.get("/api/sessions", response_model=List[SessionResponse])
async def list_sessions(api_key: str = Depends(get_api_key), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Session).options(selectinload(Session.messages)))
    return result.scalars().all()

@app.get("/api/sessions/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str, api_key: str = Depends(get_api_key), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Session).where(Session.id == session_id).options(selectinload(Session.messages))
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

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
