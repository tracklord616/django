web: gunicorn InDjango.wsgi --log-file -
worker: celery worker -A InDjango --beat -l info --pool=solo
