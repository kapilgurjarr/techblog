# Use a specific Python base image
FROM python:3.8-slim

# Create a non-root user for security
RUN useradd -m appuser

# Switch to the non-root user
USER appuser

# Set the working directory
WORKDIR /app

# Add the user-specific binary path to PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy the requirements file
COPY requirements.txt /app/

# Upgrade pip to avoid outdated issues
RUN /usr/local/bin/python -m pip install --upgrade pip  # Explicit path to ensure correct pip installation

# Install the Python dependencies
RUN /usr/local/bin/python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port the application will use
EXPOSE 9075

# Define the command to start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:9075"]
