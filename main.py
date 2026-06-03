import os
import telebot
from telebot import types

TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 1. القائمة الرئيسية لبوت التمويل
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    # أزرار خدمات التمويل
    btn1 = types.InlineKeyboardButton("➕ زيادة أعضاء", callback_data="add_members")
    btn2 = types.InlineKeyboardButton("📊 إحصائيات القناة", callback_data="stats")
    btn3 = types.InlineKeyboardButton("⚙️ إعدادات التمويل", callback_data="settings")
    btn4 = types.InlineKeyboardButton("📞 تواصل مع الدعم", callback_data="support")
    
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "أهلاً بك في بوت تمويل ليفاندوسكي 🔥9\nاختاري الخدمة المطلوبة:", reply_markup=markup)

# 2. الاستجابة للأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "add_members":
        bot.answer_callback_query(call.id, "جاري فتح طلب التمويل...")
        bot.send_message(call.message.chat.id, "💡 يرجى إرسال رابط القناة المراد تمويلها الآن:")
    
    elif call.data == "stats":
        bot.answer_callback_query(call.id, "جاري جلب البيانات...")
        bot.send_message(call.message.chat.id, "📊 إحصائياتك الحالية:\n- عدد المشتركين: 0\n- رصيد التمويل: 0")
        
    elif call.data == "settings":
        bot.answer_callback_query(call.id, "جاري فتح الإعدادات...")
        bot.send_message(call.message.chat.id, "⚙️ يمكنك التحكم في سرعة التمويل من هنا.")
        
    elif call.data == "support":
        bot.answer_callback_query(call.id, "جاري تحويلك للدعم...")
        bot.send_message(call.message.chat.id, "👤 سيقوم أحد المبرمجين بالرد عليكِ في أقرب وقت.")

# 3. معالجة الردود (عند إرسال رابط القناة)
@bot.message_handler(func=lambda message: "t.me" in message.text)
def handle_link(message):
    bot.reply_to(message, "✅ تم استلام الرابط، جاري البدء في فحص القناة للتمويل...")

print("البوت يعمل الآن...")
bot.polling()


