# ROADMAP

This roadmap outlines the implementation plan for the AI web chatbot based on the private vLLM engine, as defined in `CONCEPT.md` and `DESIGN.md`.

## Progress Overview

| Phase | Description | Status |
| :--- | :--- | :---: |
| 1 | Project Foundation & CI/CD Setup | ✅ |
| 2 | MVP - Backend Orchestrator | 🚧 |
| 3 | MVP - Frontend UI | 🚧 |
| 4 | Integration & MVP Validation | ⏳ |
| 5 | Advanced Features & Documentation | ⏳ |
| 6 | Enterprise Caching & Optimization | ⏳ |

## Goals
- 🚧 Build a functional private AI web chatbot (MVP).
- ⏳ Ensure data privacy by hosting on private infrastructure.
- ⏳ Optimize for high-throughput using vLLM.
- ⏳ Maintain 100% testability across all layers.
- ⏳ Optimize TTFT and costs with Automatic Prefix Caching (APC).

---

## Phase 1: Project Foundation & CI/CD Setup ✅
- [x] Initialize project structure (directories and placeholders) (2025-01-24)
- [x] Create `TOP_ARCHITECTURE.puml` (2025-01-24)
- [x] Create `src/install.sh` for development environment setup (2025-05-22)
- [x] Create `test/install.sh` for testing tools setup (2025-05-22)
- [x] Configure GitHub Action Workflow for CI/CD (2025-05-22)
    - [x] Implement basic linting and structure verification
    - [ ] Setup caching for dependencies
- [x] Verify CI/CD pipeline with a baseline validation script (2025-05-22)

## Phase 2: MVP - Backend Orchestrator 🚧
- [x] Define API interfaces and Pydantic models (2025-05-22)
- [x] Implement basic FastAPI server in `src/backend` (2025-05-22)
- [x] Implement OpenAI-compatible client for vLLM communication (2025-05-22)
- [x] Implement configuration for switching between local Ollama and remote vLLM (2025-05-22)
- [x] Implement stubbed SSE (Server-Sent Events) endpoint for streaming responses (2025-05-22)
- [x] Create unit tests for backend logic in `test/backend` (2025-05-22)
- [x] Implement integration tests for vLLM proxying (using mocks) (2025-05-22)
- [x] **Verification**: Ensure `pytest` runs successfully in CI/CD (2025-05-22)

## Phase 3: MVP - Frontend UI 🚧
- [x] Initialize React project structure in `src/frontend` (2025-05-22)
- [ ] Create responsive chat interface component
- [x] Implement SSE client skeleton for real-time message rendering (2025-05-22)
- [ ] Setup UI automation tests (e.g., Playwright)
    - [ ] Configure screenshot capture for each test step
- [ ] **Verification**: UI tests run in CI/CD and store screenshots as assets

## Phase 4: Integration & MVP Validation ⏳
- [ ] Connect Frontend UI to Backend Orchestrator
- [ ] Perform End-to-End (E2E) testing of the full flow (UI -> Backend -> vLLM Mock)
- [ ] Verify local development flow with Ollama
- [ ] Deploy MVP to a test instance on vast.ai
- [ ] **Verification**: Successful manual and automated validation of the MVP flow

## Phase 5: Advanced Features & Documentation ⏳
- [ ] Implement Session Management and basic Authentication
- [ ] Integrate RAG (Retrieval-Augmented Generation) support
- [ ] Configure ReadTheDocs (RTD) for automated documentation publishing
- [ ] Perform performance and throughput testing
- [ ] Final review and logging of technical debts in `TECHNICAL_DEBTS.md`

## Phase 6: Enterprise Caching & Optimization ⏳
- [ ] Enable vLLM Automatic Prefix Caching (APC)
    - [ ] Update vLLM startup scripts to include `--enable-prefix-caching`
    - [ ] Configure `gpu_memory_utilization` to accommodate cache blocks
- [ ] Implement Sticky Session Routing in Backend Orchestrator
    - [ ] Add session-based routing middleware to FastAPI
    - [ ] Verify session persistence across multi-replica deployments
- [ ] Validate Caching Performance
    - [ ] Benchmarking TTFT for multi-turn conversations (Cache Hit vs. Miss)
    - [ ] Monitor VRAM utilization and eviction patterns
- [ ] **Verification**: Documented TTFT reduction and cache hit rates in performance reports
