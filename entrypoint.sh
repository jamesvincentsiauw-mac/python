#!/bin/bash

# Check if the argument is "/var/run/dev-test/sock"
if [ "$1" = "/var/run/dev-test/sock" ]; then
    # Run the server.py script with the socket file path
    python /app/server.py "$1"
else
    # Run the grading script
    python /app/client.py
fi
