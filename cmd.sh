#!/bin/bash

set -e

if [ "$env" = 'dev' ]; then
  echo "Running Dev server"
  exec python3 identydock.py
else
  echo "Running Prod server"
  exec uwsgi --http 0.0.0.0:9090 --wsgi-file /app/identydock.py --callable app --stats 0.0.0.0:9191
fi
