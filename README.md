# VALV Logistics Carrier Prediction Tool

This project is a machine learning application designed for a fictitious industrial valve manufacturer (VALV Industries). It takes shipment details (client, destination, dimensions, and weight) as input and provides two key functions:

1.  **Classification**: Classifies the shipment as a "Box," "Pallet," or "Crate."
2.  **Prediction**: Predicts the optimal shipping carrier service based on the inputs and the classified shipment type.

The entire application is containerized with Docker for seamless, one-command reproducibility.

---
## Live Application Link

**https://ddhrgvebw25wfi2b.anvil.app/2HMRG2H6JAF5JQZUOLTYTRIR**

---
## Instructions (Using Docker)

These instructions allow you to run the entire backend application with a single command.

### Prerequisites

* You must have **Docker Desktop** installed and running on your machine. It can be downloaded from the official Docker website.
* Git should be installed, otherwise download the zip file and extract it

### Running the Application

**1. Clone the Repository:**

Open a command prompt or PowerShell and clone this repository to your local machine:
```bash
git clone https://github.com/Marvynro1/logistics-carrier-prediction-tool.git
cd logistics-carrier-prediction-tool
```

## Create the Environment File:
This project requires an Anvil Uplink key to connect the backend to the web UI. You'll have to create an Anvil account if you don't already have one. A template file, **.env.example**, is included in the repository.

First, make a copy of this file and rename the copy to **.env**. You can do this in your file explorer or by running the appropriate command in your terminal:

* **For Windows (Command Prompt or PowerShell):**
```bash
copy .env.example .env
```

* **For macOS or Linux:**
```bash
cp .env.example .env
```

Next, open the new ***.env*** file and replace the placeholder ***enter_you_key_here*** with the actual Anvil Server Uplink key for the project. The file should contain a single line:
```bash
ANVIL_UPLINK_KEY=enter_your_key_here
```

## Build and Run the Container:
Navigate to the project's root directory in your terminal and run the following single command:
```bash
docker-compose up --build
```

This command will:
* Build the Docker image from the **Dockerfile**, installing all necessary dependencies.
* Start the conatiner and run the **main.py** script, which connects to the Anvil service.

You will see log output in your terminal indicating that the models are loading and the conection to the Anvil server is established. The backend is now running and can be accessed via the live Anvil application link provided above. To stop the application, press **Ctrl+C** in the terminal.

## Project Structure

**/app**: Contains the backend Python script (main.py) that runs in the Docker container.

**/data**: Contains the raw shipping-data.csv file.

**/models**: Contains the serialized .joblib files for the trained models and encoders.

**/notebooks**: Contains the Jupyter Notebook for EDA and model development.

**Dockerfile**: Instructions for building the application's Docker image.

**docker-compose.yml**: Simplifies running the Docker container.

**environment.yml**: Defines the reproducible Conda environment.

**.env.example**: A template for the required environment variables.