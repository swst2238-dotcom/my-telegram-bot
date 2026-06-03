import os
from pyrogram import Client
from telebot import TeleBot, types
import threading

# 1. إعدادات البوت (موظف الاستقبال)
BOT_TOKEN = os.environ.get('API_TOKEN')
bot = TeleBot(BOT_TOKEN)

# 2. إعدادات حساب التمويل (فريق التنفيذ)
# ضعي هنا الأرقام التي حصلتِ عليها من my.telegram.org
API_ID = 1234567 
API_HASH = "هنا_الـ_hash_الخاص_بك"

# تهيئة حساب التمويل
app = Client("my_session", api_id=API_ID, api_hash=API_HASH)

# دالة حفظ الرابط في ملف
def save_link(link):
    with open("channels.txt", "a") as f:
        f.write(link + "\n")

# --- أوامر البوت ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "أهلاً في بوت ليفاندوسكي 🔥9\nأرسلي رابط القناة للتمويل:")

@bot.message_handler(func=lambda message: "t.me" in message.text)
def handle_link(message):
    link = message.text
    save_link(link) # حفظ الرابط في الملف
    bot.reply_to(message, "✅ تم استلام الرابط، جاري إضافته لقائمة التمويل...")

# --- وظيفة التمويل (فريق التنفيذ) ---
def run_funding_task():
    # هذا السكربت يقرأ الملف وينفذ التمويل
    # سنقوم لاحقاً بتشغيل هذا الجزء كعملية منفصلة
    print("فريق التمويل مستعد للعمل...")

# تشغيل البوت في مسار منفصل
def start_bot():
    bot.polling()

if __name__ == "__main__":
    # تشغيل البوت
    threading.Thread(target=start_bot).start()




