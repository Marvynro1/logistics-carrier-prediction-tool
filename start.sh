#!/bin/bash

# Start the Anvil backend script in the background
echo "Starting Anvil Uplink server..."
python app/main.py &

# Start the JupyterLab server in the foreground
echo "Starting JupyterLab server on http://localhost:8888"
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''