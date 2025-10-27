#!/bin/bash

# ==============================================
# GDE Docker Management Script
# ==============================================
# Este script facilita la gestión del stack Docker de GDE

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if docker and docker-compose are installed
check_requirements() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    print_success "Docker and Docker Compose are installed"
}

# Create .env.docker if it doesn't exist
setup_env() {
    if [ ! -f .env.docker ]; then
        print_warning ".env.docker not found. Creating from template..."
        if [ -f .env.docker.example ]; then
            cp .env.docker.example .env.docker
            print_success ".env.docker created. Please configure it before continuing."
        else
            print_error ".env.docker.example not found"
            exit 1
        fi
    else
        print_success ".env.docker found"
    fi
}

# Build all containers
build_all() {
    print_header "Building all containers..."
    docker-compose --env-file .env.docker build --no-cache
    print_success "All containers built successfully"
}

# Start all services
start_all() {
    print_header "Starting all services..."
    docker-compose --env-file .env.docker up -d
    print_success "All services started"
    print_info "Access the application:"
    echo "  - Frontend: http://localhost:3000"
    echo "  - Backend API: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - Nginx: http://localhost:80"
    echo "  - PgAdmin: http://localhost:5050 (if using --profile tools)"
}

# Stop all services
stop_all() {
    print_header "Stopping all services..."
    docker-compose --env-file .env.docker down
    print_success "All services stopped"
}

# Restart all services
restart_all() {
    print_header "Restarting all services..."
    docker-compose --env-file .env.docker restart
    print_success "All services restarted"
}

# Show logs
show_logs() {
    if [ -z "$1" ]; then
        docker-compose --env-file .env.docker logs -f
    else
        docker-compose --env-file .env.docker logs -f "$1"
    fi
}

# Show status
show_status() {
    print_header "Services Status"
    docker-compose --env-file .env.docker ps
}

# Clean everything (including volumes)
clean_all() {
    print_warning "This will remove all containers, volumes, and data. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_header "Cleaning all Docker resources..."
        docker-compose --env-file .env.docker down -v --remove-orphans
        print_success "All Docker resources cleaned"
    else
        print_info "Clean cancelled"
    fi
}

# Execute command in container
exec_container() {
    if [ -z "$1" ]; then
        print_error "Please specify a container name (backend, frontend, db, redis, nginx)"
        exit 1
    fi
    
    print_info "Executing shell in $1..."
    docker-compose --env-file .env.docker exec "$1" sh
}

# Database backup
backup_db() {
    print_header "Creating database backup..."
    BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
    docker-compose --env-file .env.docker exec -T db pg_dump -U gde_user gde_db > "$BACKUP_FILE"
    print_success "Database backed up to $BACKUP_FILE"
}

# Database restore
restore_db() {
    if [ -z "$1" ]; then
        print_error "Please specify backup file: ./docker-manage.sh restore <backup_file>"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        print_error "Backup file not found: $1"
        exit 1
    fi
    
    print_warning "This will restore database from $1. Continue? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_header "Restoring database from $1..."
        docker-compose --env-file .env.docker exec -T db psql -U gde_user gde_db < "$1"
        print_success "Database restored successfully"
    else
        print_info "Restore cancelled"
    fi
}

# Main menu
show_menu() {
    print_header "GDE Docker Management"
    echo "Commands:"
    echo "  setup       - Setup environment files"
    echo "  build       - Build all containers"
    echo "  start       - Start all services"
    echo "  stop        - Stop all services"
    echo "  restart     - Restart all services"
    echo "  logs [svc]  - Show logs (optionally for specific service)"
    echo "  status      - Show services status"
    echo "  exec <svc>  - Execute shell in container"
    echo "  backup      - Backup database"
    echo "  restore <f> - Restore database from file"
    echo "  clean       - Remove all containers and volumes"
    echo "  help        - Show this menu"
    echo ""
    echo "Services: backend, frontend, db, redis, nginx, pgadmin"
}

# Main script
main() {
    check_requirements

    case "${1:-help}" in
        setup)
            setup_env
            ;;
        build)
            setup_env
            build_all
            ;;
        start)
            setup_env
            start_all
            ;;
        stop)
            stop_all
            ;;
        restart)
            restart_all
            ;;
        logs)
            show_logs "$2"
            ;;
        status)
            show_status
            ;;
        exec)
            exec_container "$2"
            ;;
        backup)
            backup_db
            ;;
        restore)
            restore_db "$2"
            ;;
        clean)
            clean_all
            ;;
        help|*)
            show_menu
            ;;
    esac
}

# Run main function
main "$@"
