import telebot
import requests
import os

bot = telebot.TeleBot(os.environ.get('API_TOKEN'))
API_KEY = "ضعي_مفتاحك_هنا"
API_URL = "https://xklash.com/api/v2"

# 1. عرض زر الشراء
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    # زر شراء 100 عضو بـ 13 نجمة
    btn = telebot.types.InlineKeyboardButton("اشترِ 100 عضو بـ 13 نجمة ⭐", callback_data="buy_100")
    markup.add(btn)
    bot.send_message(message.chat.id, "أهلاً بك! اختر خدمتك:", reply_markup=markup)

# 2. معالجة طلب الشراء
@bot.callback_query_handler(func=lambda call: call.data == "buy_100")
def buy_stars(call):
    # إنشاء فاتورة دفع بالنجوم
    bot.send_invoice(
        call.message.chat.id,
        title="تمويل 100 عضو",
        description="خدمة إضافة 100 عضو لقناتك بسرعة",
        invoice_payload="order_100_members",
        currency="XTR", # عملة نجوم تليجرام
        prices=[telebot.types.LabeledPrice("100 عضو", 13)] # 13 نجمة
    )

# 3. معالجة نجاح الدفع وإرسال الطلب لـ xklash
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def payment_success(message):
    bot.reply_to(message, "✅ تم الدفع بنجاح! أرسلي الآن رابط القناة التي تريدين تمويلها:")
    
    # بعد إرسال الرابط، يتم تفعيل كود الـ API الذي كتبناه سابقاً
    @bot.message_handler(func=lambda m: "t.me" in m.text)
    def send_to_xklash(m):
        data = {'key': API_KEY, 'action': 'add', 'service': 50, 'link': m.text, 'quantity': 100}
        res = requests.post(API_URL, data=data).json()
        bot.reply_to(m, f"✅ تم إرسال طلبك للتمويل! رقم الطلب: {res.get('order')}")







