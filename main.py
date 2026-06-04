import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import os

TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = "5531196107"

# القائمة المحدثة بالخدمات المطلوبة
def main_menu():
    markup = InlineKeyboardMarkup(row_width=3) # توزيع 3 أزرار في كل صف
    services = [10, 50, 100, 150, 200, 250, 300, 350, 400, 500, 1000]
    buttons = [InlineKeyboardButton(f"✅ {s} عضو", callback_data=f"buy_{s}") for s in services]
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🔥 بوت ليفاندوسكي 9 للتمويل الحقيقي.\nاختر الباقة المطلوبة:", reply_markup=main_menu())

# عند اختيار خدمة
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_service(call):
    qty = call.data.split("_")[1]
    bot.send_message(call.message.chat.id, f"✅ تم اختيار باقة {qty} عضو.\nالآن أرسل رابط القناة والـ TxID الخاص بدفع USDT (شبكة TRC20) ليتم تفعيل الطلب.")

# استقبال الـ TxID
@bot.message_handler(func=lambda m: len(m.text) > 10 and " " in m.text)
def get_txid(message):
    msg = f"🚨 طلب جديد من العميل: {message.from_user.id}\nالرسالة: {message.text}"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ قبول وتفعيل الطلب", callback_data=f"accept_{message.chat.id}"))
    bot.send_message(ADMIN_ID, msg, reply_markup=markup)
    bot.reply_to(message, "⏳ تم إرسال بياناتك للإدارة، سيتم التنفيذ فور التأكيد.")

# تأكيد الأدمن
@bot.callback_query_handler(func=lambda call: call.data.startswith("accept_"))
def accept(call):
    user_id = call.data.split("_")[1]
    bot.send_message(user_id, "✅ تم قبول الطلب! جاري التنفيذ الآن.")
    bot.edit_message_text("✅ تم تفعيل الطلب بنجاح.", call.message.chat.id, call.message.message_id)

bot.infinity_polling()





















