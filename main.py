import os
import telebot
from telebot import types
import subprocess

TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "أهلاً بك في بوت التمويل! أرسلي رابط القناة للبدء.")

@bot.message_handler(func=lambda message: "t.me" in message.text)
def handle_link(message):
    link = message.text
    bot.reply_to(message, "⏳ جاري تنفيذ التمويل...")
    # هنا البوت يستدعي سكربت الجيش للعمل
    subprocess.Popen(["python", "adder.py", link])
    bot.reply_to(message, "✅ تم إرسال الأمر لجيش الحسابات!")

bot.polling()






