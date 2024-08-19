#!/bin/bash

# Upgrade pip and install dependencies
pip3 install --upgrade pip
pip3 install --no-cache-dir -r /var/www/html/requirements.txt

# Run the main command (start Apache server)
exec "$@"