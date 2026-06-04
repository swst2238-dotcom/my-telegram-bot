import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import requests
import os
from pycricryptopay import CryptoPay

# إعدادات البوت
TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)
crypto = CryptoPay("591551:AAaCLeCJ3KRPZbR6Cj6Dg1eqq1iLisbkz7P")

API_KEY = "b31916beaf30a275e6195d4ba79941a2"
API_URL = "https://xklash.com/api/v2"

# دالة تنظيم الأزرار (20 زر - 4 أعمدة في 5 صفوف)
def main_menu():
    markup = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(f"خـدمة {i}", callback_data=f"service_{i}") for i in range(1, 21)]
    
    # توزيع الأزرار في صفوف (كل صف يحتوي 4 أزرار)
    for i in range(0, 20, 4):
        markup.row(*buttons[i:i+4])
        
    markup.add(InlineKeyboardButton("⬅️ العودة للرئيسية", callback_data="back_main"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛒 المتجر", "💳 شحن الرصيد", "👤 حسابي")
    bot.send_message(message.chat.id, "🔥 **بوت ليفاندوسكي 9**\nأفضل خدمات التمويل الآلي.", reply_markup=kb, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🛒 المتجر")
def shop(message):
    bot.send_message(message.chat.id, "📋 **قائمة الخدمات:**\nاختر الخدمة المطلوبة من الجدول أدناه:", reply_markup=main_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "💳 شحن الرصيد")
def deposit(message):
    try:
        invoice = crypto.create_invoice(asset="USDT", amount=1)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💰 دفع 1 USDT", url=invoice.pay_url))
        bot.reply_to(message, "💳 **مركز الشحن:**\nاضغط على الزر للتحويل الآلي.", reply_markup=markup, parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "❌ خطأ في الاتصال بمحفظة الشحن.")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "back_main":
        bot.edit_message_text("🏠 القائمة الرئيسية:", call.message.chat.id, call.message.message_id, reply_markup=None)
        start(call.message)
    elif call.data.startswith("service_"):
        service_id = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"تم اختيار {service_id}")
        bot.send_message(call.message.chat.id, f"✅ **الخدمة {service_id}**\nأرسل رابط القناة للبدء.")

bot.infinity_polling()


















