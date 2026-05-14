# Configuration

The Backend Orchestrator can be configured using environment variables. Create a `.env` file in the root directory (or set them in your environment) to customize the behavior.

## Inference Engine Configuration

- `INFERENCE_API_BASE`: The base URL of the OpenAI-compatible inference engine.
    - **Local Ollama**: `http://localhost:11434/v1` (Default for development)
    - **Remote vLLM**: `http://<vast-ai-ip>:8000/v1` (Production)
- `INFERENCE_API_KEY`: The API key for the inference engine.
    - **Local Ollama**: Not required (can be anything or left empty).
    - **Remote vLLM**: Depends on the vLLM configuration.
- `MODEL_NAME`: The name of the model to use.
    - **Local Ollama**: e.g., `llama3`, `mistral`, etc.
    - **Remote vLLM**: The name of the model loaded into vLLM.

## Example `.env` for Local Development (Ollama)

```env
INFERENCE_API_BASE=http://localhost:11434/v1
INFERENCE_API_KEY=ollama
MODEL_NAME=llama3
```

## Example `.env` for Production (vLLM)

```env
INFERENCE_API_BASE=https://api.example.com/v1
INFERENCE_API_KEY=your-secure-api-key
MODEL_NAME=meta-llama/Llama-3-8b-instruct
```
