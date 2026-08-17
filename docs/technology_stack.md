# NexaVoice: Technology Stack & Usage Documentation

This document outlines the technologies, frameworks, and APIs utilized across the NexaVoice (Salesforce AI Calling Agent) platform and details how each component contributes to the overall architecture.

## 🏗️ Architecture Overview

The platform is designed as a highly responsive, real-time AI voice calling agent integrated directly with Salesforce. It comprises three primary layers:
1. **Backend Orchestrator (The Brain):** Manages real-time audio streams, AI integrations, CRM sync, and business logic.
2. **Frontend Web Dashboard:** A React-based interface for administrators to monitor calls, manage leads, and view analytics.
3. **Mobile Client (Flutter App):** Serves as the edge device connecting the cellular network to the AI engine via WebRTC.

---

## 🧠 Backend Stack (Python / FastAPI)
The backend is the core of the system, handling high-performance asynchronous operations, real-time audio routing, and API orchestrations.

- **FastAPI & Uvicorn:** Chosen for their high performance and asynchronous capabilities, they serve as the foundational web framework and ASGI server to handle concurrent REST API requests and WebSockets/WebRTC signaling.
- **SQLAlchemy & Alembic:** Serve as the ORM (Object Relational Mapper) and database migration tool. We use them to interact with our **PostgreSQL** database to store leads, call logs, tenants, and system configuration.
- **Pydantic:** Used extensively for data validation and settings management (via `pydantic-settings`), ensuring payloads between the frontend and backend remain strictly typed.
- **LiveKit (WebRTC Engine):** 
  - *Usage:* Replaced raw WebSockets for sub-200ms latency audio streaming.
  - *Libraries:* `livekit`, `livekit-agents`
  - *Role:* Streams in-call audio bi-directionally between the mobile device and the AI backend.
- **AI Integrations:**
  - **Deepgram (`deepgram-sdk`):** Provides ultra-fast Speech-to-Text (STT) transcription, turning customer speech into text in real-time.
  - **Google Gemini (`google-generativeai`):** Acts as the conversational "brain" (LLM). It processes the transcribed text, determines intent, extracts relevant data (like appointment times), and generates the next conversational response.
  - **ElevenLabs (`elevenlabs`):** A premium Text-to-Speech (TTS) engine that converts the LLM's text output into an ultra-realistic human voice.
- **Salesforce Integration (`simple-salesforce`):** Used to authenticate via OAuth2, pull down new `Lead` objects to be called, and push completed call logs, transcripts, and outcomes back into Salesforce as `Task` or `CallLog` objects.
- **Authentication & Security:** `python-jose`, `passlib`, and `bcrypt` are used to manage secure JWT tokens for user authentication and WebRTC room access.

---

## 🖥️ Frontend Web Dashboard (React / Vite)
The web portal provides a control center for managing the calling operations.

- **React 19 & Vite:** Provides a rapid, modern component-based UI layer built with Vite for incredibly fast HMR (Hot Module Replacement) and optimized production builds.
- **Tailwind CSS & Autoprefixer:** The core styling engine, allowing for a modern, responsive, and highly customizable UI without the overhead of heavy component libraries.
- **Framer Motion:** Used to add smooth micro-animations and dynamic transitions to the UI, enhancing the "premium" feel of the web application.
- **React Router DOM:** Manages client-side routing between different views (e.g., Leads, Calls, Devices, Dashboard).
- **Axios:** Handles HTTP requests from the client to the FastAPI backend.
- **Recharts:** Used for rendering analytical charts on the dashboard (e.g., call volumes, conversion rates).
- **Lucide React:** Provides a clean, modern icon set consistent with the platform's aesthetic.

---

## 📱 Mobile Client (Flutter / Dart)
The mobile application acts as a conduit between traditional cellular networks and our AI infrastructure.

- **Flutter & Dart:** A cross-platform framework used to build the client application, ensuring native performance.
- **Riverpod (`flutter_riverpod`):** Used for robust, compile-safe state management across the application.
- **LiveKit Client (`livekit_client`):** Connects to the backend WebRTC rooms to publish the device's microphone and subscribe to the AI's audio track.
- **Android Native Integration (`RealTimeAudioService.kt`):** Crucial for call routing. It sets the Android `AudioManager` to `MODE_IN_COMMUNICATION` to ensure audio is routed properly during active cellular phone calls, preventing echo and speakerphone bleeding.
- **Dio & Go Router:** Used for backend API communication and internal app navigation, respectively.

---

## ☁️ Infrastructure & Deployment
- **Docker & Docker Compose:** The backend, PostgreSQL database, and potentially the LiveKit server are containerized. `docker-compose.yml` ensures all services can be spun up simultaneously in isolated, reproducible environments.
- **AWS S3 (`boto3`):** Used for durable storage of compressed audio recordings (.mp3 files) generated after calls are completed.
