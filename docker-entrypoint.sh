#!/bin/sh

if [ "$1" = "uvicorn" ] || [ "$1" = "" ]; then
    python ./main.py
elif [ "$1" = "worker" ]; then
    python -m dramatiq tasks
else
    python ./main.py "$@"
fi
