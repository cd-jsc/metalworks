# Inventory Management System

A comprehensive full-stack inventory management application built with Django REST Framework and React, featuring advanced warehouse management, product variants, barcode integration, and flexible tagging systems.

## 🚀 Features

### 📦 **Core Inventory Management**
- **Item Master Data**: Complete item information with SKU, descriptions, and specifications
- **Multi-dimensional Stock Tracking**: Track inventory across warehouses, locations, and bin levels
- **Batch/Lot Tracking**: Full traceability with expiry dates and quality control
- **Real-time Stock Levels**: Live inventory quantities with reservation management

### 🏷️ **Enhanced Product Organization**
- **Product Templates**: Define product families with shared attributes
- **Product Variants**: Manage size, color, material, and style variations
- **Flexible Tagging**: Multi-dimensional classification with color-coded tags
- **Hierarchical Categories**: Organize products in nested category structures

### 🏢 **Advanced Warehouse Management**
- **Multi-Warehouse Support**: Manage multiple physical locations
- **Hierarchical Locations**: Warehouse → Zone → Aisle → Rack → Shelf structure
- **Bin Location Management**: Track inventory down to specific bin positions
- **Location Barcoding**: Scannable barcodes for locations and bins
- **Capacity Management**: Monitor volume and weight constraints

### 🔍 **Barcode & Labeling System**
- **Multiple Barcode Types**: EAN-13, EAN-8, UPC, Code 128, Code 39, QR codes
- **Barcode Generation**: Automatic barcode creation with configurable formats
- **Item Lookup**: Quick item identification via barcode scanning
- **Label Templates**: Customizable label designs for items, locations, and bins
- **Print Integration**: On-demand label printing functionality

### 📊 **Operations Management**
- **Stock Movements**: Complete audit trail of all inventory transactions
- **Inter-location Transfers**: Move stock between warehouses and locations
- **Stock Reservations**: Reserve inventory for orders and allocations
- **Cycle Counting**: Scheduled and ad-hoc inventory counts
- **Adjustment Tracking**: Record and track inventory adjustments

### 📈 **Analytics & Reporting**
- **Real-time Dashboard**: Key metrics and inventory insights
- **Low Stock Alerts**: Automatic notifications for items below reorder points
- **Expiry Monitoring**: Track and alert on expiring batches
- **Movement History**: Detailed transaction history and audit trails
- **Stock Utilization**: Warehouse and location capacity analysis

## 🛠 Technology Stack

### Backend
- **Framework**: Django 4.2.7 with Django REST Framework
- **Database**: PostgreSQL 15
- **API Documentation**: DRF Spectacular (OpenAPI/Swagger)
- **Authentication**: Django's built-in authentication system
- **Task Queue**: Celery with Redis (for background tasks)

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Notifications**: React Toastify
- **Icons**: Heroicons

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL with optimized indexing
- **File Storage**: Local storage (configurable for cloud)
- **Environment Management**: Python-decouple

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd inventory-app
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000/api
   - **API Documentation**: http://localhost:8000/api/docs/
   - **Django Admin**: http://localhost:8000/admin

4. **Create a superuser** (optional)
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

The application will automatically:
- Set up the PostgreSQL database
- Run Django migrations
- Install all dependencies
- Start both frontend and backend services

## 📁 Project Structure

