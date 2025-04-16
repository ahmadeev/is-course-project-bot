from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.config import TELEGRAM_TOKEN, API_URL
from bot.handlers.start import start
from bot.handlers.test import echo


def main():
    print(TELEGRAM_TOKEN)
    print(API_URL)

    # application = Application.builder().token(TELEGRAM_TOKEN).build()
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=["message"])


if __name__ == '__main__':
    main()
