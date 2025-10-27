# 🐳 GDE System - Docker Deployment Guide

## 📋 Overview

This guide provides complete instructions for running the GDE (Gestión de Depósitos y Existencias) system using Docker Compose. The system includes:

- **Backend API**: FastAPI-based REST API
- **Frontend**: Next.js React application
- **Database**: PostgreSQL (optional, can use Supabase)
- **Cache**: Redis (optional)
- **Reverse Proxy**: Nginx (optional)

## 🚀 Quick Start

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd GDE_UNPULSED
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.docker .env

# Edit .env with your actual values
nano .env
```

### 3. Start the System

```bash
# Using the management script (recommended)
./docker-manage.sh start

# Or using docker-compose directly
docker-compose up --build -d
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🛠️ Management Commands

### Using the Management Script

```bash
# Start all services
./docker-manage.sh start

# Stop all services
./docker-manage.sh stop

# Restart all services
./docker-manage.sh restart

# View logs
./docker-manage.sh logs

# Check status
./docker-manage.sh status

# Clean up resources
./docker-manage.sh clean

# Show help
./docker-manage.sh help
```

### Using Docker Compose Directly

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Rebuild and start
docker-compose up --build -d

# Clean up
docker-compose down -v --remove-orphans
```

## 🔧 Configuration

### Environment Variables

The system uses the following key environment variables:

```bash
# Database (Supabase)
DATABASE_URL=postgresql://user:pass@host:port/db
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=GDE Backend API
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://frontend:3000
```

### Service Configuration

#### Backend Service
- **Port**: 8000
- **Health Check**: `/health`
- **Dependencies**: Database, Redis (optional)
- **Volumes**: `uploads/`, `logs/`

#### Frontend Service
- **Port**: 3000
- **Dependencies**: Backend
- **Environment**: Next.js production build

#### Database Service (Optional)
- **Port**: 5432
- **Database**: `gde_db`
- **User**: `gde_user`
- **Password**: `gde_password`

#### Redis Service (Optional)
- **Port**: 6379
- **Purpose**: Caching and session storage

#### Nginx Service (Optional)
- **Port**: 80, 443
- **Purpose**: Reverse proxy and load balancing

## 📊 Monitoring and Health Checks

### Health Check Endpoints

- **Backend**: `GET /health`
- **Frontend**: `GET /` (returns 200 OK)
- **Database**: `pg_isready` command
- **Redis**: `redis-cli ping`

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# With timestamps
docker-compose logs -f -t
```

### Resource Monitoring

```bash
# Container stats
docker stats

# Service status
docker-compose ps

# Health status
./docker-manage.sh status
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Check what's using the port
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :3000

# Kill the process or change ports in docker-compose.yml
```

#### 2. Database Connection Issues

```bash
# Check database logs
docker-compose logs db

# Test database connection
docker-compose exec backend python -c "
from app.core.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('Database connection successful')
"
```

#### 3. Frontend Build Issues

```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build --no-cache frontend
```

#### 4. Environment Variables Not Loading

```bash
# Check if .env file exists
ls -la .env

# Verify environment variables
docker-compose exec backend env | grep DATABASE
```

### Debug Mode

```bash
# Run in debug mode
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up

# Or modify docker-compose.yml to add debug settings
```

## 🚀 Production Deployment

### Security Considerations

1. **Change default passwords**
2. **Use strong SECRET_KEY**
3. **Enable HTTPS with SSL certificates**
4. **Configure firewall rules**
5. **Use environment-specific configurations**

### Performance Optimization

1. **Enable Redis caching**
2. **Configure Nginx reverse proxy**
3. **Use production database**
4. **Optimize Docker images**
5. **Configure resource limits**

### Scaling

```bash
# Scale backend instances
docker-compose up --scale backend=3

# Use load balancer
# Configure Nginx upstream with multiple backend instances
```

## 📁 Project Structure

```
GDE_UNPULSED/
├── docker-compose.yml          # Main Docker Compose file
├── docker-manage.sh           # Management script
├── env.docker                  # Environment template
├── nginx.conf                  # Nginx configuration
├── gde-backend/
│   ├── Dockerfile             # Backend Docker image
│   ├── requirements.txt       # Python dependencies
│   └── app/                   # Backend application
├── gde-frontend/
│   ├── Dockerfile             # Frontend Docker image
│   ├── package.json           # Node.js dependencies
│   └── src/                   # Frontend application
└── docs/                      # Documentation
```

## 🆘 Support

For issues and questions:

1. Check the logs: `./docker-manage.sh logs`
2. Verify configuration: `./docker-manage.sh status`
3. Review this documentation
4. Check the troubleshooting section
5. Create an issue in the repository

## 📝 License

This project is licensed under the MIT License.

