#!/bin/sh
./pylint.sh && python backend/manage.py test
