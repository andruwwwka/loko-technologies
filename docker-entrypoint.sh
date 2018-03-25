#!/bin/bash

postgres_host=$1
postgres_port=$2

# Wait for the postgres docker to be running
while ! nc $postgres_host $postgres_port; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing command"

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Filling the tables
echo "Filling the tables"
python manage.py filling_the_tables

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
