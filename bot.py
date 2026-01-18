#!/usr/bin/env python3
"""
Telegram Scam Bot - Render Hosting Version
"""

import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable (Render sets this)
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("No BOT_TOKEN found in environment variables!")
    logger.error("On Render: Add it in Environment variables section")
    logger.error("Locally: Create .env file with BOT_TOKEN=your_token")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with 3 options"""
    keyboard = [
        [InlineKeyboardButton("💳 Cart Visa", callback_data='visa')],
        [InlineKeyboardButton("💰 Transfers", callback_data='transfer')],
        [InlineKeyboardButton("🛠️ Method", callback_data='method')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Bonjour ami, tu veux acheter une carte de crédit, effectuer des virements ou utiliser d'autres méthodes ?",
        reply_markup=reply_markup
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all button presses"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # VISA OPTION
    if data == 'visa':
        keyboard = [
            [InlineKeyboardButton("💳 400 Euro pour 40", callback_data='400')],
            [InlineKeyboardButton("💳 500 Euro pour 50", callback_data='500')],
            [InlineKeyboardButton("💳 600 Euro pour 60", callback_data='600')],
            [InlineKeyboardButton("💳 700 Euro pour 70", callback_data='700')],
            [InlineKeyboardButton("💳 800 Euro pour 80", callback_data='800')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Quel montant souhaitez-vous que la carte Visa contienne en argent ?",
            reply_markup=reply_markup
        )
    
    # VISA AMOUNTS - Show payment details
    elif data in ['400', '500', '600', '700', '800']:
        payment_text = """Payez ici Virement Instant Veuillez 

IBAN: DE48202208000040574891 

NOM ET PRENOM (REQUIS): AYMEN NOUFA

Veuillez envoyer une capture d'écran une fois le transfert effectué. Merci.

En cas de problème, veuillez contacter @de9avrai."""
        await query.edit_message_text(payment_text)
    
    # TRANSFERS OPTION
    elif data == 'transfer':
        keyboard = [
            [InlineKeyboardButton("Crypto", callback_data='crypto')],
            [InlineKeyboardButton("Virement", callback_data='virement')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Préférez-vous les transferts en cryptomonnaie ou les transferts Virement ?",
            reply_markup=reply_markup
        )
    
    # CRYPTO TRANSFER
    elif data == 'crypto':
        await query.edit_message_text(
            "Rendez-vous sur @de9avrai si vous souhaitez obtenir l'adresse crypto pour effectuer le paiement."
        )
    
    # BANK TRANSFER
    elif data == 'virement':
        await query.edit_message_text(
            "Pour tout virement bancaire, veuillez contacter @De9avrai."
        )
    
    # METHOD OPTION
    elif data == 'method':
        keyboard = [
            [InlineKeyboardButton("Fnac V2", callback_data='fnac')],
            [InlineKeyboardButton("Booking", callback_data='booking')],
            [InlineKeyboardButton("BackMarket", callback_data='backmarket')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Choisissez une méthode :",
            reply_markup=reply_markup
        )
    
    # METHOD SUB-OPTIONS
    elif data in ['fnac', 'booking', 'backmarket']:
        await query.edit_message_text(
            "Si vous souhaitez acheter la méthode, rendez-vous sur @de9avrai."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Error: {context.error}")

def main():
    """Start the bot"""
    # Log startup
    logger.info("🚀 Starting scam bot...")
    logger.info(f"🤖 Using token: {BOT_TOKEN[:10]}...")  # Only show first 10 chars for security
    
    # Create application
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_error_handler(error_handler)
    
    # Start bot
    logger.info("✅ Bot is running! Ready to scam!")
    logger.info("💸 Waiting for victims...")
    
    # Run with better error handling for Render
    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == '__main__':
    main()
