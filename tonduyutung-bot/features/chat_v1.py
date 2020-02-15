from telegram.ext import (MessageHandler, Filters, ConversationHandler,
                            CommandHandler)
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('Ron Obvious')
# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)
# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")

RESPONSE = range(1)

def start_chat_v1(update, context):
    logger.info('Sending start message')
    update.message.reply_text(
        'You are now chatting with an AI\n\n'
        'INFORMATION:\n'
        '- Build based on https://chatterbot.readthedocs.io/ backend\n'
        # English corpus https://github.com/gunthercox/chatterbot-corpus/
        '- Trained using English corpus\n\n'
        'You can chat with me as usual. '
        'Send /quit_chat to stop me.\n\n'
    )
    return RESPONSE

def cancel_chat_v1(update, context):
    logger.info("User {} quitting the conversation.".format(
        update.message.from_user.first_name
    ))
    update.message.reply_text('Goodbye! Talk later')
    return ConversationHandler.END

def chat_v1_response(update, context):
    logger.info('Start /chat_v1')
    text = update.message.text
    logger.info('Input: {}'.format(text))
    response = str(chatbot.get_response(text))
    chat_id = update.message.chat_id
    logger.info('Response: {} , type: {}'.format(response, type(response)))
    context.bot.send_message(chat_id=chat_id, text=response)
    logger.info( 'Reply sent to {}'.format(
        update.message.from_user.first_name
    ))


def set_chat_v1():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('chat_v1', start_chat_v1)],
        states={
            RESPONSE: [MessageHandler(Filters.text, chat_v1_response)]
        },
        fallbacks=[CommandHandler('quit_chat', cancel_chat_v1)]
    )
    return conv_handler
