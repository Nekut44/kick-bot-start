import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import threading

BOT_TOKEN = "8329687149:AAEEMfZ2ghcqDXDdRoqqLGSRvc5XPJNN4Lc"
ADMIN_CHAT_ID = 1170713037   # ваш chat_id, число без кавычек

# Простой обработчик, просто отвечает на любое сообщение
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Бот работает! Вы сказали: {update.message.text}")

# Flask приложение для вебхука
app = Flask(__name__)
application = None

@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

def run_bot():
    global application
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Запуск поллинга внутри asyncio цикла
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
