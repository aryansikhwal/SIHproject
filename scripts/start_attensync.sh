#!/bin/bash
# AttenSync - Unified Startup Script for Linux/macOS
# Starts all components: Backend, Frontend, and RFID Hardware Listener

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Default options
SKIP_DEPS=false
NO_RFID=false
DEV_MODE=true

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-deps)
            SKIP_DEPS=true
            shift
            ;;
        --no-rfid)
            NO_RFID=true
            shift
            ;;
        --production)
            DEV_MODE=false
            shift
            ;;
        -h|--help)
            echo "AttenSync Unified Startup Script"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --skip-deps     Skip dependency installation"
            echo "  --no-rfid       Skip RFID hardware listener"
            echo "  --production    Run in production mode"
            echo "  -h, --help      Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}🚀 AttenSync Unified Startup Script${NC}"
echo -e "${BLUE}================================================${NC}"

# Get script directory and set project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo -e "${CYAN}📁 Project Root: $PROJECT_ROOT${NC}"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    if command_exists netstat; then
        netstat -tuln | grep -q ":$1 "
    elif command_exists ss; then
        ss -tuln | grep -q ":$1 "
    else
        return 1  # Can't check, assume it's free
    fi
}

# Function to cleanup background processes
cleanup() {
    echo -e "\n${YELLOW}🛑 Stopping all AttenSync services...${NC}"
    
    if [[ -n $BACKEND_PID ]] && kill -0 $BACKEND_PID 2>/dev/null; then
        echo "Stopping Backend Server (PID: $BACKEND_PID)"
        kill -TERM $BACKEND_PID 2>/dev/null || kill -KILL $BACKEND_PID 2>/dev/null
    fi
    
    if [[ -n $FRONTEND_PID ]] && kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "Stopping Frontend Server (PID: $FRONTEND_PID)"
        kill -TERM $FRONTEND_PID 2>/dev/null || kill -KILL $FRONTEND_PID 2>/dev/null
    fi
    
    if [[ -n $RFID_PID ]] && kill -0 $RFID_PID 2>/dev/null; then
        echo "Stopping RFID Listener (PID: $RFID_PID)"
        kill -TERM $RFID_PID 2>/dev/null || kill -KILL $RFID_PID 2>/dev/null
    fi
    
    # Kill any remaining processes
    pkill -f "python.*backend.py" 2>/dev/null || true
    pkill -f "npm.*start" 2>/dev/null || true
    pkill -f "python.*rfid_system.py" 2>/dev/null || true
    
    echo -e "${GREEN}✅ All services stopped. Goodbye!${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM EXIT

# Check prerequisites
echo -e "\n${YELLOW}🔍 Checking Prerequisites...${NC}"
prereqs_ok=true

if ! command_exists python3; then
    if ! command_exists python; then
        echo -e "${RED}❌ Python not found! Please install Python 3.8+${NC}"
        prereqs_ok=false
    fi
fi

if ! command_exists node; then
    echo -e "${RED}❌ Node.js not found! Please install Node.js 16+${NC}"
    prereqs_ok=false
fi

if ! command_exists npm; then
    echo -e "${RED}❌ npm not found! Please install Node.js with npm${NC}"
    prereqs_ok=false
fi

if [ "$prereqs_ok" = false ]; then
    echo -e "\n${RED}❌ Prerequisites missing! Please install required software.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed!${NC}"

# Determine Python command
PYTHON_CMD="python3"
if ! command_exists python3; then
    PYTHON_CMD="python"
fi

# Install dependencies if not skipped
if [ "$SKIP_DEPS" = false ]; then
    echo -e "\n${YELLOW}📦 Installing/Updating Dependencies...${NC}"
    
    # Install Python dependencies
    echo -e "${CYAN}🐍 Installing Python packages...${NC}"
    $PYTHON_CMD -m pip install -r requirements.txt || {
        echo -e "${YELLOW}⚠️  Python dependencies installation had issues, continuing...${NC}"
    }
    
    # Install Node.js dependencies
    echo -e "${CYAN}📦 Installing Node.js packages...${NC}"
    cd "src/frontend"
    npm install || {
        echo -e "${YELLOW}⚠️  Node.js dependencies installation had issues, continuing...${NC}"
    }
    cd "$PROJECT_ROOT"
    
    echo -e "${GREEN}✅ Dependencies installation completed!${NC}"
fi

# Check for port conflicts
echo -e "\n${YELLOW}🔌 Checking port availability...${NC}"
if port_in_use 5000; then
    echo -e "${YELLOW}⚠️  Port 5000 is already in use. Backend may not start properly.${NC}"
fi
if port_in_use 3000; then
    echo -e "${YELLOW}⚠️  Port 3000 is already in use. Frontend may not start properly.${NC}"
fi

# Create log directory
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"

echo -e "\n${GREEN}🚀 Starting AttenSync Components...${NC}"

# Start Backend Server
echo -e "${CYAN}🔥 Starting Backend Server (Flask)...${NC}"
cd "$PROJECT_ROOT/src/backend"
if [ "$DEV_MODE" = true ]; then
    export FLASK_ENV=development
    export FLASK_DEBUG=1
fi
$PYTHON_CMD backend.py > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
cd "$PROJECT_ROOT"

# Wait for backend to initialize
sleep 3

# Start Frontend Development Server
echo -e "${CYAN}⚛️  Starting Frontend Server (React)...${NC}"
cd "$PROJECT_ROOT/src/frontend"
export BROWSER=none  # Prevent auto-opening browser
npm start > "$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
cd "$PROJECT_ROOT"

# Start RFID Hardware Listener (optional)
if [ "$NO_RFID" = false ]; then
    echo -e "${CYAN}📡 Starting RFID Hardware Listener...${NC}"
    cd "$PROJECT_ROOT/src/hardware"
    $PYTHON_CMD rfid_system.py > "$LOG_DIR/rfid.log" 2>&1 &
    RFID_PID=$!
    echo -e "${GREEN}✅ RFID Listener started (PID: $RFID_PID)${NC}"
    cd "$PROJECT_ROOT"
else
    echo -e "${YELLOW}⏭️  RFID Listener skipped (--no-rfid flag)${NC}"
fi

# Wait for services to fully start
echo -e "${YELLOW}⏳ Waiting for services to initialize...${NC}"
sleep 5

# Display service information
echo -e "\n${GREEN}🌐 AttenSync Services Running:${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${WHITE}🔥 Backend API:    http://localhost:5000${NC}"
echo -e "${WHITE}⚛️  Frontend Web:   http://localhost:3000${NC}"
echo -e "${WHITE}📊 API Health:     http://localhost:5000/api/health${NC}"
if [ "$NO_RFID" = false ]; then
    echo -e "${WHITE}📡 RFID Listener:  Active (check logs/rfid.log)${NC}"
fi
echo -e "${BLUE}========================================${NC}"

echo -e "\n${YELLOW}💡 Commands:${NC}"
echo -e "${WHITE}  • Press Ctrl+C to quit all services${NC}"
echo -e "${WHITE}  • Logs are available in the logs/ directory${NC}"
echo -e "${WHITE}  • Backend log: tail -f logs/backend.log${NC}"
echo -e "${WHITE}  • Frontend log: tail -f logs/frontend.log${NC}"
if [ "$NO_RFID" = false ]; then
    echo -e "${WHITE}  • RFID log: tail -f logs/rfid.log${NC}"
fi

# Function to check service health
check_services() {
    echo -e "\n${CYAN}📊 Service Status:${NC}"
    
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${GREEN}✅ Backend Server (PID: $BACKEND_PID) - Running${NC}"
    else
        echo -e "${RED}❌ Backend Server - Not Running${NC}"
    fi
    
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${GREEN}✅ Frontend Server (PID: $FRONTEND_PID) - Running${NC}"
    else
        echo -e "${RED}❌ Frontend Server - Not Running${NC}"
    fi
    
    if [ "$NO_RFID" = false ]; then
        if kill -0 $RFID_PID 2>/dev/null; then
            echo -e "${GREEN}✅ RFID Listener (PID: $RFID_PID) - Running${NC}"
        else
            echo -e "${RED}❌ RFID Listener - Not Running${NC}"
        fi
    fi
}

# Initial service check
check_services

# Keep script running and periodically check services
echo -e "\n${GREEN}🎯 AttenSync is running! Press Ctrl+C to stop all services.${NC}"

# Monitor services every 30 seconds
while true; do
    sleep 30
    
    # Check if any service died unexpectedly
    services_running=true
    
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "\n${RED}❌ Backend Server stopped unexpectedly!${NC}"
        services_running=false
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "\n${RED}❌ Frontend Server stopped unexpectedly!${NC}"
        services_running=false
    fi
    
    if [ "$NO_RFID" = false ] && ! kill -0 $RFID_PID 2>/dev/null; then
        echo -e "\n${YELLOW}⚠️  RFID Listener stopped (this is normal if no hardware)${NC}"
    fi
    
    if [ "$services_running" = false ]; then
        echo -e "${YELLOW}🔄 Some services stopped. Check logs for details.${NC}"
        echo -e "${WHITE}💡 Press Ctrl+C to quit and restart if needed.${NC}"
    fi
done