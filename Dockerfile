# Use Python base image
FROM python:3.11-slim

# Install system dependencies (needed for geopandas, gdal etc.)
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Set working directory
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Upgrade pip + install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy rest of code
COPY . .

# Start app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
