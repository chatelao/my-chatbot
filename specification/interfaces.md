# Technical Interfaces Specification

This document defines the communication protocols and data formats between the components of the AI web chatbot.

## 1. UI ↔ Backend Orchestrator

The Frontend UI communicates with the Backend Orchestrator via a RESTful API with support for real-time streaming.

### 1.1 Chat Completion Endpoint

- **Endpoint**: `POST /api/chat/completions`
- **Description**: Submits a list of messages and receives a generated response.
- **Content-Type**: `application/json`

#### Request Body
```json
{
  "messages": [
    {
      "role": "system",
      "content": "string (optional)"
    },
    {
      "role": "user",
      "content": "string"
    },
    {
      "role": "assistant",
      "content": "string"
    }
  ],
  "stream": true,
  "session_id": "string (optional)"
}
```

#### Response (Non-Streaming)
- **Status Code**: `200 OK`
- **Content-Type**: `application/json`

```json
{
  "id": "string",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "string"
      },
      "finish_reason": "stop"
    }
  ]
}
```

#### Response (Streaming)
- **Status Code**: `200 OK`
- **Content-Type**: `text/event-stream`
- **Mechanism**: Server-Sent Events (SSE)

Each event data chunk follows the OpenAI-compatible stream format:
```text
data: {"id": "...", "choices": [{"delta": {"content": "word"}, "finish_reason": null}]}

data: {"id": "...", "choices": [{"delta": {}, "finish_reason": "stop"}]}

data: [DONE]
```

## 2. Backend Orchestrator ↔ Inference Engine (vLLM)

The Backend Orchestrator proxies requests to the vLLM engine, which exposes an OpenAI-compatible API.

- **Base URL**: `http://<vllm-host>:<port>/v1`
- **Endpoint**: `POST /v1/chat/completions`
- **Authentication**: Bearer Token (if configured)

### 2.1 Request Mapping
The Backend Orchestrator maps the UI request to the vLLM request, adding necessary engine-specific parameters.

```json
{
  "model": "the-deployed-model-name",
  "messages": [...],
  "stream": true,
  "temperature": 0.7,
  "max_tokens": 1024
}
```

### 2.2 Response Handling
The Backend Orchestrator streams the response from vLLM directly back to the UI, potentially performing minor transformations or logging for session management.

## 3. Session Management & Sticky Routing

- **Session Identification**: Provided via `session_id` in the request or a session cookie.
- **Sticky Routing**: The Backend Orchestrator uses the `session_id` to route requests to the same vLLM instance to maximize the hit rate of the Automatic Prefix Caching (APC).
