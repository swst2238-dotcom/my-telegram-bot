import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import os

TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = "5531196107"
API_KEY = "b31916beaf30a275e6195d4ba79941a2"
API_URL = "https://xklash.com/api/v2"

# القائمة الرئيسية للخدمات
def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ 100 عضو (2$)", callback_data="buy_100"))
    markup.add(InlineKeyboardButton("✅ 200 عضو (4$)", callback_data="buy_200"))
    markup.add(InlineKeyboardButton("✅ 400 عضو (8$)", callback_data="buy_400"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "مرحباً بك في بوت ليفاندوسكي 9.\nاختر الخدمة للبدء:", reply_markup=main_menu())

# عند اختيار خدمة
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_service(call):
    qty = call.data.split("_")[1]
    bot.send_message(call.message.chat.id, f"لقد اخترت {qty} عضو.\nالآن أرسل رابط القناة والـ TxID الخاص بدفع USDT (شبكة TRC20).")

# استقبال الـ TxID
@bot.message_handler(func=lambda m: len(m.text) > 10)
def get_txid(message):
    # إرسال طلب للأدمن (أنتِ)
    msg = f"🚨 طلب جديد من {message.from_user.id}\nالرسالة: {message.text}"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ قبول وتفعيل الطلب", callback_data=f"accept_{message.chat.id}"))
    bot.send_message(ADMIN_ID, msg, reply_markup=markup)
    bot.reply_to(message, "تم استلام بياناتك، الإدارة تراجع الطلب الآن.")

# تأكيد الأدمن
@bot.callback_query_handler(func=lambda call: call.data.startswith("accept_"))
def accept(call):
    user_id = call.data.split("_")[1]
    bot.send_message(user_id, "✅ تم قبول الطلب! جاري التنفيذ.")
    bot.edit_message_text("تم تفعيل الطلب.", call.message.chat.id, call.message.message_id)

bot.infinity_polling()




















