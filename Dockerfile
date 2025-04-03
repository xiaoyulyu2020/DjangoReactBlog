FROM python:3.10-alpine

# Ensure Python output is displayed in real-time
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    mariadb-connector-c-dev \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    pkgconfig \
    mariadb-client \
    build-base \
    rabbitmq-c-dev  # Required for RabbitMQ support

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application files
COPY . /app

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
