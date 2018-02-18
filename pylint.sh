#!/bin/sh
pylint ./backend '--msg-template={line}: {msg_id}({symbol}) {msg}'
