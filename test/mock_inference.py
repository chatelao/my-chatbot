import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/v1/chat/completions")
async def chat_completions():
    async def event_generator():
        yield 'data: {"choices": [{"delta": {"content": "This is a mocked response from the inference engine."}}]}\n\n'
        yield 'data: [DONE]\n\n'

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=11434)
