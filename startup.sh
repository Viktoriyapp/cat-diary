#!/bin/sh
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn cat_diary.wsgi --bind=0.0.0.0 --timeout 600