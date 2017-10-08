#!/bin/sh
cd frontend && eslint . && yarn test && cd..