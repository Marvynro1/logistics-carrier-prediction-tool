# Stage 1: The Builder
# Use the official miniconda3 image as a builder environment
FROM continuumio/miniconda3:latest AS builder

# Set the working directory
WORKDIR /builder

# Copy the environment file into the container
COPY environment.yml .

# Create the conda environment from the yml file
# This installs all necessary dependencies into a new environment named 'logistics-carrier-prediction-tool'
RUN conda env create -f environment.yml

# ---

# Stage 2: The Final Application Image
# Use a slim Python base image for a smaller final image size
FROM python:3.11-slim

# Set the working directory in the final stage
WORKDIR /app

# Copy the created conda environment from the builder stage to the final image
COPY --from=builder /builder/envs/logistics-carrier-prediction-tool /opt/conda/envs/logistics-carrier-prediction-tool

# Add the conda environment's bin directory to the PATH
ENV PATH /opt/conda/envs/logistics-carrier-prediction-tool/bin:$PATH

# Copy the application-specific files into the container
# This ensures files are placed in /app/models, /app/data, etc.
COPY app/ .
COPY models/ ./models/
COPY data/ ./data/

# Define the command to run the application when the container starts
# The working directory is /app, and your script will be in /app/app/main.py
CMD ["python", "app/main.py"]
