import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
PORT = int(os.environ.get('PORT', '8443'))

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Bot is running with webhooks!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Error occurred: {context.error}')

async def main():
    # Initialize bot application
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_error_handler(error_handler)

    # Start webhook
    webhook_url = os.getenv('WEBHOOK_URL')
    await application.bot.set_webhook(webhook_url)
    
    # Start the webhook
    await application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=webhook_url,
        secret_token=os.getenv('SECRET_TOKEN')  # Optional but recommended
    )

if __name__ == '__main__':
    import asyncio
    try:
        # Check if an event loop is already running
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No event loop is running, so create a new one
        asyncio.run(main())
    else:
        # If an event loop is running, use it to run the main coroutine
        loop.create_task(main())
