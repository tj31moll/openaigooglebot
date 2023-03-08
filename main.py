import telegram
from telegram.ext import Updater, MessageHandler, Filters
import custom_words
from openai_integration import get_chatbot_response
from google_assistant import get_assistant_response

# Set up Telegram bot token
bot_token = "YOUR_BOT_TOKEN"
bot = telegram.Bot(token=bot_token)

# Define a function to handle user messages and generate chatbot or Google Assistant responses
def handle_user_message(update, context):
    # Get the user's message text
    text = update.message.text

    # Handle custom words and execute specific tasks or scripts
    custom_words.handle_custom_words(text)

    # Check if the user wants to use the Google Assistant API
    if text.startswith("OpenAI"):
        # Remove the "ask google" prefix from the message text
        text = text.replace("OpenAI", "", 1).strip()

        # The user does not want to use the Google Assistant API, generate a response using GPT-3
        response = get_chatbot_response(text)

        # Send the chatbot response back to the user
        update.message.reply_text(response)
    else:
        # Generate a response using the Google Assistant API
        response = get_assistant_response(text)

        # Send the Google Assistant response back to the user
        update.message.reply_text(response)
        
        
# Set up Telegram bot and start polling for user messages
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, handle_user_message))
updater.start_polling()
updater.idle()
