# Technical Interface Specification

This document defines the interfaces between the major components of the AI web chatbot.

## 1. UI ↔ Backend Interface

The communication between the React Frontend and the FastAPI Backend is handled via HTTP POST requests for input and Server-Sent Events (SSE) for output.

### 1.1 Chat Completion Request
- **Endpoint**: `POST /api/chat/completions`
- **Content-Type**: `application/json`
- **Payload**:
  ```json
  {
    "messages": [
      {
        "role": "user",
        "content": "Hello, how can you help me today?"
      }
    ],
    "stream": true
  }
  ```

### 1.2 Chat Completion Response (Streaming)
- **Content-Type**: `text/event-stream`
- **Event Format**:
  - `data: {"id": "chatcmpl-...", "object": "chat.completion.chunk", "created": 123456789, "model": "...", "choices": [{"index": 0, "delta": {"content": "Hello"}, "finish_reason": null}]}`
  - `data: [DONE]` (Signifies the end of the stream)

## 2. Backend ↔ Inference Engine Interface

The Backend Orchestrator communicates with the vLLM engine using the OpenAI-compatible API.

### 2.1 Request to vLLM
- **Endpoint**: `POST /v1/chat/completions` (Standard OpenAI path)
- **Auth**: Bearer Token (if configured on vLLM/vast.ai)
- **Payload**: Follows the OpenAI Chat Completion API specification.

### 2.2 Response from vLLM
- **Format**: JSON or `text/event-stream` depending on the `stream` parameter in the request.

## 3. Session Management
- **Method**: HTTP-only Cookies or Authorization Headers.
- **Backend responsibility**: Validate session tokens before proxying requests to the Inference Engine.
