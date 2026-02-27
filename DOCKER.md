# Docker Setup Guide

## Overview

This project includes Docker configurations for both development and production environments.

## Available Dockerfiles

### Development: `Dockerfile.dev`

- Single-stage build for faster iteration
- Includes dev dependencies
- Usage: `docker build -f Dockerfile.dev -t expense-api:dev .`

### Staging: `Dockerfile.stage`

- Single-stage build optimized for staging
- Uses `fastapi run` command
- Usage: `docker build -f Dockerfile.stage -t expense-api:stage .`

### Production: `Dockerfile.prod`

- **Multi-stage build** for optimized final image
- Minimal runtime dependencies
- Non-root user execution for security
- Health checks included
- Uses uvicorn with multiple workers
- Usage: `docker build -f Dockerfile.prod -t expense-api:prod .`

## Production Docker Build

The `Dockerfile.prod` uses a multi-stage approach:

### Stage 1: Builder

- Installs build tools and compiles Python dependencies
- Creates a Python virtual environment with all packages
- Discarded after dependencies are built (smaller final image)

### Stage 2: Runtime

- Uses a clean `python:3.13-slim` base image
- Copies only the virtual environment from builder
- Adds minimal runtime dependencies (PostgreSQL client, curl)
- Creates non-root `appuser` for security
- Includes health check endpoint

## Entrypoint Script

The `entrypoint.sh` script handles:

1. **Database Readiness Check** (PostgreSQL)
   - Waits for PostgreSQL to be ready before continuing
   - Configurable timeout (30 attempts, 2s interval)

2. **Database Migrations**
   - Runs `alembic upgrade head` to apply pending migrations
   - Safe to run multiple times (idempotent)

3. **Translation Compilation**
   - Compiles `.po` files to `.mo` for gettext
   - Optional (warnings if it fails)

4. **Application Startup**
   - Starts uvicorn with 4 workers
   - Production-ready ASGI server

## Running with Docker Compose (Production)

### Setup Environment

Create a `.env` file:

```env
POSTGRES_DB=expense_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password_here
JWT_SECRET_KEY=your-very-secure-secret-key-here
SENTRY_DSN=https://your-sentry-dsn-here (optional)
```

### Start Services

```bash
# Build and start all services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f api

# Stop services
docker-compose -f docker-compose.prod.yml down
```

### Services Included

- **PostgreSQL 16** (postgres:16-alpine)
  - Port: 5432
  - Volume: `postgres_data` (persistent storage)

- **Redis 7** (redis:7-alpine)
  - Port: 6379
  - For caching and session management

- **API** (expense_api:prod)
  - Port: 8000
  - Uvicorn with 4 workers
  - Automatic migration and startup

## Building the Production Image

```bash
# Build the image
docker build -f Dockerfile.prod -t expense-api:prod .

# Run the container
docker run -d \
  --name expense-api \
  -e SQLALCHEMY_DATABASE_URL="postgresql://user:pass@localhost/dbname" \
  -e REDIS_URL="redis://localhost:6379" \
  -e JWT_SECRET_KEY="your-secret-key" \
  -p 8000:8000 \
  --health-cmd='curl -f http://localhost:8000/is-ready || exit 1' \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  expense-api:prod
```

## Best Practices

1. **Environment Variables**: Always use `.env` files or secret management for sensitive data
2. **Health Checks**: The API exposes a `/is-ready` endpoint for health monitoring
3. **Non-Root User**: The application runs as `appuser` (UID 1000) for security
4. **Image Size**: Multi-stage reduces image size from ~1.2GB to ~800MB
5. **Database**: Always use PostgreSQL in production (not SQLite)
6. **Workers**: Adjusted to 4 workers; modify in `entrypoint.sh` based on CPU cores

## Troubleshooting

### Database Connection Failed

```bash
# Check PostgreSQL is running
docker-compose -f docker-compose.prod.yml logs postgres

# Check network connectivity
docker network inspect <network_name>
```

### Migrations Failed

```bash
# Check Alembic status
docker exec expense_api alembic current
docker exec expense_api alembic history
```

### Permission Issues

```bash
# Fix file permissions
sudo chown -R $(id -u):$(id -g) .
```

## Production Checklist

- [ ] Change `JWT_SECRET_KEY` to a strong random value
- [ ] Set up proper `SENTRY_DSN` for error tracking
- [ ] Configure PostgreSQL with strong password
- [ ] Enable SSL/TLS for Redis
- [ ] Use a reverse proxy (nginx, Caddy) in front of the API
- [ ] Set up persistent volumes for database
- [ ] Configure resource limits in docker-compose
- [ ] Set up log aggregation
- [ ] Monitor health check endpoint
