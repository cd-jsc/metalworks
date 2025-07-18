# Inventory Management System

A comprehensive full-stack inventory management application built with Django REST Framework, React, and PostgreSQL.

## Features

### Core Functionality
- **Item Master Data Management**: Complete item catalog with SKUs, descriptions, categories, and specifications
- **Multi-Location Support**: Manage inventory across multiple warehouses and locations
- **Stock Level Tracking**: Real-time stock quantities with reserved stock management
- **Batch/Lot Tracking**: Full traceability with batch numbers, expiry dates, and quality status
- **Stock Movements**: Complete audit trail of all inventory transactions
- **Cycle Counting**: Scheduled inventory counts with variance tracking
- **Low Stock Alerts**: Automated alerts for items below reorder points
- **Supplier Management**: Vendor information and supplier tracking
- **Category Management**: Hierarchical product categorization

### Advanced Features
- **Stock Reservations**: Reserve inventory for orders and allocations
- **Transfer Management**: Inter-location stock transfers
- **Expiry Tracking**: Monitor expiring batches and products
- **Reporting Dashboard**: Real-time analytics and KPIs
- **RESTful API**: Complete API for integrations
- **Responsive UI**: Mobile-friendly interface

## Technology Stack

### Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **PostgreSQL 15**: Database
- **Redis**: Caching and background tasks
- **Celery**: Background task processing

### Frontend
- **React 18**: Frontend framework
- **Tailwind CSS**: Styling and UI components
- **Recharts**: Data visualization
- **Axios**: HTTP client
- **React Router**: Navigation

### Infrastructure
- **Docker & Docker Compose**: Containerization
- **Nginx**: Web server (production)

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd inventory-app
   ```

2. **Build and start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs/
   - Admin Interface: http://localhost:8000/admin/

4. **Create a superuser (optional)**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

## Project Structure

```
inventory-app/
├── backend/                    # Django backend
│   ├── inventory_project/      # Django project settings
│   ├── inventory/              # Main inventory app
│   │   ├── models.py          # Database models
│   │   ├── serializers.py     # API serializers
│   │   ├── views.py           # API views
│   │   ├── urls.py            # URL routing
│   │   └── admin.py           # Admin interface
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile            # Backend container
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   └── App.js            # Main app component
│   ├── package.json          # Node dependencies
│   └── Dockerfile            # Frontend container
├── docker-compose.yml         # Container orchestration
└── docs/                      # Documentation
```

## API Endpoints

### Core Resources
- `GET /api/items/` - List all items
- `POST /api/items/` - Create new item
- `GET /api/items/{id}/` - Get item details
- `PUT /api/items/{id}/` - Update item
- `DELETE /api/items/{id}/` - Delete item

### Stock Management
- `GET /api/stock-levels/` - Current stock levels
- `GET /api/stock-movements/` - Stock movement history
- `POST /api/stock-movements/transfer/` - Transfer stock
- `POST /api/items/{id}/adjust_stock/` - Adjust stock level

### Locations & Batches
- `GET /api/locations/` - List locations
- `GET /api/batches/` - List batches
- `GET /api/batches/expiring_soon/` - Expiring batches

### Cycle Counting
- `GET /api/cycle-counts/` - List cycle counts
- `POST /api/cycle-counts/{id}/start_count/` - Start count
- `POST /api/cycle-counts/{id}/complete_count/` - Complete count

For complete API documentation, visit: http://localhost:8000/api/docs/

## Database Schema

See [Database Schema Documentation](docs/database-schema.md) for detailed information about the data model.

## System Design

See [System Design Documentation](docs/system-design.md) for architecture overview and design decisions.

## Configuration

### Environment Variables

#### Backend (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://inventory_user:inventory_pass@db:5432/inventory_db
```

#### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
```

## Development

### Backend Development
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Frontend Development
```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

### Running Tests
```bash
# Backend tests
docker-compose exec backend python manage.py test

# Frontend tests
docker-compose exec frontend npm test
```

## Deployment

### Production Setup
1. Update environment variables for production
2. Configure SSL certificates
3. Set up proper database backups
4. Configure monitoring and logging

### Docker Production
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `docs/` directory
- Review the API documentation at `/api/docs/`