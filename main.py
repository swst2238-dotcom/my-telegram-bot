import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import os

# إعدادات البوت والموقع
TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)
API_KEY = "b31916beaf30a275e6195d4ba79941a2"
API_URL = "https://xklash.com/api/v2"

# الباقات المتاحة
PACKAGES = {
    "100 عضو": 100,
    "500 عضو": 500,
    "1000 عضو": 1000
}

# تخزين مؤقت للطلبات
user_temp_qty = {}

# قائمة الأزرار الرئيسية
def get_main_markup():
    markup = InlineKeyboardMarkup()
    for text, qty in PACKAGES.items():
        markup.add(InlineKeyboardButton(f"🛒 شراء {text}", callback_data=f"qty_{qty}"))
    markup.add(InlineKeyboardButton("🎧 تواصل مع الدعم الفني", url="https://t.me/Jama2006A82"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "🔥 **أهلاً بك في بوت تمويل ليفاندوسكي 9** 🔥\n\n"
        "بوتك الأول لخدمات التمويل الحقيقي.\n"
        "اختر باقتك من القائمة أدناه، ولأي استفسار تواصل معنا عبر الدعم الفني."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_markup(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("qty_"))
def handle_qty(call):
    qty = call.data.split("_")[1]
    user_temp_qty[call.message.chat.id] = qty
    bot.answer_callback_query(call.id, f"تم اختيار {qty} عضو")
    bot.send_message(call.message.chat.id, f"✅ تم اختيار باقة {qty} عضو.\nأرسل رابط القناة الآن وسأبدأ فوراً!")

@bot.message_handler(func=lambda m: "t.me" in m.text)
def execute_order(m):
    qty = user_temp_qty.get(m.chat.id)
    if not qty:
        bot.reply_to(m, "❌ يرجى اختيار الباقة أولاً من زر /start")
        return

    msg = bot.reply_to(m, "⏳ جاري الإرسال للموقع، يرجى الانتظار...")
    
    data = {
        'key': API_KEY,
        'action': 'add',
        'service': 16225, 
        'link': m.text,
        'quantity': int(qty)
    }
    
    res = requests.post(API_URL, data=data).json()
    
    if 'order' in res:
        bot.edit_message_text(f"✅ **تم تنفيذ طلب ليفاندوسكي بنجاح!**\n🆔 رقم الطلب: {res['order']}", m.chat.id, msg.message_id, parse_mode="Markdown")
        user_temp_qty.pop(m.chat.id, None)
    else:
        error_msg = res.get('error', 'خطأ غير معروف')
        bot.edit_message_text(f"❌ **حدث خطأ:** {error_msg}", m.chat.id, msg.message_id, parse_mode="Markdown")

# تشغيل البوت
if __name__ == "__main__":
    bot.infinity_polling()
















