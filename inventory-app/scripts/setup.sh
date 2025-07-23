#!/bin/bash

# Setup Script for Inventory Management System
# This script provides an easy way to set up the database and generate dummy data

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    printf "${1}${2}${NC}\n"
}

# Function to print section headers
print_header() {
    echo
    print_color $CYAN "=================================="
    print_color $CYAN "$1"
    print_color $CYAN "=================================="
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_color $RED "❌ Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_color $GREEN "✅ Docker is running"
}

# Function to check if we're in the right directory
check_directory() {
    if [[ ! -f "docker-compose.yml" ]]; then
        print_color $RED "❌ docker-compose.yml not found. Please run this script from the inventory-app directory."
        exit 1
    fi
    print_color $GREEN "✅ Found docker-compose.yml"
}

# Function to start services
start_services() {
    print_header "Starting Database Service"
    print_color $YELLOW "Starting PostgreSQL database..."
    
    # Start only the database service first
    docker-compose up -d db
    
    # Wait for database to be ready
    print_color $YELLOW "Waiting for database to be ready..."
    sleep 10
    
    # Check if database is ready
    max_attempts=30
    attempt=1
    while [ $attempt -le $max_attempts ]; do
        if docker-compose exec -T db pg_isready -U inventory_user -d inventory_db > /dev/null 2>&1; then
            print_color $GREEN "✅ Database is ready"
            break
        fi
        print_color $YELLOW "Waiting for database... (attempt $attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        print_color $RED "❌ Database failed to start after $max_attempts attempts"
        exit 1
    fi
}

# Function to run setup scripts
run_setup() {
    print_header "Running Database Setup and Data Generation"
    
    # Build the backend service
    print_color $YELLOW "Building backend service..."
    docker-compose build backend
    
    # Run the complete setup
    print_color $YELLOW "Running complete setup (database + dummy data)..."
    docker-compose run --rm backend python /app/scripts/setup_complete.py
}

# Function to start all services
start_all_services() {
    print_header "Starting All Services"
    print_color $YELLOW "Starting frontend and backend services..."
    docker-compose up -d
    
    # Wait a moment for services to start
    sleep 5
    
    # Check service status
    print_color $GREEN "✅ Services started successfully"
    print_color $CYAN "Service status:"
    docker-compose ps
}

# Function to display access information
show_access_info() {
    print_header "🎉 Setup Complete!"
    
    print_color $GREEN "Your Inventory Management System is ready!"
    echo
    print_color $CYAN "📱 Access URLs:"
    print_color $WHITE "  • Frontend (React):        http://localhost:3000"
    print_color $WHITE "  • Backend API:             http://localhost:8000/api"
    print_color $WHITE "  • API Documentation:       http://localhost:8000/api/docs/"
    print_color $WHITE "  • Django Admin Panel:      http://localhost:8000/admin"
    echo
    print_color $CYAN "🔐 Admin Credentials:"
    print_color $WHITE "  Username: admin"
    print_color $WHITE "  Password: admin123"
    echo
    print_color $CYAN "🛠️  Useful Commands:"
    print_color $WHITE "  • View logs:           docker-compose logs -f"
    print_color $WHITE "  • Stop services:       docker-compose down"
    print_color $WHITE "  • Restart services:    docker-compose restart"
    print_color $WHITE "  • Access backend:      docker-compose exec backend bash"
    print_color $WHITE "  • Access database:     docker-compose exec db psql -U inventory_user -d inventory_db"
    echo
    print_color $YELLOW "💡 Pro Tip: Check the API documentation at http://localhost:8000/api/docs/ to explore all available endpoints!"
}

# Main execution
main() {
    print_header "🚀 Inventory Management System Setup"
    print_color $YELLOW "This script will set up your complete inventory management system with:"
    echo "  • PostgreSQL database with migrations"
    echo "  • Admin user account"
    echo "  • Comprehensive dummy data"
    echo "  • All services running and ready to use"
    echo
    
    # Confirmation
    read -p "Do you want to proceed? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_color $YELLOW "Setup cancelled."
        exit 0
    fi
    
    # Run setup steps
    check_docker
    check_directory
    start_services
    run_setup
    start_all_services
    show_access_info
}

# Handle script arguments
case "${1:-}" in
    "db-only")
        print_header "Database Setup Only"
        check_docker
        check_directory
        start_services
        docker-compose run --rm backend python /app/scripts/setup_database.py
        ;;
    "data-only")
        print_header "Dummy Data Generation Only"
        check_docker
        check_directory
        docker-compose run --rm backend python /app/scripts/generate_dummy_data.py
        ;;
    "help"|"-h"|"--help")
        print_color $CYAN "Inventory Management System Setup Script"
        echo
        print_color $YELLOW "Usage:"
        echo "  ./setup.sh           # Complete setup (database + data + services)"
        echo "  ./setup.sh db-only   # Database setup only"
        echo "  ./setup.sh data-only # Generate dummy data only"
        echo "  ./setup.sh help      # Show this help message"
        ;;
    *)
        main
        ;;
esac