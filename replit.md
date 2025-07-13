# PT Telkom Indonesia Inventory Management System

## Overview

This is a web-based inventory management system built for PT Telkom Indonesia using Flask (Python) and SQLAlchemy. The application provides comprehensive inventory tracking capabilities including item management, categorization, warehouse operations, and activity logging.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Database**: SQLite (development) with support for PostgreSQL (production via DATABASE_URL environment variable)
- **Forms**: Flask-WTF with WTForms for form handling and validation
- **Session Management**: Flask sessions with configurable secret key

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5 with dark theme
- **Icons**: Font Awesome 6.4.0
- **JavaScript**: Vanilla JavaScript with Bootstrap components
- **Responsive Design**: Mobile-first approach using Bootstrap grid system

### Application Structure
```
├── app.py              # Application factory and configuration
├── main.py             # Application entry point
├── models.py           # Database models and relationships
├── routes.py           # URL routes and view functions
├── forms.py            # Form classes and validation
├── templates/          # HTML templates
└── static/            # CSS, JavaScript, and static assets
```

## Key Components

### Database Models
1. **Category**: Product categories with hierarchical organization
2. **Warehouse**: Storage locations with manager assignments
3. **Item**: Inventory items with stock tracking and pricing
4. **ActivityLog**: System activity tracking and audit trail

### Form Components
- **CategoryForm**: Category creation and editing
- **WarehouseForm**: Warehouse location management
- **ItemForm**: Comprehensive item management with dynamic dropdowns

### Core Features
- Dashboard with key performance indicators
- CRUD operations for all major entities
- Search and filtering capabilities
- Low stock alerts and inventory tracking
- Activity logging for audit purposes

## Data Flow

### Item Management Flow
1. Categories and warehouses must be created first
2. Items are created with required category and warehouse assignments
3. Stock levels are tracked with minimum stock thresholds
4. All operations are logged to the activity log

### Database Relationships
- **One-to-Many**: Category → Items, Warehouse → Items
- **Foreign Keys**: Items reference both category_id and warehouse_id
- **Cascade Deletes**: Deleting categories or warehouses removes associated items

### Form Data Processing
1. WTForms validates input data on the client and server side
2. Dynamic dropdown population from database queries
3. Form submission triggers database operations
4. Success/error messages provided via Flask flash messaging

## External Dependencies

### Python Packages
- **Flask**: Web framework and core functionality
- **Flask-SQLAlchemy**: Database ORM and migrations
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form field validation and rendering
- **Werkzeug**: WSGI utilities and proxy fix middleware

### Frontend Dependencies
- **Bootstrap 5**: UI framework with dark theme support
- **Font Awesome**: Icon library for enhanced UI
- **CDN-hosted assets**: External hosting for faster load times

### Environment Variables
- `SESSION_SECRET`: Flask session encryption key
- `DATABASE_URL`: Database connection string (defaults to SQLite)

## Deployment Strategy

### Development Setup
- SQLite database for local development
- Debug mode enabled via main.py
- Automatic table creation on application startup
- Hot reloading for development efficiency

### Production Considerations
- Environment-based configuration via DATABASE_URL
- ProxyFix middleware for reverse proxy deployments
- Connection pooling with health checks
- Logging configuration for monitoring

### Database Migration Strategy
- SQLAlchemy model-first approach
- Automatic table creation via db.create_all()
- Support for PostgreSQL in production environments
- Foreign key constraints and cascade operations

### Security Features
- CSRF protection via Flask-WTF
- Session-based security with configurable secrets
- Input validation and sanitization
- SQL injection prevention through ORM usage

### Scalability Considerations
- Database connection pooling configured
- Static asset serving via CDN
- Template inheritance for code reusability
- Modular code organization for maintainability