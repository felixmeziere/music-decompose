#!/bin/sh
BACKEND_FILES="$(git diff origin/master...$(git symbolic-ref --short -q HEAD) --name-only --diff-filter=ACMRT backend)"
FRONTEND_FILES="$(git diff origin/master...$(git symbolic-ref --short -q HEAD) --name-only --diff-filter=ACMRT frontend)"

if [ ! -z ${BACKEND_FILES} ]
then
    echo "Detected changes to the backend. Running backend tests"
    ./test_backend.sh
fi

if [ ! -z ${FRONTEND_FILES} ]
then
    echo "Detected changed to the frontend. Running frontend tests"
    ./test_frontend.sh
fi
