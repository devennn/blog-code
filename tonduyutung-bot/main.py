from telegram.ext import Updater, CommandHandler
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from features import *

def get_token():
    with open('token.txt', 'r') as f:
        token = f.read()
        token = token.strip('\n')
    return token

def main():
    # Get token and start program
    token = get_token()
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Add Feature handler
    dp.add_handler(CommandHandler('start', start))
    conv_handler_chat1 = set_chat_v1()
    dp.add_handler(conv_handler_chat1)

    # Polling and Idle
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
