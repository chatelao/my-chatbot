# Detailed Architecture

![Top Level Architecture](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/chatelao/my-chatbot/main/TOP_ARCHITECTURE.puml)

The system is structured into three distinct layers, each with specific technical responsibilities and interfaces.

1. **User Interface (UI) Layer**:
   - Built as a Single Page Application (SPA).
   - Manages local state for chat history and active streaming.
   - Renders Markdown content in real-time.

2. **Backend Orchestrator Layer**:
   - Acts as a stateless proxy and orchestrator.
   - Handles authentication and session validation.
   - Formats requests for the vLLM engine and manages the streaming response back to the UI.

3. **Inference Engine Layer**:
   - **Production**: vLLM instance running on specialized GPU hardware (e.g., vast.ai).
   - **Local Development**: Ollama instance running on the developer's local machine.
   - Both expose an OpenAI-compatible API to the Backend Orchestrator.

# Technical Interfaces
- **UI ↔ Backend**:
  - **Method**: POST for sending prompts.
  - **Streaming**: Server-Sent Events (SSE) for real-time token delivery.
  - **Format**: JSON for requests, `text/event-stream` for responses.
- **Backend ↔ Inference**:
  - **Method**: POST.
  - **Protocol**: HTTP/HTTPS.
  - **Format**: OpenAI-compatible Chat Completion JSON.
  - **Configuration**: The Backend Orchestrator uses environment variables (e.g., `INFERENCE_API_BASE` and `INFERENCE_API_KEY`) to toggle between the local Ollama endpoint and the production vLLM endpoint.

# Technology Stack

| Layer | Component | Choice | Rationale |
|-------|-----------|--------|-----------|
| **Frontend** | Framework | React | Large ecosystem, excellent state management for complex UIs. |
| | Styling | Tailwind CSS | Rapid development, consistent design system, highly responsive. |
| **Backend** | Framework | FastAPI | High performance, native async support, automatic API documentation. |
| | Language | Python | Industry standard for AI/ML integration and backend orchestration. |
| **Inference** | Engine | vLLM | High-throughput serving with PagedAttention optimization. |
| **Caching** | Strategy | APC | Automatic Prefix Caching for TTFT and cost reduction. |
| **Hosting** | Infrastructure | vast.ai | Market-leading cost efficiency for GPU spot instances. |
| **Documentation**| Publishing | ReadTheDocs | Automated CI/CD integration for documentation consistency. |

# Enterprise Caching Architecture & Surgical Assessment

| Architectural Vector | Implementation Mechanics (FastAPI + vLLM) | Surgical Assessment & Red Teaming Risks (DA / RT / GR) |
| :--- | :--- | :--- |
| **Engine-Level Activation (Single Node)** | Pass `--enable-prefix-caching` to the vllm serve CLI or set `enable_prefix_caching=True` inside `AsyncEngineArgs` when instantiating your `AsyncLLMEngine` within FastAPI lifecycle events. | **Gordon Ramsay**: Free efficiency is a myth. vLLM’s caching works at the KV-block level by calculating block hashes. If your server is slammed with massive, dynamic inputs that share zero overlap, the CPU overhead of block hashing will drag down baseline prefill speeds.<br><br>**Red Teaming**: Persistent cache blocks consume physical VRAM. If your `--gpu-memory-utilization` is aggressively allocated and you fail to tune block eviction parameters, dead chat sessions will permanently anchor memory blocks, starving the engine of available blocks for active decode phases and triggering silent runtime OOM stalls. |
| **Distributed Routing (Multi-Replica Scaling)** | Implement a custom routing layer or sticky-session middleware at the FastAPI ingress gateway that pins specific user session IDs (or hashes of fixed system prompts) to identical downstream vLLM worker nodes. | **Devil's Advocate**: Stateless REST backends are highly robust, but persistent caching demands stateful spatial awareness.<br><br>**Red Teaming**: Naive round-robin load balancing destroys prefix caching completely. If user Turn 1 executes on Pod A, and FastAPI routes Turn 2 to Pod B, Pod B encounters a complete cache miss. You end up burning parallel compute recalculating identical KV blocks across segregated GPU nodes, eliminating the precise financial efficiency you sought to build. |

