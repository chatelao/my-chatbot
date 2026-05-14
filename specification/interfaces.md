# Technical Interfaces

This document specifies the communication interfaces between the major components of the AI web chatbot.

## UI ↔ Backend

- **Method**: POST
- **Endpoint**: `/api/chat/completions`
- **Request Body**: JSON
    ```json
    {
      "model": "string",
      "messages": [
        {
          "role": "user",
          "content": "string"
        }
      ],
      "stream": true
    }
    ```
- **Response**: `text/event-stream` (SSE)
- **Streaming Format**: Server-Sent Events delivering individual tokens.

## Backend ↔ Inference

The Backend Orchestrator communicates with the Inference Engine using an OpenAI-compatible API.

- **Method**: POST
- **Endpoint**: `/v1/chat/completions`
- **Protocol**: HTTP/HTTPS
- **Configuration**:
    - `INFERENCE_API_BASE`: The base URL of the inference engine (e.g., `http://localhost:11434/v1` for Ollama or `http://vast-ai-ip:8000/v1` for vLLM).
    - `INFERENCE_API_KEY`: API key if required (typically not for local Ollama, but may be for remote vLLM).

### Supported Engines

1. **vLLM (Production)**
   - Optimized for high throughput and multiple users.
   - Hosted on `vast.ai`.

2. **Ollama (Development)**
   - Optimized for ease of use and local development.
   - Hosted on the developer's local machine.
