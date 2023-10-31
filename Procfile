release: python manage.py migrate --noinput
web: gunicorn app.wsgi --log-file -
web: gunicorn app.wsgi --log-file -
worker: celery -A app worker --beat -S django -l info