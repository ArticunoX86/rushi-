#!/bin/bash

# ==================================================
# Salesforce AI Calling Agent - Backend Startup Script
# ==================================================

set -e  # Exit immediately on any error

# -- Colors --
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# -- Helpers --
log_info()    { echo -e "${CYAN}[INFO]${RESET}  $1"; }
log_success() { echo -e "${GREEN}[OK]${RESET}    $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${RESET}  $1"; }
log_error()   { echo -e "${RED}[ERROR]${RESET} $1"; }

# -- Banner --
echo -e "${BOLD}${CYAN}"
echo "======================================================"
echo "   Salesforce AI Calling Agent -- Backend Server     "
echo "======================================================"
echo -e "${RESET}"

# -- Step 1: Navigate to backend directory --
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
log_info "Working directory: $(pwd)"

# -- Step 2: Check for .env file --
if [ ! -f ".env" ]; then
    log_error ".env file not found! Please create one from the template."
    exit 1
fi
log_success ".env file found."

# -- Step 3: Activate virtual environment --
VENV_ACTIVATE=""

if [ -f "venv/Scripts/activate" ]; then
    # Windows Git Bash / MSYS
    VENV_ACTIVATE="venv/Scripts/activate"
elif [ -f "venv/bin/activate" ]; then
    # Linux / macOS
    VENV_ACTIVATE="venv/bin/activate"
fi

if [ -z "$VENV_ACTIVATE" ]; then
    log_warn "Virtual environment not found at 'venv/'. Creating one..."
    python -m venv venv
    if [ -f "venv/Scripts/activate" ]; then
        VENV_ACTIVATE="venv/Scripts/activate"
    else
        VENV_ACTIVATE="venv/bin/activate"
    fi
fi

source "$VENV_ACTIVATE"
log_success "Virtual environment activated."

# -- Step 4: Install / sync dependencies --
if [ -f "requirements.txt" ]; then
    log_info "Installing dependencies from requirements.txt ..."
    pip install -r requirements.txt --quiet
    log_success "Dependencies installed."
else
    log_warn "requirements.txt not found -- skipping."
fi

# -- Step 5: Read HOST, PORT, DEBUG from .env --
HOST=$(grep -E '^HOST=' .env | cut -d '=' -f2 | tr -d '[:space:]')
PORT=$(grep -E '^PORT=' .env | cut -d '=' -f2 | tr -d '[:space:]')
DEBUG=$(grep -E '^DEBUG=' .env | cut -d '=' -f2 | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"

# -- Step 6: Hot-reload flag --
RELOAD_FLAG=""
if [ "$DEBUG" = "true" ]; then
    RELOAD_FLAG="--reload"
    log_info "Debug mode ON  -- hot reload ENABLED."
else
    log_info "Debug mode OFF -- running in production mode."
fi

# -- Step 7: Launch uvicorn --
echo ""
echo -e "${BOLD}${GREEN}Starting FastAPI backend ...${RESET}"
echo -e "  Base URL : http://${HOST}:${PORT}"
echo -e "  Swagger  : http://${HOST}:${PORT}/docs"
echo -e "  ReDoc    : http://${HOST}:${PORT}/redoc"
echo -e "  Health   : http://${HOST}:${PORT}/health"
echo ""

exec uvicorn app.main:app \
    --host "$HOST" \
    --port "$PORT" \
    --workers 1 \
    $RELOAD_FLAG \
    --log-level info
