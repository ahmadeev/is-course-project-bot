import requests
from telegram import Update
from telegram.ext import ContextTypes
from bot.config import API_URL


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    try:
        response = requests.post(
            f"{API_URL}/user",
            json={'telegram_id': telegram_id}
        )

        if response.status_code == 201:
            await update.message.reply_text("Welcome! You've been registered.")
        elif response.status_code == 409:
            await update.message.reply_text("You're already registered!")
        else:
            await update.message.reply_text("Something went wrong. Try again later.")

    except requests.RequestException:
        await update.message.reply_text("Failed to connect to the server.")
