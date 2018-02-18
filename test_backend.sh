#!/bin/sh
./backend/pylint.sh && python backend/manage.py test
