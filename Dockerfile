# Use an official Python image with your desired version
FROM python:3.11.3-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies using pip
RUN python -m pip install -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Set the Flask application entry point
CMD ["flask", "run", "--host=0.0.0.0", "--port=8081"]