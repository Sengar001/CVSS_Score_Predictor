# Dockerfile

FROM python:3.10

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /app

EXPOSE 8000

# Default command (can be changed in Jenkins)
CMD ["python3", "main.py"]
