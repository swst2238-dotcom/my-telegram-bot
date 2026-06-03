import telebot
import requests
import os

# الاتصال بالبوت
TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)

# تم وضع مفتاح الـ API الخاص بكِ هنا
API_KEY = "65361371be2f02279470ed1387d7" 
API_URL = "https://xklash.com/api/v2"

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("طلب تمويل 100 عضو", callback_data="buy_100")
    markup.add(btn)
    bot.send_message(message.chat.id, "أهلاً بك في متجر تمويل ليغاندوسكي! اختر خدمتك:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "buy_100")
def buy_info(call):
    bot.answer_callback_query(call.id, text="جاري التحويل...")
    bot.send_message(call.message.chat.id, 
        "⭐ لطلب 100 عضو بـ 13 نجمة:\n\n"
        "1. قم بتحويل المقابل المادي لحسابي: @Jama2006A82\n"
        "2. بعد التحويل، أرسل كلمة 'تم التحويل' هنا.\n"
        "3. سأطلب منك رابط قناتك فوراً لتمويلها.")

@bot.message_handler(func=lambda message: message.text == "تم التحويل")
def ask_for_link(message):
    bot.reply_to(message, "✅ ممتاز! أرسل الآن رابط القناة التي تريد تمويلها:")

@bot.message_handler(func=lambda m: "t.me" in m.text)
def send_to_xklash(m):
    data = {
        'key': API_KEY,
        'action': 'add',
        'service': 50, 
        'link': m.text,
        'quantity': 100
    }
    try:
        res = requests.post(API_URL, data=data).json()
        if 'order' in res:
            bot.reply_to(m, f"✅ تم إرسال الطلب للموقع بنجاح! رقم الطلب: {res['order']}")
        else:
            bot.reply_to(m, f"❌ خطأ: {res.get('error', 'تأكد من رصيدك في الموقع')}")
    except Exception as e:
        bot.reply_to(m, "❌ حدث خطأ تقني.")

bot.infinity_polling()










