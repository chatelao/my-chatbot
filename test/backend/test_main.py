import json
import pytest
import httpx
from fastapi.testclient import TestClient
from src.backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "config" in response.json()

@pytest.mark.asyncio
async def test_chat_completions_streaming(respx_mock):
    # Mock the inference engine
    inference_url = "http://localhost:11434/v1/chat/completions"

    mock_response_content = (
        'data: {"choices": [{"delta": {"content": "Hello"}}]}\n\n'
        'data: {"choices": [{"delta": {"content": " world"}}]}\n\n'
        'data: [DONE]\n\n'
    )

    respx_mock.post(inference_url).return_value = httpx.Response(
        200,
        content=mock_response_content,
        headers={"Content-Type": "text/event-stream"}
    )

    payload = {
        "model": "stub-model",
        "messages": [{"role": "user", "content": "Hi"}],
        "stream": True
    }

    # Since we are using TestClient which is synchronous, we use it directly
    # But for streaming we might need something else or just check it works as expected
    headers = {"X-App-Api-Key": "dev-key"}
    with client.stream("POST", "/api/chat/completions", json=payload, headers=headers) as response:
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]

        lines = [line for line in response.iter_lines() if line]
        assert len(lines) == 3
        assert "Hello" in lines[0]
        assert "world" in lines[1]
        assert "[DONE]" in lines[2]

@pytest.mark.asyncio
async def test_chat_completions_non_streaming(respx_mock):
    # Mock the inference engine
    inference_url = "http://localhost:11434/v1/chat/completions"

    mock_response_json = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "llama3",
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "Hello there!"
            },
            "finish_reason": "stop",
            "index": 0
        }]
    }

    respx_mock.post(inference_url).return_value = httpx.Response(
        200,
        json=mock_response_json
    )

    payload = {
        "model": "stub-model",
        "messages": [{"role": "user", "content": "Hi"}],
        "stream": False
    }

    headers = {"X-App-Api-Key": "dev-key"}
    response = client.post("/api/chat/completions", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["choices"][0]["message"]["content"] == "Hello there!"

def test_chat_completions_unauthorized():
    payload = {
        "model": "stub-model",
        "messages": [{"role": "user", "content": "Hi"}],
        "stream": False
    }
    # No API Key
    response = client.post("/api/chat/completions", json=payload)
    assert response.status_code == 401

    # Invalid API Key
    headers = {"X-App-Api-Key": "wrong-key"}
    response = client.post("/api/chat/completions", json=payload, headers=headers)
    assert response.status_code == 401
