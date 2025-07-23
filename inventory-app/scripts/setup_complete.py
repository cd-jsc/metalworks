#!/usr/bin/env python3
"""
Complete Setup Script for Inventory Management System
This script runs both database setup and dummy data generation in sequence.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n🔄 {description}...")
    print("=" * 60)
    
    script_path = Path(__file__).parent / script_name
    
    try:
        result = subprocess.run([sys.executable, str(script_path)], check=True)
        print(f"\n✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False

def main():
    """Main function to run complete setup"""
    print("🚀 Complete Setup for Inventory Management System")
    print("=" * 60)
    print("This script will:")
    print("1. Set up the database with migrations")
    print("2. Create a superuser account")
    print("3. Generate comprehensive dummy data")
    print("4. Prepare the system for immediate use")
    print("=" * 60)
    
    # Confirm before proceeding
    response = input("\nDo you want to proceed? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Setup cancelled by user.")
        return False
    
    # Step 1: Database setup
    if not run_script("setup_database.py", "Setting up database and creating superuser"):
        print("\n❌ Database setup failed. Please check the errors above.")
        return False
    
    # Step 2: Generate dummy data
    if not run_script("generate_dummy_data.py", "Generating comprehensive dummy data"):
        print("\n❌ Dummy data generation failed. Please check the errors above.")
        return False
    
    print("\n🎉 Complete setup finished successfully!")
    print("\n" + "=" * 60)
    print("🌟 Your Inventory Management System is ready to use!")
    print("=" * 60)
    
    print("\n📋 What was set up:")
    print("  ✅ PostgreSQL database with all migrations applied")
    print("  ✅ Admin superuser account created")
    print("  ✅ Complete sample data including:")
    print("     • Product categories and tags")
    print("     • Suppliers and warehouses")
    print("     • Hierarchical location structure")
    print("     • Product templates and variants")
    print("     • Items with barcodes")
    print("     • Stock levels and movements")
    print("     • Batches and reservations")
    print("     • Cycle counts and labels")
    
    print("\n🚀 Next Steps:")
    print("1. Start the application:")
    print("   cd inventory-app")
    print("   docker-compose up")
    
    print("\n2. Access the application:")
    print("   • Frontend (React):        http://localhost:3000")
    print("   • Backend API:             http://localhost:8000/api")
    print("   • API Documentation:       http://localhost:8000/api/docs/")
    print("   • Django Admin Panel:      http://localhost:8000/admin")
    
    print("\n🔐 Admin Credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    
    print("\n📚 Explore the system:")
    print("   • Browse products and inventory levels")
    print("   • Test barcode scanning functionality")
    print("   • Review stock movements and history")
    print("   • Manage warehouses and locations")
    print("   • Generate reports and analytics")
    
    print("\n💡 Pro Tips:")
    print("   • Use the API documentation to explore all endpoints")
    print("   • Check the Django admin for detailed data management")
    print("   • Try scanning the generated barcodes")
    print("   • Explore the hierarchical location structure")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)