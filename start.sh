#!/bin/bash

# ─────────────────────────────────────────────
#  Colours
# ─────────────────────────────────────────────
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

print_step()  { echo -e "\n${CYAN}${BOLD}$1${RESET}"; }
print_ok()    { echo -e "${GREEN}✅  $1${RESET}"; }
print_info()  { echo -e "${YELLOW}ℹ️   $1${RESET}"; }
print_error() { echo -e "${RED}❌  $1${RESET}"; }

spinner() {
    local pid=$1
    local msg=$2
    local frames=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")
    local i=0
    while kill -0 "$pid" 2>/dev/null; do
        printf "\r${CYAN}  ${frames[$i]} ${msg}${RESET}"
        i=$(( (i+1) % ${#frames[@]} ))
        sleep 0.1
    done
    printf "\r\033[K"
}

# ─────────────────────────────────────────────
#  Banner
# ─────────────────────────────────────────────
echo -e "${GREEN}${BOLD}"
echo "  ███████╗██████╗ ██╗            █████╗  ██████╗ ███████╗███╗   ██╗████████╗"
echo "  ██╔════╝██╔══██╗██║           ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝"
echo "  █████╗  ██████╔╝██║   ────   ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   "
echo "  ██╔══╝  ██╔═══╝ ██║           ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   "
echo "  ██║     ██║     ███████╗       ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   "
echo "  ╚═╝     ╚═╝     ╚══════╝       ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝  "
echo -e "${RESET}"
echo -e "${BOLD}  🤖 FPL-Agent — AI-powered Fantasy Premier League Assistant${RESET}"
echo -e "  ─────────────────────────────────────────────────────────\n"

# ─────────────────────────────────────────────
#  Load env
# ─────────────────────────────────────────────
print_step "📂 Loading environment..."

ENV_FILE="${1:-.env}"

if [ ! -f "$ENV_FILE" ]; then
    print_error "$ENV_FILE not found. Rename .env.sample to .env and fill in your values."
    exit 1
fi

export $(grep -v '^#' "$ENV_FILE" | xargs)
print_ok "Environment loaded from $ENV_FILE  (APP_ENV=${APP_ENV})"

# ─────────────────────────────────────────────
#  Create log directories
# ─────────────────────────────────────────────
print_step "📋 Setting up log directories..."

setup_log() {
    local dir="${1:-logs}"
    local file="$2"
    mkdir -p "$dir" && touch "$dir/$file"
    print_ok "$dir/$file"
}

setup_log "${ETL_LOGS_DIR:-logs}"         "etl.log"
setup_log "${WEBSERVICE_LOGS_DIR:-logs}"  "api.log"
setup_log "${FRONTEND_LOGS_DIR:-logs}"    "frontend.log"

# ─────────────────────────────────────────────
#  Export HF token
# ─────────────────────────────────────────────
if [ -n "$HF_TOKEN" ]; then
    print_step "🔑 Exporting Hugging Face token..."
    export HUGGINGFACEHUB_API_TOKEN=$HF_TOKEN
    print_ok "HUGGINGFACEHUB_API_TOKEN set"
fi

# ─────────────────────────────────────────────
#  Start webservice
# ─────────────────────────────────────────────
print_step "🚀 Starting webservice..."

if [ "$APP_ENV" = "dev" ]; then
    fastapi dev Web/webservice/main.py > /dev/null 2>&1 &
else
    fastapi run Web/webservice/main.py > /dev/null 2>&1 &
fi
WEBSERVICE_PID=$!

# spinner while waiting
(
    until curl -s http://${API_HOST:-127.0.0.1}:8000/docs > /dev/null 2>&1; do
        sleep 2
    done
) &
WAIT_PID=$!
spinner $WAIT_PID "Waiting for webservice on ${API_HOST:-127.0.0.1}:8000"
wait $WAIT_PID

print_ok "Webservice is live → http://${API_HOST:-127.0.0.1}:8000"
print_info "API docs → http://${API_HOST:-127.0.0.1}:8000/docs"

# ─────────────────────────────────────────────
#  Start frontend
# ─────────────────────────────────────────────
print_step "🌐 Starting frontend..."
print_ok "Frontend is live → http://${API_HOST:-127.0.0.1}:5000"
echo ""

python3 Web/frontend/app.py
