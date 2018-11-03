#!/bin/sh
venv/bin/pylint ./backend --rcfile .pylintrc '--msg-template={line}: {msg_id}({symbol}) {msg}'
