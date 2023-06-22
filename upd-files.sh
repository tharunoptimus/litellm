#!/bin/bash

printf "Updating Local Files...\n"

printf "Removing the files...\n"
rm -rf ./static
rm index.html
rm service.py

printf "Downloading the latest files...\n"
wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/service.py -O service.py
wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/index.html -O index.html
mkdir static
cd static
wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/static/style.css -O style.css
wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/static/app.js -O app.js
cd ..

printf "Successfully Updated the Local Files with the latest udpate!\n\n"

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

printf "Run python3 service.py to start the service!"
