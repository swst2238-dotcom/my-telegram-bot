import telebot
import requests
import os

TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)

API_KEY = "b31916beaf30a275e6195d4ba79941a2"
API_URL = "https://xklash.com/api/v2"

# قائمة الكميات والأسعار (يمكنك تعديل الأسعار هنا)
# {الكمية: السعر بالنجوم}
OPTIONS = {
    "10": 1,
    "50": 4,
    "100": 7,
    "500": 30
}

# تخزين مؤقت للكمية المختارة
user_qty = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = [telebot.types.InlineKeyboardButton(f"{qty} عضو بـ {price} نجمة", callback_data=f"qty_{qty}") 
               for qty, price in OPTIONS.items()]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "مرحباً بك في متجر ليغاندوسكي!\nاختر عدد الأعضاء الذي تريده:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("qty_"))
def select_qty(call):
    qty = call.data.split("_")[1]
    price = OPTIONS[qty]
    user_qty[call.message.chat.id] = qty
    
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 
        f"✅ اخترت {qty} عضو.\n💰 المطلوب تحويل: {price} نجمة.\n\n"
        f"بعد التحويل لحسابي @Jama2006A82، أرسل رابط قناتك هنا للبدء.")

@bot.message_handler(func=lambda m: "t.me" in m.text)
def execute_order(m):
    qty = user_qty.get(m.chat.id)
    if not qty:
        bot.reply_to(m, "❌ يرجى اختيار الكمية من الأزرار أولاً عبر كتابة /start")
        return

    bot.reply_to(m, f"⏳ جاري تمويل طلبك ({qty} عضو)...")
    
    data = {
        'key': API_KEY,
        'action': 'add',
        'service': 16225, # الخدمة المطلوبة
        'link': m.text,
        'quantity': int(qty)
    }
    
    try:
        res = requests.post(API_URL, data=data).json()
        if 'order' in res:
            bot.reply_to(m, f"✅ تم التنفيذ بنجاح! رقم الطلب: {res['order']}")
            del user_qty[m.chat.id] # مسح الطلب بعد التنفيذ
        else:
            bot.reply_to(m, f"❌ خطأ من الموقع: {res}")
    except Exception as e:
        bot.reply_to(m, f"❌ خطأ تقني: {e}")

bot.infinity_polling()













