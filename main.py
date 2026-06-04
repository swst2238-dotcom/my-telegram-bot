from telebot import TeleBot, types

# استبدلي بالتوكن الخاص بك
bot = TeleBot('8822332836:AAENA3zWg6PuGq07QgmxbrlTu6GqYBZuQV0')

# البداية وعرض الأزرار
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # إنشاء الأزرار
    for i in range(100, 1000, 100):
        btn = types.InlineKeyboardButton(f"{i} عضو بـ {i//10} نجمة", callback_data=f"buy_{i}")
        markup.add(btn)
    bot.send_message(message.chat.id, "مرحباً! اختر باقة التمويل التي تريدها:", reply_markup=markup)

# **هذا هو الجزء المفقود** - المسؤول عن الاستجابة للضغط
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_callback(call):
    # استخراج العدد من الضغطة
    count = call.data.split('_')[1]
    
    # الرد على المستخدم ليقوم بإرسال الرابط
    bot.answer_callback_query(call.id, text="تم الاختيار!")
    msg = bot.send_message(call.message.chat.id, f"لقد اخترت {count} عضو.\nالآن أرسل رابط القناة/المجموعة:")
    
    # حفظ العدد في الذاكرة مؤقتاً لنتمكن من استخدامه لاحقاً
    bot.register_next_step_handler(msg, process_link, count)

def process_link(message, count):
    link = message.text
    # إرسال إشعار لكِ (الإدارة)
    bot.send_message("5531196107", f"⚠️ طلب جديد!\nالمستخدم: @{message.from_user.username}\nالعدد: {count}\nالرابط: {link}")
    bot.reply_to(message, "✅ تم استلام طلبك، سيقوم المسؤول بتمويل قناتك قريباً.")

bot.polling()























