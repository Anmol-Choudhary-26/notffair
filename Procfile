release: python manage.py makemigrations && python manage.py migrate --run-syncdb
web: gunicorn hillfair22_backend.wsgi