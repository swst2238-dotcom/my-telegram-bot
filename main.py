import telebot
import requests
import os

TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)

API_KEY = "b31916beaf30a275e6195d4ba79941a2"
API_URL = "https://xklash.com/api/v2"

# PRODUCTS = { "العدد": [تكلفة الموقع، سعركِ للعميل] }
# يمكنكِ تعديل السعر الثاني (سعر العميل) لزيادة ربحكِ
PRODUCTS = {
    "10": [0.02, 1],   # مثال: تكلفة الموقع 0.02، تبيعين بـ 1 نجمة
    "50": [0.10, 3],
    "100": [0.20, 5]
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    for count in PRODUCTS:
        price = PRODUCTS[count][1]
        markup.add(telebot.types.InlineKeyboardButton(f"{count} عضو بـ {price} نجمة", callback_data=f"buy_{count}"))
    bot.send_message(message.chat.id, "مرحباً! اختر الكمية التي تريد تمويلها:", reply_markup=markup)

# تخزين مؤقت للكمية المطلوبة
user_selected_qty = {}

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def process_order(call):
    count = call.data.split("_")[1]
    price = PRODUCTS[count][1]
    user_selected_qty[call.message.chat.id] = count
    
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 
        f"✅ اخترت {count} عضو.\n"
        f"💰 السعر المطلوب: {price} نجمة.\n\n"
        "يرجى التحويل لحسابي @Jama2006A82 ثم أرسل رابط قناتك هنا للبدء.")

@bot.message_handler(func=lambda m: "t.me" in m.text)
def execute_order(m):
    count = user_selected_qty.get(m.chat.id, "10")
    bot.reply_to(m, f"⏳ جاري تمويل {count} عضو...")
    
    data = {'key': API_KEY, 'action': 'add', 'service': 16234, 'link': m.text, 'quantity': int(count)}
    res = requests.post(API_URL, data=data












