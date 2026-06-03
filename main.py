import os
from pyrogram import Client
from telebot import TeleBot, types

# 1. الإعدادات
BOT_TOKEN = os.environ.get('API_TOKEN')
bot = TeleBot(BOT_TOKEN)

# بيانات حساب التمويل (استبدليها ببياناتك الحقيقية)
API_ID = 1234567 
API_HASH = "هنا_الـ_hash_الخاص_بك"
app = Client("my_session", api_id=API_ID, api_hash=API_HASH)

# 2. القائمة الرئيسية (الأزرار)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("➕ زيادة أعضاء", callback_data="add_members")
    btn2 = types.InlineKeyboardButton("📊 إحصائيات", callback_data="stats")
    btn3 = types.InlineKeyboardButton("⚙️ إعدادات", callback_data="settings")
    btn4 = types.InlineKeyboardButton("📞 تواصل مع الدعم", callback_data="support")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "أهلاً بك في بوت تمويل ليفاندوسكي 🔥9\nاختاري الخدمة المطلوبة:", reply_markup=markup)

# 3. معالجة الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "add_members":
        bot.send_message(call.message.chat.id, "💡 يرجى إرسال رابط القناة للبدء في التمويل:")
    elif call.data == "stats":
        bot.answer_callback_query(call.id, "إحصائياتك: 0 مشتركين")
    elif call.data == "support":
        bot.send_message(call.message.chat.id, "👤 سيقوم الدعم بالرد عليك قريباً.")

# 4. معالجة الرابط والتمويل الفعلي
@bot.message_handler(func=lambda message: "t.me" in message.text)
def handle_link(message):
    link = message.text
    bot.reply_to(message, "⏳ جاري تنفيذ التمويل، يرجى الانتظار...")
    
    try:
        # تشغيل محرك Pyrogram للانضمام للقناة
        with app:
            app.join_chat(link)
        bot.reply_to(message, "✅ تم التمويل بنجاح وبانضمام حسابك للقناة!")
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ أثناء التمويل: {e}")

print("البوت يعمل الآن...")
bot.polling()



