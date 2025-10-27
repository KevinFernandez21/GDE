#!/bin/bash

# GDE System - Docker Management Script
# Usage: ./docker-manage.sh [start|stop|restart|logs|status|clean]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  GDE System - Docker Manager  ${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Check if docker-compose is available
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi

    if ! command -v docker &> /dev/null || ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not available. Please install Docker with Compose support."
        exit 1
    fi
}

# Check if .env file exists
check_env() {
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from template..."
        if [ -f env.docker ]; then
            cp env.docker .env
            print_status ".env file created from env.docker"
        else
            print_error "No env.docker template found. Please create .env file manually."
            exit 1
        fi
    fi
}

# Start services
start_services() {
    print_header
    print_status "Starting GDE System with Docker Compose..."
    
    check_docker
    check_env
    
    # Build and start services
    docker compose up --build -d
    
    print_status "Services started successfully!"
    print_status "Waiting for services to be ready..."
    
    # Wait for services to be healthy
    sleep 10
    
    # Check service status
    docker compose ps
    
    echo ""
    print_status "🌐 Access URLs:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo "   Health Check: http://localhost:8000/health"
    echo "   Nginx (if enabled): http://localhost"
}

# Stop services
stop_services() {
    print_header
    print_status "Stopping GDE System..."
    
    docker-compose down
    
    print_status "Services stopped successfully!"
}

# Restart services
restart_services() {
    print_header
    print_status "Restarting GDE System..."
    
    docker compose restart
    
    print_status "Services restarted successfully!"
}

# Show logs
show_logs() {
    print_header
    print_status "Showing logs for all services..."
    
    docker compose logs -f
}

# Show status
show_status() {
    print_header
    print_status "Service Status:"
    
    docker compose ps
    
    echo ""
    print_status "Service Health:"
    
    # Check backend health
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_status "✅ Backend: Healthy"
    else
        print_warning "❌ Backend: Not responding"
    fi
    
    # Check frontend health
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_status "✅ Frontend: Healthy"
    else
        print_warning "❌ Frontend: Not responding"
    fi
}

# Clean up
clean_up() {
    print_header
    print_warning "This will remove all containers, volumes, and images. Are you sure? (y/N)"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        print_status "Cleaning up Docker resources..."
        
        docker compose down -v --remove-orphans
        docker system prune -f
        
        print_status "Cleanup completed!"
    else
        print_status "Cleanup cancelled."
    fi
}

# Show help
show_help() {
    print_header
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     Start all services"
    echo "  stop      Stop all services"
    echo "  restart   Restart all services"
    echo "  logs      Show logs for all services"
    echo "  status    Show service status and health"
    echo "  clean     Clean up Docker resources"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start     # Start the system"
    echo "  $0 logs      # View logs"
    echo "  $0 status    # Check status"
}

# Main script logic
case "${1:-help}" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    clean)
        clean_up
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
