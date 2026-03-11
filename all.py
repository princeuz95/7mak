import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
TOKEN = "7674225506:AAHExt6AzxkqeYxpzaWWJ68KMWbbZXc06wE"

API_URL = "http://127.0.0.1:5000"

keyboard = ReplyKeyboardMarkup(
    [
        ["🏆 TOP 5"],
        ["📊 Natijalar"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Natijalarni ko‘rish uchun tugmani bosing",
        reply_markup=keyboard
    )

async def results(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = requests.get(API_URL).json()

    # ovozlar bo‘yicha saralash
    data = sorted(data, key=lambda x: x["ovoz"], reverse=True)

    text = "📊 <b>Loyiha reytingi</b>\n\n"

    medals = ["🥇","🥈","🥉"]

    for i, p in enumerate(data):

        name = p["loyiha"]
        votes = p["ovoz"]

        if i < 3:
            place = medals[i]
        else:
            place = f"{i+1}."

        text += f"{place} <b>{name}</b>\n"
        text += f"🗳 {votes} ovoz\n"

        # faqat 2-5 o‘rinlar uchun farqni ko‘rsatish
        if 1 <= i <= 4:
            diff = data[i-1]["ovoz"] - votes
            text += f"👆 dan ➖ {diff} ta kam\n"

        text += "\n"

    await update.message.reply_text(text, parse_mode="HTML")

async def top5(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = requests.get(API_URL).json()

    data = sorted(data, key=lambda x: x["ovoz"], reverse=True)

    top5 = data[:5]

    medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]

    text = "🏆 <b>TOP 5 loyiha</b>\n\n"

    for i, p in enumerate(top5):

        name = p["loyiha"]
        votes = p["ovoz"]

        text += f"{medals[i]} <b>{name}</b>\n"
        text += f"🗳 {votes} ovoz\n"

        if i > 0:
            diff = top5[i-1]["ovoz"] - votes
            text += f"👆 dan ➖ {diff} ta kam\n"

        text += "\n"

    await update.message.reply_text(text, parse_mode="HTML")



app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Regex("🏆 TOP 5"), top5))
app.add_handler(MessageHandler(filters.Regex("📊 Natijalar"), results))


print("Bot ishga tushdi...")

app.run_polling()