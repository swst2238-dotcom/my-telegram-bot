import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import requests
import os

# إعداد البوت
TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)
API_KEY = "b31916beaf30a275e6195d4ba79941a2"
API_URL = "https://xklash.com/api/v2"

# بيانات الباقات
PACKAGES = {"100 عضو": 100, "500 عضو": 500, "1000 عضو": 1000}
user_temp_qty = {}

# 1. زر الترحيب والبدء (القائمة الرئيسية)
def main_menu():
    markup = InlineKeyboardMarkup()
    for text, qty in PACKAGES.items():
        markup.add(InlineKeyboardButton(f"🛒 شراء {text}", callback_data=f"qty_{qty}"))
    markup.add(InlineKeyboardButton("🎧 تواصل مع الدعم الفني", url="https://t.me/Jama2006A82"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    # لوحة أزرار سفلية إضافية (مثل بوت تمويل الدينار)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🚀 تمويلاتي"), KeyboardButton("💰 رصيد الموقع"))
    
    welcome_text = (
        "🔥 **أهلاً بك في بوت ليفاندوسكي 9** 🔥\n\n"
        "أفضل خدمات التمويل الحقيقي.\n"
        "اختر باقتك من الأزرار أدناه:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(), parse_mode="Markdown")
    bot.send_message(message.chat.id, "لوحة التحكم:", reply_markup=keyboard)

# 2. كود الاستعلام عن الرصيد
@bot.message_handler(func=lambda m: m.text == "💰 رصيد الموقع")
def check_balance(message):
    data = {'key': API_KEY, 'action': 'balance'}
    try:
        res = requests.post(API_URL, data=data).json()
        bal = round(float(res.get('balance', 0)) * 14.3, 2)
        bot.reply_to(message, f"💰 رصيد البوت الحالي في الموقع هو: {bal} دولار")
    except:
        bot.reply_to(message, "❌ خطأ في الاتصال بالموقع.")

# 3. كود اختيار الباقة
@bot.callback_query_handler(func=lambda call: call.data.startswith("qty_"))
def handle_qty(call):
    qty = call.data.split("_")[1]
    user_temp_qty[call.message.chat.id] = qty
    bot.answer_callback_query(call.id, f"تم اختيار {qty} عضو")
    bot.send_message(call.message.chat.id, "✅ الآن أرسل رابط القناة التي تريد تمويلها وسأبدأ فوراً!")

# 4. كود التمويل (التنفيذ التلقائي)
@bot.message_handler(func=lambda m: "t.me" in m.text)
def execute_order(m):
    qty = user_temp_qty.get(m.chat.id)
    if not qty:
        bot.reply_to(m, "❌ يرجى اختيار الباقة أولاً من قائمة الشراء.")
        return

    msg = bot.reply_to(m, "⏳ جاري تنفيذ الطلب، يرجى الانتظار...")
    data = {'key': API_KEY, 'action': 'add', 'service': 16225, 'link': m.text, 'quantity': int(qty)}
    res = requests.post(API_URL, data=data).json()
    
    if 'order' in res:
        bot.edit_message_text(f"✅ **تم تنفيذ الطلب بنجاح!**\n🆔 رقم الطلب: {res['order']}", m.chat.id, msg.message_id, parse_mode="Markdown")
        user_temp_qty.pop(m.chat.id, None)
    else:
        bot.edit_message_text(f"❌ **حدث خطأ:** {res.get('error', 'غير معروف')}", m.chat.id, msg.message_id, parse_mode="Markdown")

bot.infinity_polling()

















