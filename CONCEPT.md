# Goal
Build an AI web chatbot based on a private vLLM engine.

# Business & Use Cases
- **Data Privacy and Intellectual Property Protection**: Ensure that sensitive company data used in prompts remains within a private, controlled environment, avoiding exposure to public AI service providers.
- **Cost-Efficient AI Operations**: Reduce operational costs by using specialized GPU spot instance providers like vast.ai instead of expensive managed API services.
- **Customizable Conversational Experience**: Enable the fine-tuning and deployment of specialized models tailored to specific business needs, such as internal knowledge base querying or technical support.
- **Operational Efficiency via Caching**: Implement Automatic Prefix Caching (APC) to drastically reduce Time-To-First-Token (TTFT) latency and minimize redundant GPU compute costs, especially for multi-turn conversations and RAG-heavy workloads.

# High-Level Architecture
The system consists of three main functional layers:

1. **User Interface (UI) Layer**:
   - Provides the conversational interface for the user.
   - Handles message rendering, state management, and user input.
   - **Business Interface**: Sends user prompts to the Backend Orchestrator and receives generated responses.

2. **Backend Orchestrator Layer**:
   - Manages user sessions and authentication.
   - Performs prompt engineering or retrieval-augmented generation (RAG) if necessary.
   - Routes requests to the Inference Engine.
   - **Business Interface**: Receives requests from the UI; communicates with the Inference Engine via standardized API protocols (e.g., OpenAI-compatible API).

3. **Inference Engine Layer**:
   - Hosts the Large Language Model using vLLM.
   - Manages GPU resources and optimized batching for high throughput.
   - **Business Interface**: Provides a high-performance endpoint for generating text based on input tokens.

# Technology Stack Overview
Inspired by the modular structure of the Renode RP2040 simulation project, the following high-level stack is proposed:

| Layer | Core Requirement | Preferred Solution |
|-------|------------------|--------------------|
| UI | Responsive Web Framework | Modern Frontend Framework |
| Backend | API Orchestration | Lightweight Backend Framework |
| Inference | High-throughput Engine | vLLM (Production), Ollama (Local Dev) |
| Caching | Performance Optimization | vLLM Automatic Prefix Caching (APC) |
| Hosting | Cost-effective GPU | vast.ai (Production), Local Machine (Local Dev) |
| Documentation | Automated Publishing | ReadTheDocs (RTD) |

# Component Capabilities
Following the status-tracking pattern from the Renode RP2040 project, the initial capabilities are defined:

| Component | Status | Capability |
|-----------|--------|------------|
| UI | 🔴 Planned | Chat interface, markdown support, mobile responsive |
| Backend | 🔴 Planned | Session management, API routing, RAG support, Sticky Session Routing |
| Inference | 🔴 Planned | vLLM integration, OpenAI API compatibility, Automatic Prefix Caching |

# Alternatives
## 1. Inference Engine
- **Alternative A: vLLM (Preferred for Production)**: High-throughput serving with PagedAttention. Best for performance and resource utilization in a production environment.
- **Alternative B: Text Generation Inference (TGI)**: Developed by Hugging Face, robust but has different licensing and performance characteristics.
- **Alternative C: Ollama (Preferred for Local Development)**: Extremely simple to set up and run on local hardware. While less optimized for high-throughput production serving than vLLM, it is ideal for rapid local prototyping and testing.

## 2. Hosting Platform
- **Alternative A: vast.ai (Preferred)**: Peer-to-peer GPU marketplace offering extremely competitive pricing for spot instances.
- **Alternative B: RunPod**: Reliable GPU cloud with both on-demand and spot instances, slightly higher cost than vast.ai.
- **Alternative C: Managed Cloud (AWS/GCP)**: High reliability and integrated services but significantly higher cost for GPU compute.

## 3. Documentation Publishing
- **Alternative A: ReadTheDocs (RTD) (Preferred)**: Standard for open-source documentation, automates builds from main branch.
- **Alternative B: GitHub Pages**: Integrated with GitHub, but requires more manual setup for complex documentation generators.
- **Alternative C: GitBook**: User-friendly UI, but may have limitations on the free tier for certain automation workflows.

## 4. Caching Strategy
- **Alternative A: Automatic Prefix Caching (APC) (Preferred)**: Native vLLM feature that caches KV blocks based on content hashes. Zero application-level logic required for basic functionality.
- **Alternative B: Manual KV Caching**: Managing cache state at the application layer. Offers precise control but introduces extreme complexity and potential for cache-consistency bugs.
- **Alternative C: No Caching**: Simplest to implement but leads to high latency and redundant compute costs in multi-turn or RAG scenarios.

# Summary of Discarded Alternatives
- **Inference Engine**: TGI was discarded. Ollama was discarded for production use in favor of vLLM due to vLLM's superior throughput and memory management (PagedAttention), but Ollama is retained as the primary choice for local development.
- **Hosting Platform**: RunPod and AWS/GCP were discarded in favor of vast.ai to minimize costs, leveraging the "Assume a running vLLM on vast.ai" requirement.
- **Documentation Publishing**: GitHub Pages and GitBook were discarded in favor of ReadTheDocs to ensure seamless "ReadTheDocs.org" integration as specified in `GEMINI.md`.
- **Caching Strategy**: Manual KV Caching and No Caching were discarded in favor of APC due to its seamless integration with vLLM and significant performance gains with minimal overhead.
