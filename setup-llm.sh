#!/bin/bash

echo "Downloading Python and other dependencies for setting the environment..."
apt-get install wget python3 python3-venv -y

echo "Creating the environment..."
python3 -m venv litellm
source litellm/bin/activate

echo "Downloading and installing libraries for running the models"
pip install torch
pip install transformers
pip install sentencepiece
pip install fastapi
pip install uvicorn

echo "Downloading the source for the server..."
echo "You will have to download about 400MB during setting up the model"

wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/server.py -o server.py
echo "Installation complete. Run `python3 server.py` to start the server"
