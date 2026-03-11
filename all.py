import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7674225506:AAHExt6AzxkqeYxpzaWWJ68KMWbbZXc06wE"


PROJECT_IDS = [
"2e98b667-5104-4bde-907f-3e41b396eda9",
"19b8324a-18e3-496d-b0f2-c317cce6c97b",
"4b377184-72c0-4ab6-854f-a5d912cdf506",
"c5068e96-9ca7-4190-80ba-e184221acb51",
"0547a533-b215-4da6-a633-0cd32213302b",
"ee5b3c2c-f322-489b-b3c8-3f724d502a46",
"4e992590-060e-4e67-889a-9d68313edc1a",
"03287501-4a97-45da-ba01-323963bbcdcc",
"aaad92c2-f7c7-46ba-9239-04b24d1aa519",
"340dbd1c-b4de-4fc3-89ac-d678ac31c045",
"3e724492-6a75-4d28-87b5-221a53ce6cd9",
"07e72546-688d-4600-9d6e-757655325409",
"d2b74663-3514-4700-a7b7-25da94443e85",
"562961f4-e352-44ff-a0bf-4cd0fc3405a5",
"f0bbe0a5-4fb8-4013-8c08-f0932864996f",
"3a6e0fb8-f282-4938-810a-1600bafa547d",
"52e81882-5a96-4408-8cfc-7571704cc191",
"62bc99fa-21b2-4d46-9e2b-c65a3ee6009d",
"5ea15ba2-c5ee-4882-8f73-2abe10796ce8",
"5761af54-aace-4c30-aef3-f380afb56133",
"2a7c6c6a-da81-4787-86b4-1b26f938df7e",
"77b011c9-b5ef-4610-9f26-e8d8d37ac347",
"a16f0c27-5cc5-4e11-ade8-6d94e535b249",
"f671b5e1-72d1-4ca4-a0a3-683882a7a346",
"38c1c0f0-7367-455d-ac3f-a99db621706e",
"cad7ff37-1536-471a-9aa3-b499ac5235f3",
"e31f2399-4041-41d9-807e-9ca42650ca92",
"18afa0a2-85dc-424a-8d79-37f3a0255cd1",
"af4df1df-7f6c-4961-b7b2-0c67839d9d41",
"c75dc947-926e-4be2-b8bc-856853fa169b",
"0f2f1141-b9b9-448a-ae9a-1b3795c6eb47",
"010285fd-8c7e-478b-8931-629691ad232b",
"e96dd997-6ad6-4fee-b025-9ed1abf992a3"
]


headers = {
"User-Agent":"Mozilla/5.0",
"Accept":"application/json"
}

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


def get_projects():

    result = []

    for pid in PROJECT_IDS:

        info_url=f"https://openbudget.uz/api/v1/initiatives/{pid}"
        vote_url=f"https://openbudget.uz/api/v2/info/initiative/count/{pid}"

        info=requests.get(info_url,headers=headers).json()
        vote=requests.get(vote_url,headers=headers).json()

        name=(
        info.get("organization_title")
        or info.get("title")
        or "Noma'lum loyiha"
        )

        result.append({
        "loyiha":name,
        "ovoz":vote.get("count",0)
        })

    return result


async def results(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data=get_projects()

    data=sorted(data,key=lambda x:x["ovoz"],reverse=True)

    text="📊 Loyiha reytingi\n\n"

    medals=["🥇","🥈","🥉"]

    for i,p in enumerate(data):

        name=p["loyiha"]
        votes=p["ovoz"]

        place=medals[i] if i<3 else f"{i+1}."

        text+=f"{place} {name}\n"
        text+=f"🗳 {votes} ovoz\n\n"

    await update.message.reply_text(text)


async def top5(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data=get_projects()

    data=sorted(data,key=lambda x:x["ovoz"],reverse=True)

    top5=data[:5]

    medals=["🥇","🥈","🥉","4️⃣","5️⃣"]

    text="🏆 TOP 5 loyiha\n\n"

    for i,p in enumerate(top5):

        name=p["loyiha"]
        votes=p["ovoz"]

        text+=f"{medals[i]} {name}\n"
        text+=f"🗳 {votes} ovoz\n"

        if i>0:
            diff=top5[i-1]["ovoz"]-votes
            text+=f"👆 dan ➖ {diff} ta kam\n"

        text+="\n"

    await update.message.reply_text(text)


app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.Regex("📊 Natijalar"),results))
app.add_handler(MessageHandler(filters.Regex("🏆 TOP 5"),top5))

print("Bot ishga tushdi...")

app.run_polling()
