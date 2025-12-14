FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Download YOLOv8 model if not present
RUN python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')" || true

# Expose port
EXPOSE 5000

# Run the service
CMD ["python", "inference.py"]
