from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from agent.brain import ask_agent
from settings import settings

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Olá! Eu sou o {settings.BOT_NAME}. Qual ação você quer analisar hoje?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    response = ask_agent(user_text)
    await update.message.reply_text(response)

def run_telegram_bot():
    app = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot em execução...")
    app.run_polling()