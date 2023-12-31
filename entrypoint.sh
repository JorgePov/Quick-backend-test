#!/bin/sh

echo "Run Backend"

sleep 3

python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000