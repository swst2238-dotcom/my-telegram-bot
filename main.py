import telebot

TOKEN = '8822332836:AAHvDv6ccQAQt0Mm70iJlFR8mJBbxlwsD70'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "مرحباً Najah، أنا أعمل الآن!")

bot.polling()
