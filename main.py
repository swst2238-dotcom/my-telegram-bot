
import os
from pyrogram import Client
from telebot import TeleBot, types

# إعدادات البوت
BOT_TOKEN = os.environ.get('API_TOKEN')
bot = TeleBot(BOT_TOKEN)

# إعدادات الـ Pyrogram (محرك التمويل)
# تأكدي أن لديكِ ملفات الـ session في نفس المجلد
API_ID = 1234567 
API_HASH = "اكتبي_هنا_الـ_hash"

# إنشاء محرك التمويل
app = Client("my_session", api_id=API_ID, api_hash=API_HASH)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "أهلاً بك في بوت ليفاندوسكي للتمويل الحقيقي 🔥9\nأرسلي رابط القناة للبدء:")

@bot.message_handler(func=lambda message: "t.me" in message.text)
def handle_link(message):
    link = message.text
    bot.reply_to(message, "⏳ جاري الانضمام للقناة عبر حسابات التمويل...")
    
    try:
        # هنا المحرك الفعلي
        with app:
            app.join_chat(link)
        bot.reply_to(message, "✅ تم الانضمام للقناة بنجاح!")
    except Exception as e:
        bot.reply_to(message, f"❌ فشل التمويل: {e}")

# تشغيل البوت
if __name__ == "__main__":
    bot.polling()





