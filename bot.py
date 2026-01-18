#!/usr/bin/env python3
"""
Telegram Scam Bot - Clean Working Version for Render
Using python-telegram-bot 13.15
"""

import os
import sys
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# ========== CONFIGURATION ==========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("=" * 50)
    logger.error("ERROR: BOT_TOKEN not found in environment variables!")
    logger.error("=" * 50)
    logger.error("On Render dashboard:")
    logger.error("1. Go to your service")
    logger.error("2. Click 'Environment' tab")
    logger.error("3. Add Environment Variable:")
    logger.error("   Key: BOT_TOKEN")
    logger.error("   Value: 8126424869:AAE-GFxBL5ip9ZwS1yJDR44AS3T1zvI1a8")
    logger.error("4. Click 'Save Changes'")
    logger.error("5. Click 'Manual Deploy'")
    logger.error("=" * 50)
    sys.exit(1)

logger.info(f"✅ Bot token found: {BOT_TOKEN[:10]}...")
logger.info("🚀 Starting scam bot...")

# ========== BOT CODE ==========
def start(update, context):
    """Send welcome message with 3 options"""
    keyboard = [
        [InlineKeyboardButton("💳 Cart Visa", callback_data='visa'),
         InlineKeyboardButton("💰 Transfers", callback_data='transfer'),
         InlineKeyboardButton("🛠️ Method", callback_data='method')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "Bonjour ami, tu veux acheter une carte de crédit, effectuer des virements ou utiliser d'autres méthodes ?",
        reply_markup=reply_markup
    )

def button(update, context):
    """Handle all button presses"""
    query = update.callback_query
    query.answer()
    
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
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Quel montant souhaitez-vous que la carte Visa contienne en argent ?",
            reply_markup=reply_markup
        )
    
    # VISA AMOUNTS - Show payment details
    elif data in ['400', '500', '600', '700', '800']:
        payment_text = """Payez ici Virement Instant Veuillez 

IBAN: DE48202208000040574891 

NOM ET PRENOM (REQUIS): AYMEN NOUFA

Veuillez envoyer une capture d'écran une fois le transfert effectué. Merci.

En cas de problème, veuillez contacter @de9avrai."""
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=payment_text
        )
    
    # TRANSFERS OPTION
    elif data == 'transfer':
        keyboard = [
            [InlineKeyboardButton("Crypto", callback_data='crypto')],
            [InlineKeyboardButton("Virement", callback_data='virement')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Préférez-vous les transferts en cryptomonnaie ou les transferts Virement ?",
            reply_markup=reply_markup
        )
    
    # CRYPTO TRANSFER
    elif data == 'crypto':
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Rendez-vous sur @de9avrai si vous souhaitez obtenir l'adresse crypto pour effectuer le paiement."
        )
    
    # BANK TRANSFER
    elif data == 'virement':
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Pour tout virement bancaire, veuillez contacter @De9avrai."
        )
    
    # METHOD OPTION
    elif data == 'method':
        keyboard = [
            [InlineKeyboardButton("Fnac V2", callback_data='fnac')],
            [InlineKeyboardButton("Booking", callback_data='booking')],
            [InlineKeyboardButton("BackMarket", callback_data='backmarket')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Choisissez une méthode :",
            reply_markup=reply_markup
        )
    
    # METHOD SUB-OPTIONS
    elif data in ['fnac', 'booking', 'backmarket']:
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Si vous souhaitez acheter la méthode, rendez-vous sur @de9avrai."
        )

def error(update, context):
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    logger.info("✅ Creating updater...")
    
    # Create updater
    updater = Updater(BOT_TOKEN, use_context=True)
    
    # Get dispatcher
    dp = updater.dispatcher
    
    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_error_handler(error)
    
    # Start bot
    logger.info("✅ Bot is running! Ready to scam!")
    logger.info("💸 Waiting for victims...")
    
    # Start polling
    updater.start_polling()
    
    # Run the bot until stopped
    updater.idle()

if __name__ == '__main__':
    main()
