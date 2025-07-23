# Inventory Management System - Setup Scripts

This directory contains helper scripts to set up the database and generate dummy data for the Inventory Management System.

## 🚀 Quick Start

The easiest way to get started is to use the shell script:

```bash
cd inventory-app
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This will:
1. Set up the PostgreSQL database with all migrations
2. Create an admin superuser account
3. Generate comprehensive dummy data
4. Start all services (frontend, backend, database)

## 📁 Available Scripts

### 1. `setup.sh` (Recommended)
**Shell script wrapper for easy setup**

```bash
# Complete setup (database + data + services)
./scripts/setup.sh

# Database setup only
./scripts/setup.sh db-only

# Generate dummy data only (requires existing database)
./scripts/setup.sh data-only

# Show help
./scripts/setup.sh help
```

### 2. `setup_complete.py`
**Master Python script that runs both database setup and data generation**

```bash
# Run from inventory-app directory
python scripts/setup_complete.py
```

### 3. `setup_database.py`
**Database setup and admin user creation**

```bash
# Set up database with migrations and create superuser
python scripts/setup_database.py
```

### 4. `generate_dummy_data.py`
**Comprehensive dummy data generation**

```bash
# Generate realistic sample data (requires database to be set up first)
python scripts/generate_dummy_data.py
```

## 🗃️ Generated Dummy Data

The scripts generate realistic sample data including:

### Core Data
- **8 Categories** with hierarchical structure (Electronics → Computers, etc.)
- **10 Tags** with color coding (High Value, Fragile, Hazardous, etc.)
- **5 Suppliers** with complete contact information
- **3 Warehouses** (Main Distribution Center, West Coast Facility, East Coast Hub)

### Location Structure
- **Hierarchical locations**: Warehouse → Zone → Aisle → Rack → Bin
- **12 Zones** (4 zones per warehouse: A, B, C, D)
- **36 Aisles** (3 aisles per zone)
- **180 Racks** (5 racks per aisle)
- **240 Bin Locations** (multiple bins per rack with capacity limits)

### Product Management
- **4 Product Templates** (Laptop Computer, Office Chair, Industrial Drill Bit Set, Chemical Solvent)
- **12 Product Variants** with different specifications (size, color, material)
- **14 Items** (from variants + standalone items)
- **14 Barcodes** (EAN-13 format for all items)

### Inventory Tracking
- **Batches** for items that require batch tracking
- **Stock Levels** across multiple locations
- **Stock Movements** with complete audit trail
- **Stock Reservations** for order management
- **Cycle Counts** for inventory accuracy

### Additional Features
- **3 Label Templates** (Item, Location, Bin labels)
- **Expiry tracking** for applicable items
- **Serial number tracking** for high-value items
- **Quality control** status for batches

## 🔐 Default Admin Account

The setup creates an admin superuser with these credentials:

- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@inventory.com`

⚠️ **Security Note**: Change these credentials in production!

## 🌐 Access URLs

After setup completion, access the system at:

- **Frontend (React)**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **API Documentation**: http://localhost:8000/api/docs/
- **Django Admin**: http://localhost:8000/admin

## 🔧 Prerequisites

### For Shell Script (`setup.sh`)
- Docker and Docker Compose installed
- Bash shell (Linux/macOS/WSL)

### For Python Scripts
- Python 3.8+
- Django 4.2.7
- PostgreSQL database running
- All dependencies from `requirements.txt`

## 📊 Data Statistics

After running the complete setup, you'll have:

```
Categories: 17 (including subcategories)
Tags: 10
Suppliers: 5
Warehouses: 3
Locations: 228 (zones, aisles, racks)
Bin Locations: 240
Product Templates: 4
Product Variants: 12
Items: 14
Barcodes: 14
Batches: ~20-30 (for items that track batches)
Stock Levels: ~40-50 (items across multiple locations)
Stock Movements: ~40-50 (initial receipts)
Labels: 3
Reservations: 10
Cycle Counts: ~6
```

## 🛠️ Troubleshooting

### Common Issues

**1. Docker not running**
```bash
# Error: Cannot connect to Docker daemon
# Solution: Start Docker Desktop or Docker service
sudo systemctl start docker  # Linux
```

**2. Port conflicts**
```bash
# Error: Port 5432/8000/3000 already in use
# Solution: Stop conflicting services or change ports in docker-compose.yml
```

**3. Database connection issues**
```bash
# Error: Could not connect to database
# Solution: Wait for database to fully start (the script includes wait logic)
docker-compose logs db  # Check database logs
```

**4. Permission denied on setup.sh**
```bash
# Error: Permission denied
# Solution: Make script executable
chmod +x scripts/setup.sh
```

### Reset Everything

To completely reset and start over:

```bash
# Stop all services
docker-compose down

# Remove all data (⚠️ This deletes everything!)
docker-compose down -v

# Remove Docker images (optional)
docker-compose down --rmi all

# Run setup again
./scripts/setup.sh
```

## 🔍 Script Details

### Database Setup Process
1. Install Python dependencies
2. Create Django migrations
3. Apply migrations to database
4. Collect static files
5. Create superuser account

### Data Generation Process
1. Create categories with hierarchical structure
2. Create tags with color coding
3. Create suppliers with contact information
4. Create warehouses and location hierarchy
5. Create product templates and variants
6. Create items with SKUs and barcodes
7. Create batches for trackable items
8. Create stock levels across locations
9. Create stock movements (receipts)
10. Create label templates
11. Create reservations and cycle counts

## 📝 Customization

### Modifying Generated Data

To customize the dummy data:

1. Edit `generate_dummy_data.py`
2. Modify the data dictionaries in each function
3. Run the data generation script again

### Adding New Data Types

1. Create new functions in `generate_dummy_data.py`
2. Follow the existing pattern of creating realistic sample data
3. Add the function call to the `main()` function

## 🤝 Contributing

When adding new setup functionality:

1. Follow the existing error handling patterns
2. Add appropriate logging and status messages
3. Update this README with new script information
4. Test with a clean database

## 📚 Related Documentation

- [Main Project README](../README.md)
- [Database Schema Documentation](../docs/database-schema.md)
- [System Design Documentation](../docs/system-design.md)
- [API Documentation](http://localhost:8000/api/docs/) (after setup)

---

**Need help?** Check the main project README or open an issue on GitHub.