# Use official TensorFlow image (includes Python + TensorFlow pre-installed)
FROM tensorflow/tensorflow:2.19.0

# Set working directory
WORKDIR /app

# Copy requirements (excluding tensorflow if it's in there)
COPY requirements.txt .

# Install other dependencies (make sure tensorflow is NOT in this file)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Expose the default FastAPI port
EXPOSE 8000

# Launch the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]