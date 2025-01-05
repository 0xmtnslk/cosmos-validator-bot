# Cosmos Validator Bot

## Installation

1. Clone the repository:
```bash
cd /root
git clone https://github.com/0xmtnslk/cosmos-validator-bot.git
cd cosmos-validator-bot
```

2. Configure bot token:
```bash
# Edit config.json and add your Telegram bot token
nano config.json
```

3. Run setup script:
```bash
chmod +x setup.sh
./setup.sh
```

4. Start services:
```bash
systemctl daemon-reload
systemctl enable tenderduty
systemctl start tenderduty
python3 bot.py
```

## Usage

1. Start chat with your bot on Telegram
2. Use /start to begin
3. Add validators using the bot commands
4. Monitor your validators through Telegram notifications
