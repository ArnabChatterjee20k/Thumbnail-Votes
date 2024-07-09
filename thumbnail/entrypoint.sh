#!/bin/bash

# Start Celery worker
celery -A celery_worker.celery_app worker --loglevel INFO -P solo &

# Start Flower
celery -A celery_worker.celery_app flower &

# Execute the command passed to the script
exec "$@"