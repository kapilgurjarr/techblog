# Use an official Python runtime as a parent image
FROM python:3.8.10-slim

# Create a non-root user to run the application
RUN useradd -m appuser
USER appuser

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code
COPY . /app

# Expose the port for external access
EXPOSE 80

# Define environment variables (you can add more as needed)
ENV NAME World

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"] 
