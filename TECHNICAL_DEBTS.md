# Technical Debts

This document logs technical debts and areas for improvement identified during development.

## Phase 2: MVP - Backend Orchestrator
- [x] **Authentication**: Basic API Key authentication has been implemented.
    - *Debt*: The API key is currently hardcoded in the frontend (`ChatInterface.jsx`) for the MVP. This must be refactored to use a secure session-based or environment-driven approach in Phase 5.
    - *Debt*: A more robust solution (e.g., JWT, OAuth2) should be considered for enterprise use.
- [ ] **Session Management**: No server-side session management. Conversation history is currently managed by the frontend only.
- [ ] **Error Handling**: Basic error handling is in place, but more robust handling of edge cases in SSE streaming is needed.

## Phase 3: MVP - Frontend UI
- [ ] **Tailwind CSS Integration**: Currently using custom CSS in `ChatInterface.css` because of difficulties with Tailwind's dynamic building in the sandbox environment. This should be refactored to use standard Tailwind classes once the build pipeline is fully optimized.
- [ ] **Markdown Styling**: `react-markdown` is used but default styling is minimal. Integration with `@tailwindcss/typography` is recommended.

## Phase 4: Integration & MVP Validation
- [ ] **Backend static serving**: The backend currently serves the `frontend/build` directory. This is suitable for MVP but a dedicated static file server (e.g., Nginx) should be used in production.
