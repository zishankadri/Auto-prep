#!/bin/bash

# Apply migrations at runtime
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Start the Gunicorn server
exec gunicorn project.wsgi --timeout 300
