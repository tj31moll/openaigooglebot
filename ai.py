import logging
import chatterbot
import time
import telegram
import openai
import custom_words

from telegram import __version__ as TG_VER, ForceReply, Update
from telegram.ext import Updater, MessageHandler, filters, Application, CommandHandler, ContextTypes

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create a new chat bot named 'EchoBot'
chatbot = ChatBot('EchoBot')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Load the english corpus
trainer.train("chatterbot.corpus.english")

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    await update.message.reply_text(response)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("YOUR_BOT_TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(filters=text_filter, callback=echo))

    # Start the Bot
    updater.start_polling
