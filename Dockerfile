# Use a specific Python base image
FROM python:3.8.10-slim

# Create a new user to avoid running as root
RUN useradd -m appuser

# Switch to the new user
USER appuser

# Set the working directory
WORKDIR /app

# Copy requirements.txt and upgrade pip
COPY requirements.txt /app/
RUN pip install --upgrade pip  # Upgrade pip to the latest version

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the appropriate port
EXPOSE 80

# Define the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
