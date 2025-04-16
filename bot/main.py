import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.config import TELEGRAM_TOKEN, API_URL
from bot.handlers.start import conv_handler
from bot.handlers.test import echo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # application = Application.builder().token(TELEGRAM_TOKEN).build()
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        application.add_handler(conv_handler)

        application.run_polling(allowed_updates=["message"])
    except Exception as e:
        logger.error("Bot failed to start: %s", e)


if __name__ == '__main__':
    main()
