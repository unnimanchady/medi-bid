#!/bin/bash
# Fail immediately if any command exits with a non-zero status
set -e

echo "=========================================="
echo "Starting Render Deployment Initialization"
echo "=========================================="

echo "[1/4] Running database migrations (Alembic)..."
flask db upgrade

echo "[2/4] Seeding languages..."
python seed_languages.py

echo "[3/4] Seeding specialties..."
python seed_specialties.py

echo "[4/4] Seeding admin account (if configured)..."
python create_admin.py || true

echo "=========================================="
echo "Initialization successful! Starting web server..."
echo "=========================================="

# Replace the current process with gunicorn
exec gunicorn app:app
