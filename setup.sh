#!/bin/bash

# System updates
apt update && apt upgrade -y
apt install python3 python3-pip golang-go -y

# Install Python dependencies
pip3 install python-telegram-bot pyyaml

# Create tenderduty user
addgroup --system tenderduty 
adduser --ingroup tenderduty --system --home /var/lib/tenderduty tenderduty

# Install tenderduty
sudo -u tenderduty bash << EOF
cd /var/lib/tenderduty
export GOPATH=/var/lib/tenderduty/go
export PATH=$PATH:$GOPATH/bin
git clone https://github.com/blockpane/tenderduty
cd tenderduty
go install
EOF

# Create service file
cat > /etc/systemd/system/tenderduty.service << EOF
[Unit]
Description=Tenderduty
After=network.target

[Service]
Type=simple
User=tenderduty
WorkingDirectory=/root/cosmos-validator-bot
ExecStart=/var/lib/tenderduty/go/bin/tenderduty -f /root/cosmos-validator-bot/tenderduty/config.yml
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Set permissions
chown -R tenderduty:tenderduty /root/cosmos-validator-bot
chmod -R 755 /root/cosmos-validator-bot
chmod 644 /root/cosmos-validator-bot/tenderduty/config.yml
chmod 644 /root/cosmos-validator-bot/config.json
chmod 644 /root/cosmos-validator-bot/networks.json
chmod 644 /root/cosmos-validator-bot/users.json
