#!/usr/bin/env python3
"""
Database Setup Script for Inventory Management System
This script sets up the database with proper migrations and creates an admin user.
"""

import os
import sys
import django
import subprocess
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def setup_database():
    """Set up the database with migrations"""
    print("🚀 Starting Database Setup for Inventory Management System")
    print("=" * 60)
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Check if manage.py exists
    if not os.path.exists('manage.py'):
        print("❌ manage.py not found. Please run this script from the correct directory.")
        return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Make migrations
    if not run_command("python manage.py makemigrations", "Creating database migrations"):
        return False
    
    # Apply migrations
    if not run_command("python manage.py migrate", "Applying database migrations"):
        return False
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        return False
    
    # Create superuser
    print("\n🔄 Creating superuser account...")
    try:
        django.setup()
        from django.contrib.auth.models import User
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@inventory.com',
                password='admin123',
                first_name='System',
                last_name='Administrator'
            )
            print("✅ Superuser 'admin' created successfully")
            print("   Username: admin")
            print("   Password: admin123")
            print("   Email: admin@inventory.com")
        else:
            print("ℹ️  Superuser 'admin' already exists")
    except Exception as e:
        print(f"❌ Failed to create superuser: {e}")
        return False
    
    print("\n🎉 Database setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the data generation script: python scripts/generate_dummy_data.py")
    print("2. Start the Django server: python manage.py runserver")
    print("3. Access the admin panel at: http://localhost:8000/admin")
    print("4. Access the API documentation at: http://localhost:8000/api/docs/")
    
    return True

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)