# Use the official Python image as the base image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first (utilize Docker caching)
COPY requirements.txt /app/

# Install dependencies from requirements.txt (use cache if unchanged)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code (done after dependency installation)
COPY . /app/

# Expose the port on which the app runs (default for Django is 8000)
EXPOSE 8000

# Command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
