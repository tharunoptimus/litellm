#!/bin/bash

printf "Downloading Python and other dependencies for setting the environment...\n"
apt-get install wget python3 python3-venv -y

printf "Creating the environment...\n"
python3 -m venv litellm
source litellm/bin/activate

printf "Downloading and installing libraries for running the models...\n\n"
pip install torch
pip install transformers
pip install sentencepiece
pip install fastapi
pip install uvicorn

printf "Downloading the source for the server...\n"
printf "You will have to download about 400MB during first run...\n"

echo "Downloading the required files for the app..."
wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/service.py -O service.py
wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/index.html -O index.html
wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/upd-files.sh -O upd-files.sh
mkdir static
cd static 
wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/static/style.css -O style.css
wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/static/app.js -O app.js

printf "\n"
printf "\n"
printf " _      _  _          _      _     ___  ___\n"
printf "| |    (_)| |        | |    | |    |  \/  |\n"
printf "| |     _ | |_   ___ | |    | |    | .  . |\n"
printf "| |    | || __| / _ \| |    | |    | |\/| |\n"
printf "| |____| || |_ |  __/| |____| |____| |  | |\n"
printf "\_____/|_| \__| \___|\_____/\_____/\_|  |_/\n"
printf "\n                                           "
printf "\n"

printf "Installation complete. Run `python3 service.py` to start the service"
