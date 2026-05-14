# ROADMAP

This roadmap outlines the implementation plan for the AI web chatbot based on the private vLLM engine, as defined in `CONCEPT.md` and `DESIGN.md`.

## Progress Overview

| Phase | Description | Status |
| :--- | :--- | :---: |
| 1 | Project Foundation & CI/CD Setup | ✅ |
| 2 | MVP - Backend Orchestrator | 🚧 |
| 3 | MVP - Frontend UI | ⏳ |
| 4 | Integration & MVP Validation | ⏳ |
| 5 | Advanced Features & Documentation | ⏳ |

## Goals
- 🚧 Build a functional private AI web chatbot (MVP).
- ⏳ Ensure data privacy by hosting on private infrastructure.
- ⏳ Optimize for high-throughput using vLLM.
- ⏳ Maintain 100% testability across all layers.

---

## Phase 1: Project Foundation & CI/CD Setup ✅
- [x] Initialize project structure (directories and placeholders) (2025-01-24)
- [x] Create `src/install.sh` for development environment setup (2026-05-14)
- [x] Create `test/install.sh` for testing tools setup (2026-05-14)
- [x] Configure GitHub Action Workflow for CI/CD (2026-05-14)
    - [x] Implement basic linting and structure verification (2026-05-14)
    - [ ] Setup caching for dependencies
- [x] Verify CI/CD pipeline with a baseline validation script (2026-05-14)
- [x] Define Technical Interfaces in `specification/interfaces.md` (2026-05-14)

## Phase 2: MVP - Backend Orchestrator 🚧
- [ ] Implement basic FastAPI server in `src/backend`
- [ ] Implement OpenAI-compatible client for vLLM communication
- [ ] Implement SSE (Server-Sent Events) endpoint for streaming responses
- [ ] Create unit tests for backend logic in `test/backend`
- [ ] Implement integration tests for vLLM proxying (using mocks)
- [ ] **Verification**: Ensure `pytest` runs successfully in CI/CD

## Phase 3: MVP - Frontend UI ⏳
- [ ] Initialize React project with Tailwind CSS in `src/frontend`
- [ ] Create responsive chat interface component
- [ ] Implement SSE client for real-time message rendering
- [ ] Setup UI automation tests (e.g., Playwright)
    - [ ] Configure screenshot capture for each test step
- [ ] **Verification**: UI tests run in CI/CD and store screenshots as assets

## Phase 4: Integration & MVP Validation ⏳
- [ ] Connect Frontend UI to Backend Orchestrator
- [ ] Perform End-to-End (E2E) testing of the full flow (UI -> Backend -> vLLM Mock)
- [ ] Deploy MVP to a test instance on vast.ai
- [ ] **Verification**: Successful manual and automated validation of the MVP flow

## Phase 5: Advanced Features & Documentation ⏳
- [ ] Implement Session Management and basic Authentication
- [ ] Integrate RAG (Retrieval-Augmented Generation) support
- [ ] Configure ReadTheDocs (RTD) for automated documentation publishing
- [ ] Perform performance and throughput testing
- [ ] Final review and logging of technical debts in `TECHNICAL_DEBTS.md`
