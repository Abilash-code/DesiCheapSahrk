# Start with Microsoft's official Playwright environment for Python
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

# Create a folder inside the container for your project files
WORKDIR /app

# Copy your requirements file and install python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files into the container
COPY . .

# Tell the container how to start your app (change 'main.py' to your main file)
CMD ["python", "main.py"]