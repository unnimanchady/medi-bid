#!/bin/bash
# Fail immediately if any command exits with a non-zero status
set -e

echo "=========================================="
echo "Starting Render Deployment Initialization"
echo "=========================================="

echo "[1/3] Running database migrations (Alembic)..."
flask db upgrade

echo "[2/3] Seeding languages..."
python seed_languages.py

echo "[3/3] Seeding specialties..."
python seed_specialties.py

echo "=========================================="
echo "Initialization successful! Starting web server..."
echo "=========================================="

# Replace the current process with gunicorn
exec gunicorn app:app
