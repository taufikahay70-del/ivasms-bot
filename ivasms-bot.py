mimport os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
IVASMS_API_KEY = os.getenv("IVASMS_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Bot iVASMS sudah jalan ✅\nKetik /saldo untuk cek saldo iVASMS kamu")

async def cek_saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not IVASMS_API_KEY:
        await update.message.reply_text("API Key iVASMS belum diset di Railway")
        return
    try:
        url = f"https://ivasms.com/api/balance?api_key={IVASMS_API_KEY}"
        res = requests.get(url, timeout=10).json()
        if "balance" in res:
            await update.message.reply_text(f"Saldo kamu: Rp {res['balance']}")
        else:
            await update.message.reply_text("Gagal ambil saldo. Cek API Key kamu.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("saldo", cek_saldo))
app.run_polling()
