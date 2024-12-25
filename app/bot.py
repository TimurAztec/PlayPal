from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes
from app.youtube import search_and_download_music
import os

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hi! Send me the name of a song, and I'll fetch the MP3 for you! \nType /help for more info.")

async def help(update: Update, context: CallbackContext):
    await update.message.reply_text("/help for help.\n/settings to change playlist options\n\nTo find track you need best use format [Artist name] - [Song name]\nExample: Rick Astley - Never Gonna Give You Up ")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text
    await update.message.reply_text("Searching for the song...")
    download_path = "./downloads"
    os.makedirs(download_path, exist_ok=True)

    try:
        mp3_file = search_and_download_music(user_query, download_path)
        await update.message.reply_audio(audio=open(mp3_file, 'rb'), title=user_query)
        os.remove(mp3_file)
    except ValueError as e:
        await update.message.reply_text(str(e))
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

def setup_dispatcher(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
