import os
import telebot
from telebot import types

# جلب التوكن من الإعدادات
TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)

# القائمة الرئيسية
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("➕ زيادة أعضاء", callback_data="add_members")
    btn2 = types.InlineKeyboardButton("📊 إحصائيات", callback_data="stats")
    btn3 = types.InlineKeyboardButton("⚙️ إعدادات", callback_data="settings")
    btn4 = types.InlineKeyboardButton("📞 تواصل مع الدعم", callback_data="support")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "أهلاً بك في بوت تمويل ليفاندوسكي 🔥9\nاختاري الخدمة المطلوبة:", reply_markup=markup)

# الرد على الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "add_members":
        bot.answer_callback_query(call.id, "جاري فتح طلب التمويل...")
        bot.send_message(call.message.chat.id, "💡 يرجى إرسال رابط القناة الآن:")
    else:
        bot.answer_callback_query(call.id, "قيد التطوير...")

# حفظ الرابط عند إرساله
@bot.message_handler(func=lambda message: "t.me" in message.text)
def handle_link(message):
    bot.reply_to(message, "✅ تم استلام الرابط، جاري إضافته لقائمة التمويل...")

print("البوت يعمل الآن...")
bot.polling()





