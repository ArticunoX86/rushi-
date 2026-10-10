# NexaVoice: System Running Manual

This manual provides comprehensive instructions on how to start all the components of the NexaVoice AI Calling Agent (Backend, Frontend, and Mobile Client).

---

## 1. Backend (FastAPI + PostgreSQL + LiveKit)
Location: `/backend`

The backend handles AI integrations, real-time audio signaling via WebRTC, and Salesforce syncing.

### Option A: Using Docker Compose (Recommended)
This is the easiest method and automatically provisions the PostgreSQL database.
**Prerequisites:** Docker Desktop must be running.

1. Open your terminal (PowerShell or Bash) and navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Start the services:
   ```bash
   docker-compose up -d --build
   ```
   This will start the backend on port `8000`, the database on port `5432`, and Nginx on port `80`/`443`.

### Option B: Local Development using WSL (Windows Subsystem for Linux)
If you do not want to use Docker, follow these steps to run the backend natively in Ubuntu/WSL.
**Prerequisites:** You must have PostgreSQL running locally and `.env` configured.

1. Open PowerShell and start an interactive WSL session by typing:
   ```bash
   wsl
   ```
2. Navigate to the backend directory:
   ```bash
   cd /mnt/c/Internship/Backup/salesforce-ai-calling-agent/backend
   ```
3. Install the virtual environment package (if you haven't already):
   ```bash
   sudo apt update
   sudo apt install python3.12-venv -y
   ```
4. Create and activate a fresh virtual environment:
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   ```
5. Install Python dependencies and run the server:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

---

## 2. Frontend Web Dashboard (React + Vite)
Location: `/frontend`

The web portal provides the UI for administrators to monitor calls, view analytics, and manage leads.

**Prerequisites:** Node.js installed.

1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install the necessary Node packages:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The dashboard will typically be available at `http://localhost:5173`. Ensure your `.env` points to your backend URL.

---

## 3. Mobile Client (Flutter)
Location: `/ai_voice_calling`

The Flutter mobile app connects the cellular network to the AI infrastructure via WebRTC.

**Prerequisites:** Flutter SDK installed and an Android/iOS emulator running, or a physical device connected via USB/Wi-Fi debugging.

1. Open a new terminal and navigate to the Flutter project:
   ```bash
   cd ai_voice_calling
   ```
2. Install Dart dependencies:
   ```bash
   flutter pub get
   ```
3. Run the application:
   ```bash
   flutter run
   ```
   *(Testing on a physical Android device is highly recommended to properly test the `RealTimeAudioService` telephony integrations).*

---

## 4. Default Login Credentials
Once the backend and frontend are running, you can access the admin dashboard on the web portal.

**Admin Dashboard:**
- **URL:** `http://localhost:5174` (or whichever port Vite uses)
- **Email:** `admin@example.com`
- **Password:** `admin123`
