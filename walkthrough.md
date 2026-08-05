# AWS Deployment Guide (Raw IP)

Since you don't have a domain name yet, we will deploy the backend directly to the public IP address of your AWS server. This means your Flutter app will connect via `http://` instead of `https://`.

Please follow these exact steps carefully:

## Step 1: Launch an AWS EC2 Instance
1. Go to your **AWS Console** -> **EC2** -> **Launch Instances**.
2. **Name**: `NexaVoice-Backend`
3. **OS Image**: Select **Ubuntu 24.04 LTS** (or 22.04 LTS).
4. **Instance Type**: Select `t3.small` or `t3.medium` (Voice AI requires slightly more memory than the free tier `t2.micro`).
5. **Key Pair**: Create a new Key Pair (e.g., `nexavoice-key.pem`) and download it.
6. **Network Settings**: 
   - Check **Allow SSH traffic from Anywhere**
   - Check **Allow HTTP traffic from the internet**
7. Click **Launch Instance**.

## Step 2: Open Port 8000
By default, AWS blocks port `8000`. We need to open it.
1. In the EC2 console, click your new instance.
2. Go to the **Security** tab at the bottom and click the Security Group link (e.g., `sg-0abcd1234`).
3. Click **Edit inbound rules**.
4. Click **Add rule**:
   - Type: **Custom TCP**
   - Port range: **8000**
   - Source: **Anywhere-IPv4** (`0.0.0.0/0`)
5. Save the rules.

## Step 3: Copy Code to the Server
You need to copy your `backend` folder to the EC2 server. You can do this by pushing your code to GitHub and cloning it on the server, or using SCP/WinSCP.

If using GitHub (Recommended):
```bash
ssh -i nexavoice-key.pem ubuntu@YOUR_AWS_IP
git clone <your-repo-url>
cd salesforce-ai-calling-agent/backend
```

## Step 4: Run the Setup Script
I have created a script that will automatically install Docker and configure your server. Run this inside the `backend` folder on your EC2 instance:
```bash
# Make the script executable
chmod +x deploy/setup_ec2.sh

# Run the setup script
./deploy/setup_ec2.sh
```

## Step 5: Start the Backend
Once Docker is installed, start your server!
```bash
# Start the containers in the background
sudo docker-compose up -d --build
```
*You can verify it works by visiting `http://YOUR_AWS_IP:8000/docs` in your browser on your laptop.*

## Step 6: Update Flutter App
1. Go back to your VS Code project on your laptop.
2. Open `lib/core/config/app_config.dart`.
3. Change `_awsHost` to your actual AWS Public IPv4 Address.
4. Change `isProduction = true;`.
5. Rebuild your Android APK! Your mobile app is now officially communicating with your AWS Cloud Server.
