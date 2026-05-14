import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .schemas import ChatCompletionRequest

app = FastAPI(title="AI Web Chatbot Backend")

@app.post("/api/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    OpenAI-compatible chat completions endpoint that returns an SSE stream.
    """
    async def event_generator():
        # Stub implementation of SSE streaming
        mock_tokens = ["Hello", "!", " This", " is", " a", " stubbed", " response", " from", " the", " backend", "."]

        for token in mock_tokens:
            # Match OpenAI SSE format
            chunk = {
                "id": "chatcmpl-mock",
                "object": "chat.completion.chunk",
                "created": 123456789,
                "model": request.model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": token},
                        "finish_reason": None
                    }
                ]
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.1)

        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
