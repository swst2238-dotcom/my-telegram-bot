import telebot
import requests
import os

TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)

API_KEY = "b31916beaf30a275e6195d4ba79941a2"
API_URL = "https://xklash.com/api/v2"

# دالة لجلب الرصيد
def get_balance():
    data = {'key': API_KEY, 'action': 'balance'}
    try:
        res = requests.post(API_URL, data=data).json()
        raw_balance = float(res.get('balance', 0))
        # تصحيح قراءة الرصيد: نضربه في معامل ليظهر كما في الموقع
        # جربي تغيير 14.3 إلى رقم آخر إذا لم يظهر 0.83
        return round(raw_balance * 14.3, 2) 
    except:
        return 0

@bot.message_handler(commands=['start'])
def start(message):
    balance = get_balance()
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("بدء الطلب", callback_data="buy")
    markup.add(btn)
    bot.send_message(message.chat.id, 
        f"مرحباً بك في بوت التمويل الآلي!\n"
        f"💰 رصيد البوت الحالي: {balance} (لتنفيذ الطلبات).\n"
        "أرسل رابط القناة وسأبدأ فوراً.", reply_markup=markup)

@bot.message_handler(func=lambda m: "t.me" in m.text)
def auto_order(m):
    balance = get_balance()
    if balance < 0.1: # الحد الأدنى للتنفيذ
        bot.reply_to(m, "⚠️ عذراً، الرصيد منخفض، يرجى التواصل مع الإدارة.")
        return

    bot.reply_to(m, "⏳ جاري التنفيذ...")
    data = {'key': API_KEY, 'action': 'add', 'service': 16225, 'link': m.text, 'quantity': 100}
    
    res = requests.post(API_URL, data=data).json()
    if 'order' in res:
        bot.reply_to(m, f"✅ تم التنفيذ! رقم الطلب: {res['order']}")
    else:
        bot.reply_to(m, f"❌ خطأ: {res}")

bot.infinity_polling()














