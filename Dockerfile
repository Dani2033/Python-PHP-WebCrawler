# Use an official PHP image as a base
FROM php:8.1-apache

# Update package list and install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /var/www/html

# Copy the PHP code into the container
COPY . /var/www/html

# Install Python dependencies globally
# We are using '--break-system-packages' because of some incompatibilities Docker has with Python, 
# this can be also fixed by using a Python virtual environment but since we are using Docker and 
# not storing any kind of data there is no need to overengineer it
RUN pip install --no-cache-dir -r /var/www/html/requirements.txt --break-system-packages

# Expose port 80 for Apache
EXPOSE 80

# Start Apache in the foreground
CMD ["apache2-foreground"]

