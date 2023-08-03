import os
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes
from hashlib import md5
from datetime import datetime

if "data" not in os.listdir():
    os.mkdir("data")

def encode_to_md5(value):
    return md5( ( str(value) ).encode("utf-8") ).hexdigest()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.full_name not in os.listdir("data"):
        os.mkdir(f"data/{update.effective_user.full_name}")

    photo_hash_name = encode_to_md5(f"{datetime.now()}{update.effective_user.full_name}")

    new_file = await update.effective_message.effective_attachment[-1].get_file()
    await new_file.download_to_drive(f'data/{update.effective_user.full_name}/{photo_hash_name}.png')

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Foto adicionada ao seu perfil")



if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ["TOKEN_BOT"]).build()
    
    echo_handler = MessageHandler(filters.PHOTO, echo)
    application.add_handler(echo_handler)

    application.run_polling()