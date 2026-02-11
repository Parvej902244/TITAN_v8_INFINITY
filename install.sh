#!/bin/bash
echo "🚀 INITIALIZING TITAN_v8∞∞ (INFINITE LOGIC HUNTER)..."

# 1. System Dependencies
echo "📦 Installing System Libraries..."
sudo apt update && sudo apt install -y python3-pip python3-venv curl jq git libpcap-dev

# 2. Python Environment
echo "🐍 Setting up Python Environment..."
python3 -m venv venv
source venv/bin/activate

# 3. Install Python Libs
echo "📚 Installing Python Dependencies..."
pip install -r requirements.txt

# 4. Install Passive Tools (Safe Mode)
echo "🛠️ Installing Safe Passive Tools..."
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/katana/cmd/katana@latest
go install -v github.com/lc/gau/v2/cmd/gau@latest

# 5. Make CLI Executable
echo "🔨 Building CLI..."
chmod +x titan
echo "✅ Setup Complete. Activate venv: 'source venv/bin/activate'"
echo "🚀 Run: ./titan scan https://target.com"
