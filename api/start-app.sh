#!/bin/sh

# Ensure database schema is created.
python manage.py init-db

# Import/update master data.
python manage.py update-master

# Invoke gunicorn with our configuration.
gunicorn -c gunicorn.conf.py main:app