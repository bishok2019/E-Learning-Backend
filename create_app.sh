#!/bin/bash

# Ensure the script is executed from the project root
# cd "$(dirname "$0")/.."

# Get app name: either from argument or user input
if [ -z "$1" ]; then
  read -p "Enter the Django app name: " APP_NAME
else
  APP_NAME=$1
fi

# Validate input
if [ -z "$APP_NAME" ]; then
  echo "No app name provided. Exiting."
  exit 1
fi

# Run Django startapp
python manage.py startapp "$APP_NAME"

# Check if startapp succeeded
if [ $? -ne 0 ]; then
  echo "Failed to create the app '$APP_NAME'."
  exit 1
fi

# Ensure 'apps' directory exists
if [ ! -d "apps" ]; then
  mkdir apps
fi

# Move the new app
mv "$APP_NAME" "apps/$APP_NAME"

# Verify move success
if [ $? -eq 0 ]; then
  echo "App '$APP_NAME' has been created and moved to 'apps/$APP_NAME'."
else
  echo "Failed to move the app '$APP_NAME' to 'apps/'."
  exit 1
fi
