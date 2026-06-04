
from telebot import TeleBot, types

# 1. إعدادات البوت
TOKEN = '8822332836:AAENA3zWg6PuGq07QgmxbrlTu6GqYBZuQV0'
ADMIN_ID = '5531196107'
bot = TeleBot(TOKEN)

# 2. جدول الأسعار (العدد : عدد النجوم)
prices = {
    100: 10, 200: 20, 300: 30, 400: 40,
    500: 50, 600: 60, 700: 70, 800: 80, 900: 90
}

# 3. أمر البداية
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    for count, stars in prices.items():
        btn = types.InlineKeyboardButton(f"{count} عضو بـ {stars} نجمة", callback_data=f"buy_{count}")
        markup.add(btn)
    bot.send_message(message.chat.id, "مرحباً! اختر باقة التمويل التي تريدها:", reply_markup=markup)

# 4. معالجة اختيار الباقة وإرسال الفاتورة بالنجوم
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy(call):
    count = int(call.data.split('_')[1])
    stars_amount = prices[count]
    
    # إرسال فاتورة النجوم
    bot.send_invoice(
        chat_id=call.message.chat.id,
        title=f"شراء {count} عضو",
        description="تمويل القناة عبر نجوم تليجرام",
        payload=f"order_{count}",
        currency="XTR",
        prices=[types.LabeledPrice(label="السعر بالنجوم", amount=stars_amount)]
    )

# 5. الموافقة التلقائية على الدفع
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# 6. تأكيد الدفع وإبلاغك (أنتِ) بالطلب
@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    count = message.successful_payment.invoice_payload.split('_')[1]
    bot.reply_to(message, "✅ تم الدفع بنجاح! الآن أرسل رابط قناتك ليتم التمويل.")
    
    # انتظار الرابط
    bot.register_next_step_handler(message, send_to_admin, count)

def send_to_admin(message, count):
    link = message.text
    order_info = (f"⚠️ طلب تمويل جديد (مدفوع بالنجوم)!\n"
                  f"👤 المستخدم: @{message.from_user.username}\n"
                  f"🔢 العدد: {count} عضو\n"
                  f"🔗 الرابط: {link}\n\n"
                  f"يرجى تنفيذ التمويل فوراً!")
    
    bot.send_message(ADMIN_ID, order_info)
    bot.reply_to(message, "✅ تم استلام الرابط، سيتم تنفيذ طلبك في أسرع وقت.")

# تشغيل البوت
bot.polling()






















