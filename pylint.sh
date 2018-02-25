#!/bin/sh
pylint ./backend --rcfile ./backend/pylintrc '--msg-template={line}: {msg_id}({symbol}) {msg}'
