#!/bin/sh
set -e

python manage.py migrate
python manage.py runserver 0.0.0.0:3000 --noreload
