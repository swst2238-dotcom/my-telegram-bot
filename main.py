import telebot
import requests
import os

TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)

# تم تحديث المفتاح بالمفتاح الجديد الذي أرسلتِه
API_KEY = "b31916beaf30a275e6195d4ba79941a2" 
API_URL = "https://xklash.com/api/v2"

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("بدء طلب التمويل الآن", callback_data="start_proc")
    markup.add(btn)
    bot.send_message(message.chat.id, "مرحباً بك! اضغط الزر أدناه لبدء الطلب:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_proc")
def process_step(call):
    bot.answer_callback_query(call.id, text="جاري الفتح...")
    bot.send_message(call.message.chat.id, 
        "⭐ لطلب 100 عضو:\n\n"
        "1. قم بتحويل المقابل المادي لحسابي: @Jama2006A82\n"
        "2. بعد التحويل، أرسل كلمة 'تم التحويل' هنا.")

@bot.message_handler(func=lambda message: message.text == "تم التحويل")
def ask_for_link(message):
    bot.reply_to(message, "✅ ممتاز! أرسل الآن رابط القناة التي تريد تمويلها وسأبدأ فوراً:")

@bot.message_handler(func=lambda m: "t.me" in m.text)
def send_to_xklash(m):
    bot.reply_to(m, "⏳ جارٍ الإرسال للموقع، يرجى الانتظار...")
    data = {
        'key': API_KEY,
        'action': 'add',
        'service': 16234,  # الخدمة الصحيحة التي اخترناها
        'link': m.text,
        'quantity': 100
    }
    try:
        res = requests.post(API_URL, data=data).json()
        if 'order' in res:
            bot.reply_to(m, f"✅ تم تنفيذ الطلب بنجاح! رقم الطلب هو: {res['order']}")
        else:
            bot.reply_to(m, f"❌ خطأ من الموقع: {res}")
    except Exception as e:
        bot.reply_to(m, f"❌ حدث خطأ تقني: {e}")

bot.infinity_polling()











