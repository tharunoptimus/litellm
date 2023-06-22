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
echo "You will have to download about 400MB during first run..."

echo "Downloading the required files for the app..."
wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/service.py -O service.py
wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/index.html -O index.html
mkdir static
cd static && wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/static/style.css -O style.css
cd static && wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/static/app.js -O app.js

echo "Installation complete. Run `python3 server.py` to start the server"
