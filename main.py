import os
import telebot
from telebot import types

TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 1. أمر البداية مع الأزرار
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    # إنشاء الأزرار
    btn1 = types.InlineKeyboardButton("زر الترحيب", callback_data="hello")
    btn2 = types.InlineKeyboardButton("زر المساعدة", callback_data="help")
    btn3 = types.InlineKeyboardButton("زر الموقع", url="https://railway.com")
    
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "أهلاً بكِ يا Najah! اختاري خدمة من القائمة:", reply_markup=markup)

# 2. معالجة الضغط على الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "hello":
        bot.answer_callback_query(call.id, "جاري الرد...")
        bot.send_message(call.message.chat.id, "مرحباً بكِ في خدمتنا المميزة! 😊")
    elif call.data == "help":
        bot.answer_callback_query(call.id, "جاري الرد...")
        bot.send_message(call.message.chat.id, "كيف يمكنني مساعدتك اليوم؟ أنا هنا لخدمتك.")

# 3. معالجة النصوص العادية
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "أنا لا أفهم هذا الأمر، جربي الضغط على /start")

print("البوت يعمل بانتظار الأوامر...")
bot.polling()

