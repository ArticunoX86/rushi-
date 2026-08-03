#!/bin/bash
# NexaVoice Raw IP EC2 Setup Script
# Run this on your Ubuntu EC2 instance to install Docker and start the backend.

echo "========================================="
echo " Starting NexaVoice EC2 Setup..."
echo "========================================="

# 1. Update the system
echo "Updating packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

# 2. Install Docker
echo "Installing Docker..."
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# 3. Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Add current user to Docker group (optional, prevents needing sudo for docker commands)
sudo usermod -aG docker $USER

echo "========================================="
echo " Setup Complete!"
echo "========================================="
echo "To start your backend, navigate to the backend folder and run:"
echo "sudo docker-compose up -d --build"
