#!/bin/bash

# Check if FFmpeg is installed
if ! type "ffmpeg" > /dev/null; then
  # Install FFmpeg
  echo "FFmpeg not found. Installing."
  # Depending on your system you might need to use different commands
  apt-get update -y
  apt-get install ffmpeg -y
else
  echo "FFmpeg already installed."
fi

# Start your web app
echo "Starting Flask app..."
# The following line assumes gunicorn is in your requirements.txt and will be installed
gunicorn --bind=0.0.0.0 --timeout 600 app:app
