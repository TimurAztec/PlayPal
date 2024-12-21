from telegram.ext import Application
from app.bot import setup_dispatcher
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables.")

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    setup_dispatcher(application)

    application.run_polling()

if __name__ == "__main__":
    main()