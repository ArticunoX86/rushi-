# Project Transfer & Setup Manual

This guide outlines the detailed, step-by-step process for transferring the NexaVoice AI Calling Agent to a completely new laptop and getting it up and running from scratch.

---

## Phase 1: Install System Prerequisites
Before moving any code, ensure the new laptop has the following core dependencies installed.

1. **Git**: To clone/manage the repository. 
   - Download: https://git-scm.com/
2. **Node.js (v18 or higher)**: Required for the React frontend.
   - Download: https://nodejs.org/
3. **Python (v3.10 or higher)**: Required for the FastAPI backend.
   - Download: https://www.python.org/downloads/
   - *Windows Note: Check "Add Python to PATH" during installation.*
4. **Docker Desktop**: Required to run the PostgreSQL database seamlessly with the `pgvector` extension.
   - Download: https://www.docker.com/products/docker-desktop/
5. **pgAdmin4**: A GUI tool to view and manage your PostgreSQL database.
   - Download: https://www.pgadmin.org/download/
6. **WSL2 (Windows Only)**: Required if you prefer running the backend in a Linux environment natively on Windows.
   - Open PowerShell as Administrator and run: `wsl --install`

---

## Phase 2: Transfer the Codebase
1. Either clone the repository via Git:
   ```bash
   git clone <your-repo-url>
   ```
2. Or transfer the entire project folder via a USB drive/ZIP file. 
   - *Note: If transferring via ZIP, delete the `node_modules` and `backend/venv` folders first to save space and prevent cross-platform compatibility issues.*

---

## Phase 3: Database & pgAdmin Setup (Docker)
We use Docker to instantly spin up a PostgreSQL instance pre-configured with the AI vector extension (`pgvector`).

1. Open **Docker Desktop** and ensure the Docker engine is running.
2. Open a terminal, navigate to the `backend` folder, and start the database:
   ```bash
   cd backend
   docker-compose up -d db
   ```
3. **Verify in pgAdmin4:**
   - Open **pgAdmin4**.
   - Right-click "Servers" > **Register** > **Server...**
   - **General Tab:** Name it `NexaVoice Local DB`.
   - **Connection Tab:**
     - Host name/address: `localhost`
     - Port: `5432`
     - Maintenance database: `nexa_voice` (or `postgres`)
     - Username: `postgres`
     - Password: `postgres`
   - Click **Save**. You should now see your database connected.

---

## Phase 4: Backend Setup & Seeding
Next, we must install the Python dependencies and create the database tables.

1. **Set up the Virtual Environment:**
   Navigate to the `backend` folder in your terminal and run:
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate it (Windows PowerShell)
   .\venv\Scripts\activate
   
   # Activate it (Mac/Linux/WSL)
   source venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   - Ensure the `.env` file exists inside the `backend` folder.
   - Critical Database setting inside `.env` must be:
     `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nexa_voice`
   - *Note: If running in WSL, ensure `HOST=0.0.0.0` is set in `.env` so Windows can reach it.*

4. **Run Migrations & Seed the Database:**
   This creates the tables and your default admin user.
   ```bash
   alembic upgrade head
   python seed_admin.py
   ```

5. **Start the Backend Server:**
   ```bash
   uvicorn app.main:app --reload
   # Or use your bash script: bash start_backend.sh
   ```
   *The backend is now live at `http://localhost:8000`.*

---

## Phase 5: Frontend Setup
1. Open a **new terminal window**, and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. **Install Node modules:**
   ```bash
   npm install
   ```
3. **Configure Environment Variables:**
   - Ensure the `.env` file exists in the `frontend` folder.
   - It should contain: `VITE_API_URL=http://localhost:8000` (Update to your WSL IP if using WSL, e.g., `http://172.20.113.228:8000`).
4. **Start the Frontend:**
   ```bash
   npm run dev
   ```
   *The frontend is now live at `http://localhost:5174` (or 5173).*

---

## Phase 6: Mobile App Setup (Flutter)
The AI Calling Agent uses a Flutter mobile app to act as the telephony gateway. All actual calling is performed on a physical mobile device.

1. **Prerequisites for Mobile Development:**
   - Install **Flutter SDK**: https://docs.flutter.dev/get-started/install
   - Install **Android Studio** (for Android SDK and USB Drivers): https://developer.android.com/studio
   - Ensure your physical Android device has **Developer Options** and **USB Debugging** enabled, and is connected to the laptop via USB.

2. **Configure the App connection to the Backend:**
   - Open a terminal and navigate to the mobile app folder:
     ```bash
     cd ai_voice_calling
     ```
   - Install Dart dependencies:
     ```bash
     flutter pub get
     ```
   - **CRITICAL STEP:** You must tell the mobile app how to connect to your backend!
     - Open the file: `ai_voice_calling/lib/core/config/app_config.dart`
     - Change `static const bool isProduction = true;` to `false` so it uses the local environment.
     - Change `static const String _localHost = "192.168.1.9";` to match your laptop's actual IPv4 Wi-Fi address (or WSL IP if using WSL without bridging). You can find this by running `ipconfig` (Windows) or `ifconfig` (Mac/Linux) in your terminal.

3. **Install and Run on Mobile:**
   - Check that your device is detected:
     ```bash
     flutter devices
     ```
   - Build and install the app onto your connected Android device:
     ```bash
     flutter run
     ```
   - The app will open on your phone. Make sure your phone and laptop are connected to the **same Wi-Fi network**.

---

## Phase 7: Final Verification
Go to your browser and open the frontend URL. Log in using the seeded credentials:

- **Email:** `admin@example.com`
- **Password:** `admin123`

Once logged in, verify that the dashboard loads. With the backend, frontend, and your physical mobile app all running and connected, the migration to the new laptop is fully complete!
