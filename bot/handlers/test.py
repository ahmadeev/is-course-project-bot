from telegram import Update
from telegram.ext import CallbackContext


async def echo(update: Update, context: CallbackContext):
    await update.message.reply_text(f'Вы написали: {update.message.text}')