```
inventory-app/
├── backend/                    # Django backend
│   ├── inventory_project/     # Django project settings
│   ├── inventory/             # Main inventory app
│   │   ├── models.py         # Database models
│   │   ├── serializers.py    # API serializers
│   │   ├── views.py          # API views
│   │   ├── urls.py           # URL routing
│   │   └── admin.py          # Admin interface
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend container
│   └── manage.py             # Django management
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   └── App.js            # Main app component
│   ├── package.json          # Node dependencies
│   └── Dockerfile            # Frontend container
├── docs/                      # Documentation
│   ├── system-design.md      # System architecture
│   └── database-schema.md    # Database documentation
├── docker-compose.yml        # Multi-service orchestration
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://inventory_user:inventory_pass@db:5432/inventory_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Frontend (.env)**
```env
REACT_APP_API_URL=http://localhost:8000/api
```

### Database Configuration

The application uses PostgreSQL with the following default settings:
- **Database**: inventory_db
- **User**: inventory_user
- **Password**: inventory_pass
- **Host**: db (Docker service)
- **Port**: 5432

## 📊 API Endpoints

### Core Entities
- **Categories**: `/api/categories/`
- **Tags**: `/api/tags/`
- **Suppliers**: `/api/suppliers/`
- **Warehouses**: `/api/warehouses/`
- **Locations**: `/api/locations/`
- **Bin Locations**: `/api/bin-locations/`

### Product Management
- **Product Templates**: `/api/product-templates/`
- **Product Variants**: `/api/product-variants/`
- **Items**: `/api/items/`
- **Barcodes**: `/api/barcodes/`
- **Batches**: `/api/batches/`

### Stock Operations
- **Stock Levels**: `/api/stock-levels/`
- **Stock Movements**: `/api/stock-movements/`
- **Stock Reservations**: `/api/stock-reservations/`
- **Cycle Counts**: `/api/cycle-counts/`

### Utilities
- **Labels**: `/api/labels/`
- **Barcode Lookup**: `/api/barcodes/lookup_item/`
- **Stock Adjustments**: `/api/items/{id}/adjust_stock/`
- **Stock Transfers**: `/api/stock-movements/transfer/`

### Special Endpoints
- **Low Stock Items**: `/api/items/low_stock/`
- **Expiring Batches**: `/api/batches/expiring_soon/`
- **Recent Movements**: `/api/stock-movements/recent/`
- **Warehouse Summary**: `/api/warehouses/{id}/stock_summary/`

## 🎯 Usage Examples

### Creating a Product Template with Variants

1. **Create a Product Template**
   ```json
   POST /api/product-templates/
   {
     "name": "T-Shirt Basic",
     "description": "Basic cotton t-shirt",
     "category": 1,
     "tag_ids": [1, 2],
     "brand": "Fashion Co",
     "base_unit_of_measure": "pcs",
     "track_batches": false
   }
   ```

2. **Create Product Variants**
   ```json
   POST /api/product-variants/
   {
     "template": 1,
     "name": "T-Shirt Basic - Red Medium",
     "variant_code": "RED-M",
     "size": "Medium",
     "color": "Red",
     "cost_price": "15.00",
     "selling_price": "29.99"
   }
   ```

3. **Create Items from Variants**
   ```json
   POST /api/items/
   {
     "sku": "TSH-RED-M-001",
     "name": "T-Shirt Basic - Red Medium",
     "product_variant": 1,
     "unit_of_measure": "pcs",
     "minimum_stock": 10,
     "reorder_point": 5
   }
   ```

### Warehouse and Location Setup

1. **Create a Warehouse**
   ```json
   POST /api/warehouses/
   {
     "name": "Main Warehouse",
     "code": "WH001",
     "warehouse_type": "main",
     "address": "123 Industrial Blvd",
     "city": "Manufacturing City",
     "state": "CA",
     "postal_code": "90210"
   }
   ```

2. **Create Locations**
   ```json
   POST /api/locations/
   {
     "warehouse": 1,
     "name": "Zone A",
     "code": "A",
     "location_type": "zone",
     "barcode": "LOC-A-001"
   }
   ```

3. **Create Bin Locations**
   ```json
   POST /api/bin-locations/
   {
     "location": 1,
     "bin_code": "A01",
     "barcode": "BIN-A01-001",
     "capacity": "100.00",
     "max_weight": "500.00"
   }
   ```

### Stock Operations

1. **Adjust Stock**
   ```json
   POST /api/items/1/adjust_stock/
   {
     "warehouse": 1,
     "location": 1,
     "bin_location": 1,
     "quantity": 50,
     "reason": "Initial stock"
   }
   ```

2. **Transfer Stock**
   ```json
   POST /api/stock-movements/transfer/
   {
     "item": 1,
     "from_warehouse": 1,
     "from_location": 1,
     "from_bin_location": 1,
     "to_warehouse": 1,
     "to_location": 2,
     "to_bin_location": 2,
     "quantity": 10,
     "reason": "Replenishment"
   }
   ```

3. **Barcode Lookup**
   ```json
   POST /api/barcodes/lookup_item/
   {
     "barcode_data": "1234567890123"
   }
   ```

## 🧪 Development

### Running Tests
```bash
# Backend tests
docker-compose exec backend python manage.py test

# Frontend tests
docker-compose exec frontend npm test
```

### Database Migrations
```bash
# Create migrations
docker-compose exec backend python manage.py makemigrations

# Apply migrations
docker-compose exec backend python manage.py migrate
```

### Accessing Services
```bash
# Backend shell
docker-compose exec backend python manage.py shell

# Database shell
docker-compose exec db psql -U inventory_user -d inventory_db

# Frontend shell
docker-compose exec frontend sh
```

## 🚀 Deployment

### Production Environment

1. **Environment Setup**
   - Set `DEBUG=False` in backend environment
   - Configure proper `SECRET_KEY`
   - Set up production database credentials
   - Configure static file serving

2. **Database**
   - Use managed PostgreSQL service
   - Set up regular backups
   - Configure connection pooling

3. **Static Files**
   - Configure Django's static file serving
   - Consider using CDN for static assets

4. **Security**
   - Enable HTTPS
   - Configure CORS properly
   - Set up proper authentication
   - Regular security updates

### Docker Production
```bash
# Build for production
docker-compose -f docker-compose.prod.yml up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript code
- Write tests for new features
- Update documentation as needed
- Follow conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `/docs` folder for detailed documentation
- **API Reference**: Visit `/api/docs/` for interactive API documentation
- **Issues**: Report bugs and request features via GitHub Issues
- **Wiki**: Check the project wiki for additional guides and tutorials

## 🔮 Roadmap

### Upcoming Features
- **Mobile App**: React Native mobile application
- **Advanced Analytics**: Business intelligence dashboard
- **Integration APIs**: Third-party system integrations
- **Workflow Automation**: Automated reordering and notifications
- **Multi-tenant Support**: Support for multiple organizations
- **Advanced Reporting**: Custom report builder
- **Audit Logging**: Enhanced audit trail and compliance features

### Performance Enhancements
- **Caching Layer**: Redis caching for improved performance
- **Database Optimization**: Query optimization and indexing
- **Real-time Updates**: WebSocket integration for live updates
- **Bulk Operations**: Efficient bulk import/export functionality

---

**Built with ❤️ for efficient inventory management**