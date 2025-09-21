# Use an official, multi-platform Python image as the base
FROM python:3.11-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install all dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Make the startup script executable
RUN chmod +x start.sh

# Expose the port for JupyterLab
EXPOSE 8888

# Set the command to run when the container starts
CMD ["./start.sh"]