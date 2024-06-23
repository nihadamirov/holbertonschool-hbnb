# Stage 1: Base Image
FROM python:3.8-alpine

# Set working directory within the container
WORKDIR /app

# Copy and install requirements first to leverage Docker caching
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port where the Flask app runs
EXPOSE 5000

# Command to run the Flask application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
