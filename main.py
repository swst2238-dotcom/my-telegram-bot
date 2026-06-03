import os
import telebot

# هذا السطر يجلب التوكن من إعدادات Railway (التي وضعناها في Variables)
TOKEN = os.environ.get('API_TOKEN')

# تعريف البوت
bot = telebot.TeleBot(TOKEN)

# كود للرد على أي رسالة
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "أهلاً بكِ يا Najah! البوت يعمل الآن بنجاح.")

# تشغيل البوت
print("البوت يعمل الآن...")
bot.polling()
