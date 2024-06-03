# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install required packages
RUN apt-get update && \
    apt-get install -y wget gnupg curl unzip && \
    rm -rf /var/lib/apt/lists/*


# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the application
CMD [ "pytest", "tests/" ]
