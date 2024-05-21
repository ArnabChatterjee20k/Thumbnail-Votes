### Thumbnail service

[] Creating thumbnails
[] Storing it
[] Getting thumbnails

### starting the workers

> here celery_worker is the module name and celery_app is the object
```
celery -A celery_worker.celery_app worker --loglevel INFO -P solo
```
