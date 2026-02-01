# E-Learning Backend

A comprehensive Django REST Framework backend for an e-learning platform with role-based access control, course management, and progress tracking.



- **API Documentation**
  - Swagger UI at `/docs/`
  - ReDoc at `/docs/redoc/`
  - OpenAPI schema at `/docs/schema/`

## Tech Stack

- **Backend**: Django 6.0.1, Django REST Framework 3.16.1
- **Database**: PostgreSQL 15
- **Authentication**: JWT (djangorestframework-simplejwt)
- **API Documentation**: drf-spectacular
- **Task Queue**: Celery 5.6.2
- **ASGI Server**: Uvicorn 0.40.0
- **Container**: Docker & Docker Compose
- **Package Manager**: uv

## Prerequisites

- **Docker & Docker Compose** (recommended)
- **OR** Python 3.13+, PostgreSQL 15+, and uv package manager

## Quick Start (Docker - Recommended)

### 1. Clone the repository
```bash
git clone git@github.com:bishok2019/E-Learning-Backend.git
cd E-Learning-Backend
```

### 2. Start the application
```bash
docker-compose up --build
```

This will:
- Build the Docker containers
- Set up PostgreSQL database
- Run migrations automatically
- Create a default superuser (email: `admin@example.com`, password: `admin`)
- Start the server at `http://localhost:8000`

### 3. Access the application
- **API Base URL**: `http://localhost:8000/api/v1/`
- **Admin Panel**: `http://localhost:8000/admin/`
- **API Documentation**: `http://localhost:8000/docs/`
- **ReDoc**: `http://localhost:8000/docs/redoc/`

### 4. Stop the application
```bash
docker-compose down
```

To stop and remove all data (including database):
```bash
docker-compose down -v
```

## Manual Setup (Without Docker)

### 1. Clone the repository
```bash
git clone git@github.com:bishok2019/E-Learning-Backend.git
cd E-Learning-Backend
```

### 2. Install uv package manager
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Install dependencies
```bash
uv sync
```

### 4. Set up environment variables
```bash
cp .env_sample .env
# Edit .env with your database credentials
```

Example `.env` file:
```env
DB_NAME=e_learning_db
DB_USER=admin
DB_PASSWORD=admin123
DB_HOST=localhost
DB_PORT=5432
```

### 5. Set up PostgreSQL database
```bash
# Create database (using psql)
psql -U postgres
CREATE DATABASE e_learning_db;
CREATE USER admin WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE e_learning_db TO admin;
\q
```

### 6. Run migrations
```bash
uv run python manage.py migrate
```

### 7. Create superuser
```bash
uv run python manage.py createsuperuser
```

### 8. Run development server
```bash
uv run uvicorn e_learning_backend.asgi:application --host 0.0.0.0 --port 8000 --reload
```

Or using Django's runserver:
```bash
uv run python manage.py runserver
```

