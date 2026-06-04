import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import requests
import os
from pycricryptopay import CryptoPay

# إعدادات البوت والتوكن
TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)
crypto = CryptoPay("591551:AAaCLeCJ3KRPZbR6Cj6Dg1eqq1iLisbkz7P")

API_KEY = "b31916beaf30a275e6195d4ba79941a2"
API_URL = "https://xklash.com/api/v2"

# 1. القائمة الرئيسية (20 زر مرتبة)
def main_menu():
    markup = InlineKeyboardMarkup(row_width=4) # 4 أزرار في كل سطر
    buttons = []
    for i in range(1, 21):
        buttons.append(InlineKeyboardButton(f"خدمة {i}", callback_data=f"service_{i}"))
    markup.add(*buttons) # إضافة جميع الأزرار للقائمة
    markup.add(InlineKeyboardButton("⬅️ العودة للرئيسية", callback_data="back_main"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛒 المتجر", "💳 شحن الرصيد", "👤 حسابي")
    bot.send_message(message.chat.id, "🔥 أهلاً بك في بوت ليفاندوسكي 9\nاختر من القائمة:", reply_markup=kb)

# 2. نظام الشحن
@bot.message_handler(func=lambda m: m.text == "💳 شحن الرصيد")
def deposit(message):
    invoice = crypto.create_invoice(asset="USDT", amount=1)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("ادفع الآن عبر CryptoBot", url=invoice.pay_url))
    bot.reply_to(message, "اضغط للتحويل:", reply_markup=markup)

# 3. عرض الخدمات
@bot.message_handler(func=lambda m: m.text == "🛒 المتجر")
def shop(message):
    bot.send_message(message.chat.id, "اختر الخدمة المطلوبة:", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
def handle_service(call):
    service_id = call.data.split("_")[1]
    bot.send_message(call.message.chat.id, f"✅ تم اختيار الخدمة {service_id}.\nأرسل رابط القناة الآن للتنفيذ.")

# 4. تنفيذ التمويل
@bot.message_handler(func=lambda m: "t.me" in m.text)
def auto_order(m):
    msg = bot.reply_to(m, "⏳ جاري التنفيذ...")
    data = {'key': API_KEY, 'action': 'add', 'service': 16225, 'link': m.text, 'quantity': 100}
    res = requests.post(API_URL, data=data).json()
    if 'order' in res:
        bot.edit_message_text(f"✅ تم التنفيذ! رقم الطلب: {res['order']}", m.chat.id, msg.message_id)
    else:
        bot.edit_message_text(f"❌ خطأ: {res.get('error', 'غير معروف')}", m.chat.id, msg.message_id)

bot.infinity_polling()



















