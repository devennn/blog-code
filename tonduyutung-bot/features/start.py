import logging

def start(update, context):
    logging.info('Starting feature == /start')
    logging.info('Sending Start Message')
    features_list = '{}'.format(
        'Reply the command below to start\n'
        '\n'
        '=== Explore Project ===\n'
        'Simple AI Conversation Bot --> /chat_v1\n'
    )
    update.message.reply_text(text=features_list)
