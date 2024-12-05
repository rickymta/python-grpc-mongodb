# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the necessary libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source code into the container
COPY . /app/

# Set environment variables (depending on the use of .env, you may need to COPY the .env file into the container if needed)
COPY .env.docker /app/.env

# Open port for gRPC server
EXPOSE 50051

# Command to run the application when the container is started
CMD ["python", "main.py"]
