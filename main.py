from telebot import TeleBot, types
import os

# التوكن الصحيح الذي أرسلتِه
TOKEN = '8822332836:AAENA3zWg6PuGq07QgmxbrlTu6GqYBZuQV0'
ADMIN_ID = '5531196107'
bot = TeleBot(TOKEN)

# حذف أي ربط قديم لضمان العمل
bot.remove_webhook()

prices = {
    100: 10, 200: 20, 300: 30, 400: 40,
    500: 50, 600: 60, 700: 70, 800: 80, 900: 90
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for count, stars in prices.items():
        btn = types.InlineKeyboardButton(f"شراء {count} مشترك بـ {stars} نجمة", callback_data=f"buy_{count}")
        markup.add(btn)
    bot.send_message(message.chat.id, "مرحباً بك في بوت تمويل الدينار! اختر الخدمة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_callback(call):
    count = int(call.data.split('_')[1])
    stars_amount = prices[count]
    bot.send_invoice(
        chat_id=call.message.chat.id,
        title=f"شراء {count} مشترك",
        description=f"تمويل {count} مشترك حقيقي مقابل {stars_amount} نجمة",
        payload=f"order_{count}",
        currency="XTR",
        prices=[types.LabeledPrice(label="السعر بالنجوم", amount=stars_amount)]
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    count = message.successful_payment.invoice_payload.split('_')[1]
    msg = bot.reply_to(message, "✅ تم الدفع بنجاح! أرسل رابط قناتك الآن ليقوم المسؤول بالتمويل:")
    bot.register_next_step_handler(msg, process_link, count)

def process_link(message, count):
    link = message.text
    bot.send_message(ADMIN_ID, f"⚠️ طلب تمويل جديد (مدفوع)!\n👤 العضو: @{message.from_user.username}\n🔢 العدد: {count}\n🔗 الرابط: {link}")
    bot.reply_to(message, "✅ تم إرسال طلبك للإدارة، سيتم التنفيذ قريباً.")

bot.polling()

























