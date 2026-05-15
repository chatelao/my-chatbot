# My Chatbot Roadmap

This roadmap outlines the implementation plan for the AI web chatbot based on the private vLLM engine, as defined in `CONCEPT.md` and `DESIGN.md`.

## Progress Overview

| Phase | Description | Status |
| :--- | :--- | :---: |
| 1 | Project Foundation & CI/CD Setup | ✅ |
| 2 | MVP - Backend Orchestrator | ✅ |
| 3 | MVP - Frontend UI | ✅ |
| 4 | Integration & MVP Validation | 🚧 |
| 5 | Advanced Features & Documentation | ⏳ |
| 6 | Enterprise Caching & Optimization | ⏳ |

## Goals

* ✅ Build a functional private AI web chatbot (MVP).
* ⏳ Ensure data privacy by hosting on private infrastructure.
* ⏳ Optimize for high-throughput using vLLM.
* ⏳ Maintain 100% testability across all layers.
* ⏳ Optimize TTFT and costs with Automatic Prefix Caching (APC).

---

## Phase 1: Project Foundation & CI/CD Setup

This phase focuses on establishing the core project structure, development environment, and the automated CI/CD pipeline to ensure consistent quality from the start.

* ✅ Initialize project structure (directories and placeholders) (2025-01-24)
* ✅ Create `TOP_ARCHITECTURE.puml` (2025-01-24)
* ✅ Create `src/install.sh` for development environment setup (2025-05-22)
* ✅ Create `test/install.sh` for testing tools setup (2025-05-22)
* ✅ Configure GitHub Action Workflow for CI/CD (2025-05-22)
    + ✅ Implement basic linting and structure verification
    + ⏳ Setup caching for dependencies
* ✅ Verify CI/CD pipeline with a baseline validation script (2025-05-22)

## Phase 2: MVP - Backend Orchestrator

This phase involves building the core backend service using FastAPI, including the interface for the inference engines and the streaming response mechanism.

* ✅ Define API interfaces and Pydantic models (2025-05-22)
* ✅ Implement basic FastAPI server in `src/backend` (2025-05-22)
* ✅ Implement OpenAI-compatible client for vLLM communication (2025-05-22)
* ✅ Implement configuration for switching between local Ollama and remote vLLM (2025-05-22)
* ✅ Implement stubbed SSE (Server-Sent Events) endpoint for streaming responses (2025-05-22)
* ✅ Create unit tests for backend logic in `test/backend` (2025-05-22)
* ✅ Implement integration tests for vLLM proxying (using mocks) (2025-05-22)
* ✅ **Verification**: Ensure `pytest` runs successfully in CI/CD (2025-05-22)

## Phase 3: MVP - Frontend UI

This phase focuses on creating the user-facing chat interface using React and Tailwind CSS, and connecting it to the backend streaming endpoint.

* ✅ Initialize React project structure in `src/frontend` (2025-05-22)
* ✅ Create responsive chat interface component (2025-05-22)
* ✅ Implement SSE client skeleton for real-time message rendering (2025-05-22)
* ✅ Setup UI automation tests (e.g., Playwright) (2025-05-22)
    + ✅ Configure screenshot capture for each test step (2025-05-22)
* ✅ **Verification**: UI tests run in CI/CD and store screenshots as assets (2025-05-22)

## Phase 4: Integration & MVP Validation

This phase integrates the frontend and backend components and validates the end-to-end flow using both mocks and real local inference.

* ✅ Connect Frontend UI to Backend Orchestrator (2025-05-22)
* ✅ Perform End-to-End (E2E) testing of the full flow (UI -> Backend -> vLLM Mock) (2025-05-22)
* ✅ Verify local development flow with Ollama (2026-05-15)
* ⏳ Deploy MVP to a test instance on vast.ai
* ⏳ **Verification**: Successful manual and automated validation of the MVP flow

## Phase 5: Advanced Features & Documentation

This phase adds essential enterprise features like session management and RAG support, while also formalizing the project documentation.

* ⏳ Implement Session Management and basic Authentication
    + ✅ Implement basic API Key Authentication (2026-05-15)
    + ⏳ Implement server-side session storage
* ⏳ Integrate RAG (Retrieval-Augmented Generation) support
    + ⏳ Define retrieval strategy and data schema
    + ⏳ Implement data ingestion and indexing pipeline
    + ⏳ Implement context-aware retrieval logic for prompts
* ⏳ Configure ReadTheDocs (RTD) for automated documentation publishing
* ⏳ Perform performance and throughput testing
* ⏳ Final review and logging of technical debts in `TECHNICAL_DEBTS.md`

## Phase 6: Enterprise Caching & Optimization

This phase optimizes the system for high-throughput production use by enabling advanced caching and routing strategies.

* ⏳ Enable vLLM Automatic Prefix Caching (APC)
    + ⏳ Update vLLM startup scripts to include `--enable-prefix-caching`
    + ⏳ Configure `gpu_memory_utilization` to accommodate cache blocks
* ⏳ Implement Sticky Session Routing in Backend Orchestrator
    + ⏳ Add session-based routing middleware to FastAPI
    + ⏳ Verify session persistence across multi-replica deployments
* ⏳ Validate Caching Performance
    + ⏳ Benchmarking TTFT for multi-turn conversations (Cache Hit vs. Miss)
    + ⏳ Monitor VRAM utilization and eviction patterns
* ⏳ **Verification**: Documented TTFT reduction and cache hit rates in performance reports
