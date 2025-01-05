#!/bin/bash

# Sistem güncellemesi
sudo apt update && sudo apt upgrade -y

# Python ve pip kurulumu
sudo apt install python3 python3-pip -y

# Python bağımlılıklarını yükle
pip3 install python-telegram-bot pyyaml

# Tenderduty kurulumu
sudo apt install golang-go -y

# Tenderduty kullanıcısı oluştur
sudo addgroup --system tenderduty 
sudo adduser --ingroup tenderduty --system --home /var/lib/tenderduty tenderduty

# Tenderduty'yi kur
sudo -u tenderduty bash << EOF
cd /var/lib/tenderduty
echo 'export PATH=\$PATH:/var/lib/tenderduty/go/bin' >> .bashrc
source .bashrc
git clone https://github.com/blockpane/tenderduty
cd tenderduty
go install
EOF

# Tenderduty servis dosyası
sudo tee /etc/systemd/system/tenderduty.service << EOF
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

# Servis ayarları
sudo systemctl daemon-reload
sudo systemctl enable tenderduty

echo "Kurulum tamamlandı!"
