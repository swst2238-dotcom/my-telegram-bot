from telebot import TeleBot, types

# استبدلي هذا بـ Token الخاص ببوتكِ
bot = TeleBot('8822332836:AAENA3zWg6PuGq07QgmxbrlTu6GqYBZuQV0')
ADMIN_ID = '5531196107'

# جدول الأسعار بالنجوم
prices = {
    100: 10, 200: 20, 300: 30, 400: 40,
    500: 50, 600: 60, 700: 70, 800: 80, 900: 90
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    for count, stars in prices.items():
        btn = types.InlineKeyboardButton(f"{count} عضو بـ {stars} نجمة", callback_data=f"buy_{count}")
        markup.add(btn)
    bot.send_message(message.chat.id, "مرحباً بك في متجر Najah!\nاختر باقة الأعضاء التي تريدها:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy(call):
    count = call.data.split('_')[1]
    msg = bot.send_message(call.message.chat.id, f"لقد اخترت {count} عضو.\nالآن أرسل رابط القناة/المجموعة ليتم إبلاغ الإدارة:")
    bot.register_next_step_handler(msg, get_link, count)

def get_link(message, count):
    link = message.text
    # إرسال إشعار لكِ (الإدارة)
    order_info = (f"⚠️ طلب تمويل جديد!\n"
                  f"👤 المستخدم: @{message.from_user.username}\n"
                  f"🔢 العدد: {count} عضو\n"
                  f"🔗 الرابط: {link}")
    
    bot.send_message(ADMIN_ID, order_info)
    bot.reply_to(message, "✅ تم استلام طلبك بنجاح! سيتم تنفيذ التمويل قريباً.")

bot.polling()






















