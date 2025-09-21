## 🚀 Live Demo

This application has been deployed to a live server for easy access and demonstration.

**You can access the live application here:** https://ddhrgvebw25wfi2b.anvil.app/I6RUPSWSD4AFO3BBKAXT63P7

# VALV Industries - Logistics Carrier Prediction Tool - Capstone Project

## Project Overview

This project is a fully functional data product designed to solve a business problem for an industrial valve manufacturer. It uses descriptive and predictive methods to analyze historical shipping data and predict the optimal shipping carrier for new shipments. The application features a user-friendly dashboard with interactive data visualizations and is powered by a containerized machine learning backend.

This entire project is designed for one-command reproducibility, allowing the user to run both the backend server and the JupyterLab analysis environment with a single script.

---
## How to Run the Project

This project is containerized using Docker and includes a setup script for a seamless, automated setup on Windows.

### Prerequisites

* You must have **Docker Desktop** installed and running on your machine.
* You will need the Anvil Uplink Key that was provided to you.

### Instructions

1.  **Unzip Project Files:**
    Unzip the provided project folder to a location on your computer.

2.  **Run the Setup Script:**
    Double-click the **`run.bat`** file.

3.  **Enter the Anvil Key:**
    A new terminal window will open and prompt you to enter the Anvil Uplink Key. Paste the key you were provided and press **Enter**.

The script will automatically create the necessary configuration file and then build and run the Docker container. This process may take several minutes the first time.

### Accessing the Application and Notebook

Once the backend server is ready, the script will automatically open two tabs in your default web browser.

1.  **Anvil Web App**: The main application interface for making predictions and viewing the dashboard.
2.  **Jupyter Notebook**: The JupyterLab environment for reviewing the data analysis and model training process.

The URLs will also be printed in the terminal for your reference:
* **Anvil Web App:** `https://ddhrgvebw25wfi2b.anvil.app/I6RUPSWSD4AFO3BBKAXT63P7`
* **JupyterLab:** `http://localhost:8888`

To stop the application, simply press `Ctrl+C` in the terminal window that is running the backend server.

---
## Project Structure

* **/app**: Contains the backend Python script (`main.py`) that connects to Anvil.
* **/data**: Contains the raw `shipping-data.csv` file.
* **/models**: Contains the serialized `.joblib` files for the trained models.
* **/notebooks**: Contains the Jupyter Notebook for EDA and model development.
* **/output**: A git-ignored directory designated for any generated files, such as prediction logs or reports.
* **Dockerfile**: Defines the container for the backend and JupyterLab servers.
* **docker-compose.yml**: Manages the Docker container setup.
* **environment.yml**: Defines the reproducible Conda environment for local analysis.
* **start.sh**: The script that runs inside the Docker container to start the services.
* **run.bat** & **monitor.ps1**: The setup scripts for a one-click experience.