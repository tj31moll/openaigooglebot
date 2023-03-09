import time
import telegram
from telegram.ext import Updater, MessageHandler, filters, Application
import custom_words
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Set up Telegram bot token
bot_token = "YOUR_BOT_TOKEN"
bot = telegram.Bot(token=bot_token)

# Set up ChatterBot
chatbot = ChatBot('MyBot')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english.greetings', 'chatterbot.corpus.english.conversations')

# Define a function to handle user messages and generate chatbot or Google Assistant responses
def handle_user_message(update, context):
    # Get the user's message text
    text = update.message.text

    # Handle custom words and execute specific tasks or scripts
    if custom_words.handle_custom_words(text):
        return

    # Check if the user wants to use the Google Assistant API
    if text.startswith("ask openai"):
        # Remove the "ask openai" prefix from the message text
        text = text.replace("ask openai", "", 1).strip()

        # Generate a response using OpenAI
        response = chatbot.get_response(text)

        # Send the OpenAI chatbot response back to the user
        update.message.reply_text(response)
    else:
        # The user does not want to use the OpenAI chatbot, generate a response using ChatterBot
        response = chatbot.get_response(text)

        # Send the ChatterBot response back to the user
        update.message.reply_text(response)

# Set up Telegram bot and start polling for user messages
#updater = Updater(bot_token, update_queue=None)
#dispatcher = updater.dispatcher
#dispatcher.add_handler(MessageHandler(filters.text, handle_user_message))
#updater.start_polling()
#updater.idle()
updater = Updater(bot_token, update_queue=None)
#dispatcher = updater.dispatcher
application.add_handler(MessageHandler(filters.Text, handle_user_message))
updater.start_polling()

# Keep the program running until the user presses Ctrl-C to stop it
#updater.start_polling()
while True:
    time.sleep(1)
