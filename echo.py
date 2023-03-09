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

# Initialize the chatbot
chatbot = ChatBot("MyBot")
chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.train("chatterbot.corpus.english.greetings")

def echo(update: telegram.Update, context: CallbackContext) -> None:
    """Echo the user message."""
    user_input = update.message.text
    # Check if the user input is in the custom words
    if user_input.lower() in custom_words.words:
        response = custom_words.words[user_input.lower()]
    elif user_input.lower() == "ask openai":
        # Call OpenAI API and get the response
        openai.api_key = "YOUR_API_KEY"
        response = openai.Completion.create(
            engine="davinci",
            prompt="Hello, I am a bot. " + user_input,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response = response.choices[0].text.strip()
    else:
        # Pass the user input to ChatterBot
        response = chatbot.get_response(user_input)
        # Generate a response from the bot
        response_str = str(response)

    # Send the response back to the user
    update.message.reply_text(response_str)

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
