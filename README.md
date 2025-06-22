# Organization Management System

A comprehensive FastAPI-based system for managing organizations with dynamic database creation, JWT authentication, and Docker support.

## Features

- **Dynamic Database Creation**: Each organization gets its own isolated database
- **JWT Authentication**: Secure admin login with token-based authentication
- **RESTful APIs**: Clean and well-documented API endpoints
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **PostgreSQL**: Robust database backend with master and organization-specific databases

## API Endpoints

### 1. Create Organization
- **Endpoint**: `POST /org/create`
- **Payload**: 
  ```json
  {
    "email": "admin@example.com",
    "password": "securepassword",
    "organization_name": "Example Corp"
  }
  ```
- **Response**: Organization details with database information

### 2. Get Organization
- **Endpoint**: `GET /org/get?organization_name=Example Corp`
- **Response**: Organization details

### 3. Admin Login
- **Endpoint**: `POST /admin/login`
- **Payload**:
  ```json
  {
    "email": "admin@example.com",
    "password": "securepassword"
  }
  ```
- **Response**: JWT token for authentication

### 4. Get Current Admin
- **Endpoint**: `GET /admin/me`
- **Headers**: `Authorization: Bearer <jwt_token>`
- **Response**: Current admin information

## Project Structure

```
organization_management/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connections
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── crud.py              # CRUD operations
│   └── routers/
│       ├── __init__.py
│       ├── organization.py  # Organization endpoints
│       └── auth.py          # Authentication endpoints
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── env.example             # Environment variables example
└── README.md               # This file
```

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd organization_management
   ```

2. **Start the services**:
   ```bash
   docker-compose up -d
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Manual Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL**:
   - Install PostgreSQL
   - Create a database named `master_db`
   - Update environment variables in `env.example`

3. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Environment Variables

Copy `env.example` to `.env` and configure:

- `MASTER_DB_URL`: Master database connection string
- `ORG_DB_HOST`: Organization database host
- `ORG_DB_PORT`: Organization database port
- `ORG_DB_USER`: Database user
- `ORG_DB_PASSWORD`: Database password
- `SECRET_KEY`: JWT secret key (change in production)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Database Architecture

### Master Database
- `organizations`: Stores organization information
- `admin_users`: Stores admin user credentials

### Organization Databases
- Each organization gets a separate database named `org_<organization_name>`
- Contains organization-specific tables and data
- Isolated from other organizations

## Security Features

- **Password Hashing**: BCrypt for secure password storage
- **JWT Tokens**: Secure authentication with expiration
- **Database Isolation**: Each organization has its own database
- **Input Validation**: Pydantic schemas for request validation

## Development

### Running Tests
```bash
# Add test dependencies and run tests
pytest
```

### Code Formatting
```bash
# Format code with black
black app/
```

### Type Checking
```bash
# Check types with mypy
mypy app/
```

## Production Deployment

1. **Update environment variables** with production values
2. **Use a proper secret key** for JWT tokens
3. **Configure CORS** properly for your domain
4. **Set up SSL/TLS** for HTTPS
5. **Use a production database** with proper backups
6. **Monitor logs** and set up alerting

## API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
