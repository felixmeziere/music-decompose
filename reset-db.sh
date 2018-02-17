#!/bin/bash
pid=$(lsof -i:8000 -t); kill -TERM $pid || kill -KILL $pid
dropdb music-decompose
createdb music-decompose
python backend/manage.py migrate
python backend/manage.py createsuperuser
