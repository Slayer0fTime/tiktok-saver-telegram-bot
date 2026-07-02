import os
import logging
from dotenv import load_dotenv
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    InlineQueryHandler,
)
from telegram import MessageEntity

from .handlers import start, help_command, unknown, send_video, inline_video


def main() -> None:
    # Load env variables
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logging.critical("BOT_TOKEN environment variable is missing")
        return

    # Build Application
    app = ApplicationBuilder().token(bot_token).build()

    # Register Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Register Message Handlers for TikTok Links
    link_filter = filters.TEXT & (
        filters.Entity(MessageEntity.URL) | filters.Entity(MessageEntity.TEXT_LINK)
    )
    app.add_handler(MessageHandler(link_filter, send_video))

    # Register Inline Query Handlers
    app.add_handler(InlineQueryHandler(inline_video))

    # Start Polling
    logging.info("Starting Telegram bot polling...")
    app.run_polling()
