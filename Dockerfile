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

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies (FORCE fresh install)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN python -m venv data/admin/gnn/venv && \
    data/admin/gnn/venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu

# DEBUG (remove later)
RUN pip list

# Copy rest of code
COPY . .

# Start app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
