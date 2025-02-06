# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port for the app
EXPOSE 5008

# Use Gunicorn as the WSGI server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5008", "main:app"]