# 1. Use Python 3.11 slim to match your local environment
FROM python:3.11-slim

# 2. Install system dependencies
# Pillow needs: libjpeg-dev, zlib1g-dev, libpng-dev, gcc
# Tesseract needs: tesseract-ocr, libtesseract-dev
RUN apt-get update && \
    apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    gcc \
    g++ \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3. Copy requirements
COPY requirements.txt .

# 4. CRITICAL: Upgrade pip
# This ensures pip can find the pre-compiled "wheels" for Python 3.11
RUN pip install --upgrade pip

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the application code
COPY . .

# 7. Expose the port
EXPOSE 10000

# 8. Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]