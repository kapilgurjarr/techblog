# Use a specific Python base image
FROM python:3.8-slim

# Create a non-root user for security
RUN useradd -m appuser

# Switch to the created user
USER appuser

# Set the working directory
WORKDIR /app

# Copy requirements and upgrade pip
COPY requirements.txt /app/
RUN /usr/local/bin/python -m pip install --upgrade pip  # Explicit path to avoid path issues

# Install requirements and handle taggit version issues
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the appropriate port for the server
EXPOSE 80

# Define the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
