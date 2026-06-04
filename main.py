import telebot
import requests
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)
CRYPTO_TOKEN = "591551:AAaCLeCJ3KRPZbR6Cj6Dg1eqq1iLisbkz7P"

def main_menu():
    markup = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(f"خـدمة {i}", callback_data=f"service_{i}") for i in range(1, 21)]
    for i in range(0, 20, 4):
        markup.row(*buttons[i:i+4])
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛒 المتجر", "💳 شحن الرصيد")
    bot.send_message(message.chat.id, "🔥 بوت ليفاندوسكي 9 جاهز", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "🛒 المتجر")
def shop(message):
    bot.send_message(message.chat.id, "قائمة الخدمات:", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "💳 شحن الرصيد")
def deposit(message):
    # استخدام requests مباشرة بدلاً من المكتبة المعقدة
    headers = {'Crypto-Pay-API-Token': CRYPTO_TOKEN}
    data = {'asset': 'USDT', 'amount': '1'}
    try:
        response = requests.post('https://pay.crypt.bot/api/createInvoice', headers=headers, json=data).json()
        pay_url = response['result']['pay_url']
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💰 ادفع الآن", url=pay_url))
        bot.reply_to(message, "اضغط للدفع:", reply_markup=markup)
    except:
        bot.reply_to(message, "خطأ في الاتصال بالسيرفر")

bot.infinity_polling(none_stop=True)



















