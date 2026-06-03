import telebot

TOKEN = '8822332836:AAENA3zWg6PuGq07QgmxbrlTu6GqYBZuQV0'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "مرحباً Najah، أنا أعمل الآن!")

bot.polling()