# Implementation Choices

## 1. Frontend Framework
- **Alternative A: React (Preferred)**: React provides a robust component-based architecture and a vast ecosystem of libraries (like `react-markdown` and `framer-motion`) that are essential for building a polished chat experience. Its Hook system allows for clean management of the complex state involved in streaming data.
- **Alternative B: Vue.js**: An excellent, lightweight framework. However, the ecosystem for specialized AI chat components is slightly more fragmented compared to React.
- **Alternative C: Next.js**: Offers Server-Side Rendering (SSR) and built-in routing. While powerful, it introduces unnecessary complexity for a private, authenticated application where most interactions happen client-side after the initial load.

## 2. Backend Framework
- **Alternative A: FastAPI (Preferred)**: FastAPI is built on Starlette (for web parts) and Pydantic (for data parts), making it one of the fastest Python frameworks available. Its native support for `async` and `await` is critical for handling long-lived connections during LLM streaming without blocking other requests.
- **Alternative B: Express.js (Node.js)**: A very popular choice with great async support. However, using Python for the backend allows for easier integration with other AI tools and better alignment with the data science ecosystem if RAG or local processing is added later.
- **Alternative C: Flask**: A reliable and simple framework, but it is fundamentally synchronous. While it can be made to work with async, it is not as performant or modern as FastAPI for this specific use case.

## 3. Communication Protocol
- **Alternative A: Server-Sent Events (SSE) (Preferred)**: SSE is the ideal choice for AI chatbots. It provides a standard way to stream data from the server to the client over HTTP. It is simpler to implement than WebSockets, handles reconnections automatically, and is more firewall-friendly.
- **Alternative B: WebSockets**: Provides full-duplex communication. While powerful, it is overkill for a chatbot where the primary need is one-way streaming (Server to Client) after a single request. It also requires more complex server-side resource management.
- **Alternative C: REST Polling**: Involves the client repeatedly asking the server for updates. This is highly inefficient, leads to high latency, and creates a poor "stuttering" user experience.

## 4. Caching Implementation
- **Alternative A: Automatic Prefix Caching (APC) (Preferred)**: Leveraging vLLM's internal KV cache management. It is transparent to the application and highly optimized for token-level reuse.
- **Alternative B: Application-side Caching**: Implementing a cache at the FastAPI level to store full responses. While simpler, it lacks the granularity of prefix caching and doesn't help with multi-turn conversation prefixes.
- **Alternative C: Custom Middleware Routing**: Implementing sticky sessions to ensure requests from the same session always hit the same vLLM node. Essential for distributed setups to maintain high cache hit rates.

# Component Status

| Component | Status | Technical Detail |
|-----------|--------|------------------|
| **UI** | 🔴 Planned | React 18, Tailwind CSS, SSE Client implementation |
| **Backend** | 🔴 Planned | FastAPI, Python 3.10+, StreamingResponse integration, Multi-engine support, Sticky Session Routing |
| **Inference**| 🔴 Planned | vLLM (Production), Ollama (Development) |

# Summary of Discarded Alternatives
- **Frontend Framework**: Vue.js and Next.js were discarded in favor of React to leverage its superior ecosystem and state management capabilities for interactive chat UIs.
- **Backend Framework**: Express.js and Flask were discarded. FastAPI was selected for its superior performance and native async capabilities within the Python ecosystem.
- **Communication Protocol**: WebSockets and REST Polling were discarded in favor of SSE, which provides the most efficient and simplest mechanism for the required streaming functionality.
- **Caching Implementation**: Application-side Caching was discarded for lacking prefix-level granularity. Custom Middleware Routing is considered a complementary necessity for distributed scaling rather than a standalone alternative to APC.
