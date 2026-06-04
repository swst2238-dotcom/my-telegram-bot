import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import requests
import os
# تأكدي من وجود مكتبة py-cryptopay في ملف requirements.txt
from pycricryptopay import CryptoPay 

# إعدادات البوت والتوكن
TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)
# التوكن الخاص بكِ مدمج هنا
crypto = CryptoPay("591551:AAaCLeCJ3KRPZbR6Cj6Dg1eqq1iLisbkz7P")

API_KEY = "b31916beaf30a275e6195d4ba79941a2"
API_URL = "https://xklash.com/api/v2"

# 1. القائمة الرئيسية (20 زر)
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    for i in range(1, 21):
        markup.add(InlineKeyboardButton(f"خدمة رقم {i}", callback_data=f"service_{i}"))
    markup.add(InlineKeyboardButton("⬅️ العودة للرئيسية", callback_data="back_main"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛒 المتجر", "💳 شحن الرصيد", "👤 حسابي")
    bot.send_message(message.chat.id, "🔥 أهلاً بك في بوت ليفاندوسكي 9\nاختر من القائمة:", reply_markup=kb)

# 2. نظام الشحن عبر CryptoBot
@bot.message_handler(func=lambda m: m.text == "💳 شحن الرصيد")
def deposit(message):
    try:
        # إنشاء فاتورة بقيمة 1 دولار (يمكنك تغيير المبلغ)
        invoice = crypto.create_invoice(asset="USDT", amount=1)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("ادفع الآن عبر CryptoBot", url=invoice.pay_url))
        bot.reply_to(message, "اضغط على الزر أدناه لإتمام عملية الشحن:", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, "حدث خطأ في إنشاء الفاتورة، تأكدي من إعدادات الـ API.")

# 3. معالجة الأزرار والخدمات
@bot.message_handler(func=lambda m: m.text == "🛒 المتجر")
def shop(message):
    bot.send_message(message.chat.id, "اختر الخدمة المطلوبة:", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
def handle_service(call):
    service_id = call.data.split("_")[1]
    bot.answer_callback_query(call.id, f"تم اختيار الخدمة {service_id}")
    bot.send_message(call.message.chat.id, f"✅ تم اختيار الخدمة {service_id}.\nأرسل رابط القناة الآن للتنفيذ.")

# 4. تنفيذ التمويل
@bot.message_handler(func=lambda m: "t.me" in m.text)
def auto_order(m):
    msg = bot.reply_to(m, "⏳ جاري تنفيذ طلبك...")
    data = {'key': API_KEY, 'action': 'add', 'service': 16225, 'link': m.text, 'quantity': 100}
    res = requests.post(API_URL, data=data).json()
    
    if 'order' in res:
        bot.edit_message_text(f"✅ **تم التنفيذ بنجاح!**\nرقم الطلب: {res['order']}", m.chat.id, msg.message_id)
    else:
        bot.edit_message_text(f"❌ خطأ: {res.get('error', 'غير معروف')}", m.chat.id, msg.message_id)

bot.infinity_polling()


















