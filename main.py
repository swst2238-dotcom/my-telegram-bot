import telebot
import requests
import os

TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)

API_KEY = "b31916beaf30a275e6195d4ba79941a2"
API_URL = "https://xklash.com/api/v2"

# دالة لجلب الرصيد الحالي من الموقع
def get_balance():
    data = {'key': API_KEY, 'action': 'balance'}
    res = requests.post(API_URL, data=data).json()
    return float(res.get('balance', 0))

@bot.message_handler(commands=['balance'])
def check_balance(message):
    balance = get_balance()
    bot.reply_to(message, f"💰 رصيدك الحالي في الموقع هو: {balance} دولار.")

@bot.message_handler(func=lambda m: "t.me" in m.text)
def auto_order(m):
    balance = get_balance()
    # هنا نفترض تكلفة الطلب (مثلاً 0.5 دولار)
    cost = 0.5 
    
    if balance < cost:
        bot.reply_to(m, "⚠️ عذراً، الخدمة متوقفة حالياً للصيانة. يرجى التواصل مع الإدارة.")
        return

    bot.reply_to(m, "⏳ جاري تنفيذ طلبك...")
    
    data = {
        'key': API_KEY,
        'action': 'add',
        'service': 16225,
        'link': m.text,
        'quantity': 100
    }
    
    res = requests.post(API_URL, data=data).json()
    if 'order' in res:
        bot.reply_to(m, f"✅ تم التنفيذ بنجاح! رقم الطلب: {res['order']}")
    else:
        bot.reply_to(m, f"❌ خطأ تقني: {res}")

bot.infinity_polling()













