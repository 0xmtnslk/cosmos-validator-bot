from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from bot.validator_utils import validate_validator_address, sanitize_input, restart_tenderduty
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import json
import yaml
import os
from datetime import datetime

class ConfigManager:
    def __init__(self):
        self.tenderduty_config_path = 'tenderduty/config.yml'

        # Load basic configs first
        self.load_basic_configs()

        # Create tenderduty directory
        os.makedirs('tenderduty', exist_ok=True)

        # Load or create tenderduty config
        self.load_or_create_tenderduty_config()

    def load_basic_configs(self):
        # Load networks
        with open('networks.json', 'r') as f:
            self.networks = json.load(f)

        # Load bot config
        with open('config.json', 'r') as f:
            self.config = json.load(f)

        # Load or create users
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
            self.save_users()

    def load_or_create_tenderduty_config(self):
        if os.path.exists(self.tenderduty_config_path):
            with open(self.tenderduty_config_path, 'r') as f:
                self.tenderduty_config = yaml.safe_load(f)
        else:
            self.tenderduty_config = {
                'enable_dashboard': True,
                'listen_port': 8888,
                'hide_logs': True,
                'node_down_alert_minutes': 3,
                'prometheus_enabled': True,
                'prometheus_listen_port': 28686,
                'telegram': {
                    'enabled': True,
                    'api_key': self.config['telegram_bot_token']
                },
                'chains': {}
            }
            self.save_tenderduty_config()

    def load_configs(self):
        # Load networks
        with open('networks.json', 'r') as f:
            self.networks = json.load(f)

        # Load bot config
        with open('config.json', 'r') as f:
            self.config = json.load(f)

        # Load or create users
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
            self.save_users()

        # Load or create tenderduty config
        self.load_tenderduty_config()

    def load_tenderduty_config(self):
        if os.path.exists(self.tenderduty_config_path):
            with open(self.tenderduty_config_path, 'r') as f:
                self.tenderduty_config = yaml.safe_load(f)
        else:
            self.tenderduty_config = {
                'enable_dashboard': True,
                'listen_port': 8888,
                'hide_logs': True,
                'node_down_alert_minutes': 3,
                'prometheus_enabled': True,
                'prometheus_listen_port': 28686,
                'telegram': {
                    'enabled': True,
                    'api_key': self.config['telegram_bot_token']
                },
                'chains': {}
            }
            self.save_tenderduty_config()

    def save_users(self):
        with open('users.json', 'w') as f:
            json.dump(self.users, f, indent=4)

    def save_tenderduty_config(self):
        os.makedirs(os.path.dirname(self.tenderduty_config_path), exist_ok=True)
        with open(self.tenderduty_config_path, 'w') as f:
            yaml.dump(self.tenderduty_config, f, default_flow_style=False)

    def add_validator(self, user_id, network, validator_address):
        if not self.tenderduty_config:
            self.load_or_create_tenderduty_config()
            
        if network not in self.tenderduty_config['chains']:
            self.tenderduty_config['chains'][network] = self.get_network_config(network)
        
        self.tenderduty_config['chains'][network]['validators'][str(user_id)] = {
            'address': validator_address,
            'telegram_chat_id': str(user_id)
        }
        self.save_tenderduty_config()

class TelegramBot:
    def __init__(self):
        self.config_manager = ConfigManager()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("Mainnet", callback_data='select_mainnet'),
             InlineKeyboardButton("Testnet", callback_data='select_testnet')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            'Hoş geldiniz! Lütfen validator eklemek istediğiniz ağ tipini seçin:',
            reply_markup=reply_markup
        )

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        if query.data.startswith('select_'):
            network_type = query.data.replace('select_', '')
            networks = self.config_manager.networks[network_type]

            keyboard = []
            for network in networks:
                keyboard.append([InlineKeyboardButton(
                    networks[network]['name'],
                    callback_data=f'network_{network}'
                )])

            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                'Lütfen ağı seçin:',
                reply_markup=reply_markup
            )

        elif query.data.startswith('network_'):
            selected_network = query.data.replace('network_', '')
            context.user_data['selected_network'] = selected_network
            await query.edit_message_text(
                f'Seçilen ağ: {selected_network}\n\n'
                f'Lütfen validator adresinizi girin:'
            )
            context.user_data['waiting_for_address'] = True

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data.get('waiting_for_address'):
            validator_address = update.message.text
            network = context.user_data['selected_network']
            user_id = update.effective_user.id

            # Validator'ü ekle
            self.config_manager.add_validator(user_id, network, validator_address)

            await update.message.reply_text(
                f'✅ Validator başarıyla eklendi!\n\n'
                f'Ağ: {network}\n'
                f'Adres: {validator_address}\n\n'
                f'Block kaçırma durumunda size bildirim gönderilecektir.'
            )
            context.user_data['waiting_for_address'] = False

    def run(self):
        app = Application.builder().token(
            self.config_manager.config['telegram_bot_token']
        ).build()

        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CallbackQueryHandler(self.button))
        app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handle_text
        ))

        app.run_polling()

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
