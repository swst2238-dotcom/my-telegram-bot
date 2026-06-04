import telebot
import requests
import os

TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)

API_KEY = "b31916beaf30a275e6195d4ba79941a2"
API_URL = "https://xklash.com/api/v2"

def get_balance():
    data = {'key': API_KEY, 'action': 'balance'}
    try:
        res = requests.post(API_URL, data=data).json()
        raw = float(res.get('balance', 0))
        return round(raw * 14.3, 2)
    except:
        return 0

@bot.message_handler(commands=['start'])
def start(message):
    balance = get_balance()
    markup = telebot.types.InlineKeyboardMarkup()
    # زر بدء التمويل
    btn = telebot.types.InlineKeyboardButton("🚀 بدء التمويل الآن", callback_data="start_order")
    markup.add(btn)
    
    welcome_text = (
        f"مرحباً بك في بوت التمويل الآلي 🤖\n\n"
        f"💰 رصيد البوت الحالي: {balance} دولار\n"
        f"---------------------------\n"
        "اضغط على الزر أدناه لبدء عملية التمويل."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_order")
def callback_start(call):
    bot.answer_callback_query(call.id, "جاري التحضير...")
    bot.send_message(call.message.chat.id, "✅ ممتاز! الآن أرسل رابط القناة (رابط تليجرام) التي تريد تمويلها وسأقوم بالباقي.")

@bot.message_handler(func=lambda m: "t.me" in m.text)
def auto_order(m):
    balance = get_balance()
    if balance < 0.1:
        bot.reply_to(m, "⚠️ الرصيد منخفض جداً، يرجى التواصل مع الإدارة.")
        return

    msg = bot.reply_to(m, "⏳ جاري تنفيذ الطلب، يرجى الانتظار...")
    
    data = {'key': API_KEY, 'action': 'add', 'service': 16225, 'link': m.text, 'quantity': 100}
    res = requests.post(API_URL, data=data).json()
    
    if 'order' in res:
        bot.edit_message_text(f"✅ تم التنفيذ بنجاح!\n🆔 رقم الطلب: {res['order']}", m.chat.id, msg.message_id)
    else:
        bot.edit_message_text(f"❌ خطأ من الموقع: {res.get('error', 'غير معروف')}", m.chat.id, msg.message_id)

bot.infinity_polling()















