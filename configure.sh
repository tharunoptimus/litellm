pkg upgrade
pkg i wget proot git -y
cd ~
git clone https://github.com/MFDGaming/ubuntu-in-termux.git
cd ubuntu-in-termux
chmod +x ubuntu.sh
./ubuntu.sh -y
./startubuntu.sh
apt update
apt install wget
wget https://raw.githubusercontent.com/tharunoptimus/litellm/main/setup.sh -o setup.sh
chmod +x setup-llm.sh
./setup-llm.sh
