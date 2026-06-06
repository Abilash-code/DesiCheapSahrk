# Start with Microsoft's official Playwright environment for Python
FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

# Create a folder inside the container for your project files
WORKDIR /app

# Upgrade pip to ensure smooth dependency installation
RUN pip install --no-cache-dir --upgrade pip

# Copy your requirements file and install python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files into the container
COPY . .

# Run Uvicorn to keep your FastAPI app listening for incoming requests permanently.
# Replace 'main' with your actual Python filename if it is named something else (e.g., app:app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]