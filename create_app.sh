#!/usr/bin/env bash
set -e

APP_NAME="$1"

if [ "$#" -ne 1 ] || [ -z "$APP_NAME" ]; then
  echo "Usage: make app <app_name> (single word, no spaces)"
  exit 1
fi

if [ -d "apps/$APP_NAME" ]; then
  echo "Error: apps/$APP_NAME already exists"
  exit 1
fi

mkdir -p "apps/$APP_NAME"
touch "apps/$APP_NAME/__init__.py"
touch "apps/$APP_NAME/models.py"
touch "apps/$APP_NAME/schemas.py"
touch "apps/$APP_NAME/route.py"
touch "apps/$APP_NAME/utils.py"

echo "Created FastAPI app: apps/$APP_NAME"