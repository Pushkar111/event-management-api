#!/bin/bash
# Setup script for Event Management System
# Run this script to set up the development environment

echo "===================================="
echo "Event Management System Setup"
echo "===================================="
echo

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "Step 2: Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "Step 3: Upgrading pip..."
python -m pip install --upgrade pip

echo "Step 4: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "Step 5: Running migrations..."
python manage.py makemigrations
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to run migrations"
    exit 1
fi

echo
echo "===================================="
echo "Setup completed successfully!"
echo "===================================="
echo
echo "Next steps:"
echo "1. Create a superuser: python manage.py createsuperuser"
echo "2. Run the server: python manage.py runserver"
echo "3. (Optional) Start Celery worker: celery -A event_management worker -l info"
echo "4. (Optional) Start Redis: redis-server"
echo
echo "Access the API at: http://127.0.0.1:8000/api/"
echo "Access admin at: http://127.0.0.1:8000/admin/"
echo
