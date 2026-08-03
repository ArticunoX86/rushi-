# 3-Week Master Implementation Plan: Salesforce Real Estate AI Calling Platform

This plan outlines the roadmap to complete the entire platform from its current state (**~75% completion**) to **100% production readiness** within a **3-week timeframe**.

---

## 📅 3-Week Timeline Overview

```
[ Week 1: WebRTC Engine & In-Call Audio ]  ──►  [ Week 2: Salesforce CRM & Appointments ]  ──►  [ Week 3: Health, Analytics & Deployment ]
```

---

## 🛠️ Week 1: WebRTC Engine & In-Call Audio Upgrade
**Goal**: Replace raw WebSocket audio streaming with a WebRTC stream (`MODE_IN_COMMUNICATION`) for sub-200ms latency, automatic in-call audio routing, and echo cancellation.

### 1. Backend Components (`backend/`)
* **[NEW] [webrtc_agent.py](file:///C:/Internship/Backup/salesforce-ai-calling-agent/backend/app/services/webrtc_agent.py)**
  * Implement Python LiveKit agent worker with Deepgram STT, Gemini 2.5 Flash LLM, and ElevenLabs TTS plugins.
* **[NEW] [livekit_service.py](file:///C:/Internship/Backup/salesforce-ai-calling-agent/backend/app/services/livekit_service.py)**
  * Generate secure JWT WebRTC room tokens for client sessions.
* **[NEW] [webrtc.py](file:///C:/Internship/Backup/salesforce-ai-calling-agent/backend/app/api/webrtc.py)**
  * Expose `POST /webrtc/token` endpoint to provide WebRTC tokens for active call IDs.

### 2. Mobile App Components (`ai_voice_calling/`)
* **[MODIFY] [pubspec.yaml](file:///C:/Internship/Backup/salesforce-ai-calling-agent/ai_voice_calling/pubspec.yaml)**
  * Add `livekit_client: ^2.2.0` dependency.
* **[NEW] [webrtc_voice_service.dart](file:///C:/Internship/Backup/salesforce-ai-calling-agent/ai_voice_calling/lib/services/webrtc_voice_service.dart)**
  * Bridge `livekit_client` room connection, microphone publishing, and remote track subscription.
* **[MODIFY] [RealTimeAudioService.kt](file:///C:/Internship/Backup/salesforce-ai-calling-agent/ai_voice_calling/android/app/src/main/kotlin/com/aivoicecalling/ai_voice_calling/RealTimeAudioService.kt)**
  * Set `AudioManager` to `MODE_IN_COMMUNICATION` so audio feeds directly into the active in-call voice stream.

---

## 🔌 Week 2: Salesforce CRM Integration & Appointments System
**Goal**: Bi-directional sync with Salesforce CRM and live site visit appointment booking during calls.

### 1. Salesforce CRM Integration (`backend/app/integrations/salesforce/`)
* **[NEW] [client.py](file:///C:/Internship/Backup/salesforce-ai-calling-agent/backend/app/integrations/salesforce/client.py)**
  * Implement Salesforce OAuth2 authentication (Client Credentials / Refresh Token flow).
* **[NEW] [salesforce_service.py](file:///C:/Internship/Backup/salesforce-ai-calling-agent/backend/app/services/salesforce_service.py)**
  * Pull leads from Salesforce (`Lead` object) into local PostgreSQL database.
  * Push completed call logs, transcripts, call outcome, and recordings back into Salesforce `Task` / `CallLog` custom objects.

### 2. Appointments System
* **[NEW] [appointments.py](file:///C:/Internship/Backup/salesforce-ai-calling-agent/backend/app/api/appointments.py)**
  * Implement REST API endpoints for property site visit booking (`POST /appointments`, `GET /appointments`).
* **[NEW] [appointment_service.py](file:///C:/Internship/Backup/salesforce-ai-calling-agent/backend/app/services/appointment_service.py)**
  * Calendar slot availability check, site visit scheduling, and linking appointments to leads and properties.

---

## 🚀 Week 3: System Hardening, Analytics & Production Deployment
**Goal**: Health monitoring, automated follow-up scheduler, analytics dashboard, and cloud deployment.

### 1. System Hardening & Follow-up Scheduler
* **[NEW] [health.py](file:///C:/Internship/Backup/salesforce-ai-calling-agent/backend/app/api/health.py)**
  * Implement `/health` route returning operational status for DB, S3, Deepgram, ElevenLabs, and Salesforce APIs.
* **[NEW] [scheduler_service.py](file:///C:/Internship/Backup/salesforce-ai-calling-agent/backend/app/services/scheduler_service.py)**
  * Background cron task to automatically re-dispatch calls for leads marked for follow-up.

### 2. Analytics Dashboard & App UI
* **[MODIFY] [dashboard_screen.dart](file:///C:/Internship/Backup/salesforce-ai-calling-agent/ai_voice_calling/lib/features/dashboard/presentation/dashboard_screen.dart)**
  * Display real-time call conversion rate, total call duration, call outcome breakdown, and active connected devices.

### 3. Production Deployment Guide
* **[NEW] [Dockerfile](file:///C:/Internship/Backup/salesforce-ai-calling-agent/backend/Dockerfile)** & **[docker-compose.yml](file:///C:/Internship/Backup/salesforce-ai-calling-agent/backend/docker-compose.yml)**
  * Containerize Python FastAPI backend, PostgreSQL, and LiveKit server for production deployment on AWS EC2 / App Runner.

---

## 🧪 Verification Plan

### Weekly Milestones:
* **End of Week 1**: Verify WebRTC sub-200ms audio streaming directly into cellular phone calls without speaker noise.
* **End of Week 2**: Verify lead pulling from Salesforce and live appointment creation during AI calls.
* **End of Week 3**: Verify `/health` API, automated follow-up dispatch, dashboard analytics, and full system deployment.
