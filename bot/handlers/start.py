import requests
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from bot.config import API_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# состояние диалога
ENTER_NAME = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    logger.info(f"Checking user with telegram_id {telegram_id}")

    try:
        response = requests.post(
            f"{API_URL}/user",
            json={'telegram_id': telegram_id}
        )

        logger.info(f"Response status: {response.status_code}, content: {response.text}")

        if response.status_code == 409:
            await update.message.reply_text("You're already registered!")
            return ConversationHandler.END
        elif response.status_code == 201:
            await update.message.reply_text("Please enter your name:")
            return ENTER_NAME
        else:
            await update.message.reply_text(
                f"Something went wrong. Status code: {response.status_code}, Error: {response.text}"
            )
            return ConversationHandler.END

    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        await update.message.reply_text("Failed to connect to the server.")
        return ConversationHandler.END


async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    username = update.message.text.strip()

    logger.info(f"Received name '{username}' for telegram_id {telegram_id}")

    if not username:
        await update.message.reply_text("Name cannot be empty. Please enter your name again:")
        return ENTER_NAME

    try:
        response = requests.post(
            f"{API_URL}/user",
            json={'telegram_id': telegram_id, 'username': username}
        )

        logger.info(f"Response status: {response.status_code}, content: {response.text}")

        if response.status_code == 201:
            await update.message.reply_text("Welcome! You've been registered.")
        elif response.status_code == 409:
            await update.message.reply_text("You're already registered!")
        else:
            await update.message.reply_text(
                f"Something went wrong. Status code: {response.status_code}, Error: {response.text}"
            )

        return ConversationHandler.END

    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        await update.message.reply_text("Failed to connect to the server.")
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Registration cancelled.")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ENTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
