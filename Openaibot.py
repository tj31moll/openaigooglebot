import logging
import time
import telegram
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import custom_words

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
# Initialize the chatbot
chatbot = ChatBot("MyBot")
#chatbot.set_trainer(ChatterBotCorpusTrainer)
#chatbot.train("chatterbot.corpus.english.greetings")
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english.greetings",
              "chatterbot.corpus.english.conversations")
# Initialize the OpenAI API
openai.api_key = "YOUR_API_KEY"

# Define a few command handlers. These usually take the two arguments update and context.
def start(update: telegram.Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()}!", reply_markup=telegram.ForceReply(selective=True)
    )

def help_command(update: telegram.Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")



def get_openai_response(user_input):
    """Call OpenAI API and get the response"""
    chat_ml_messages = [{"role": "user", "content": user_input}]
    response = openai.Completion.create(
#        engine="gpt-3.5-turbo",
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": "Tell the world about the ChatGPT API in the style of a pirate."}]
    )
    response_str = response.choices[0].text.strip()
    return response_str

def echo(update: telegram.Update, context: CallbackContext) -> None:
    """Echo the user message."""
    user_input = update.message.text
    # Check if the user input is in the custom words
    if user_input.lower() in custom_words.words:
        response = custom_words.words[user_input.lower()]
    elif user_input.lower() == "ask openai":
        # Get the response from OpenAI API
        response = get_openai_response(user_input)
    else:
        # Pass the user input to ChatterBot
        response = chatbot.get_response(user_input)
        # Generate a response from the 
        response_str = str(response)

    # Send the response back to the user
    update.message.reply_text(response)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non-command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()
    logger.info("Bot started!")
    updater.idle()

if __name__ == "__main__":
    main()
