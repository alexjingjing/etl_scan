# etl_scan
etl_scan

## To Start
celery -A app.tasks.scan worker --beat -s /home/siming.liu/var/run/celerybeat-schedule -l info
