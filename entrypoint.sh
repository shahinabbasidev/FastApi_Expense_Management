#!/bin/bash
set -e

echo "Starting Expense Management API..."

# Check if database URL is set
if [ -z "$SQLALCHEMY_DATABASE_URL" ]; then
    echo "ERROR: SQLALCHEMY_DATABASE_URL environment variable is not set"
    exit 1
fi

# Wait for database to be ready (if using PostgreSQL with host)
if [[ "$SQLALCHEMY_DATABASE_URL" == postgresql* ]]; then
    echo "Waiting for PostgreSQL database to be ready..."
    DB_HOST=$(echo "$SQLALCHEMY_DATABASE_URL" | sed -n 's/.*@\([^:/]*\).*/\1/p')
    DB_PORT=$(echo "$SQLALCHEMY_DATABASE_URL" | sed -n 's/.*:\([0-9]*\)\/\|.*:\([0-9]*\)$/\2\1/p')
    DB_PORT=${DB_PORT:-5432}
    
    max_attempts=30
    attempt=1
    until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U postgres 2>/dev/null || [ $attempt -eq $max_attempts ]; do
        echo "Waiting for database... (attempt $attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    done
    
    if [ $attempt -eq $max_attempts ]; then
        echo "WARNING: Database did not become ready in time"
    else
        echo "Database is ready!"
    fi
fi

# Run database migrations
echo "Running database migrations..."
if ! alembic upgrade head; then
    echo "WARNING: Database migration failed (may be expected on first run or SQLite)"
else
    echo "Migrations completed successfully"
fi

# Compile translations
echo "Compiling translations..."
if python compile_translations.py; then
    echo "Translations compiled successfully"
else
    echo "WARNING: Translation compilation failed (optional)"
fi

# Start the application with uvicorn
echo "Starting application server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
