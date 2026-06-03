# 1. استبدلي الزر في دالة start (غيرنا كلمة buy_100 إلى new_order)
btn = telebot.types.InlineKeyboardButton("طلب تمويل 100 عضو", callback_data="new_order")

# 2. استبدلي دالة المعالجة بهذا الكود (غيرنا الاسم لـ new_order)
@bot.callback_query_handler(func=lambda call: call.data == "new_order")
def buy_info(call):

# 1. استقبال كلمة "تم التحويل"
@bot.message_handler(func=lambda message: message.text == "تم التحويل")
def ask_for_screenshot(message):
    bot.send_message(message.chat.id, "✅ تمام، أرسلي صورة (سكرين شوت) للتحويل الآن.")

# 2. استقبال الصورة وإرسالها لك للمراجعة
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # رقم الـ ID الخاص بك (يجب أن تعرفيه)
    YOUR_ID = 'YOUR_TELEGRAM_ID_HERE' 
    
    # إرسال الصورة لك
    bot.send_photo(YOUR_ID, message.photo[-1].file_id, caption=f"طلب جديد من المستخدم: {message.chat.id}")
    bot.send_message(YOUR_ID, "هل تم استلام المبلغ؟", reply_markup=create_admin_buttons(message.chat.id))
    
    bot.send_message(message.chat.id, "⏳ جاري مراجعة التحويل من قبل الإدارة، لحظات وسيبدأ التمويل.")

# 3. أزرار التحكم لكِ (بصفتك الأدمن)
def create_admin_buttons(user_id):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("تم الاستلام (ابدأ التمويل)", callback_data=f"approve_{user_id}"))
    return markup

    # هذا السطر ينهي التفاعل تماماً ويمنع تعليق الرسالة
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 
        "⭐ لطلب 100 عضو:\n\n"
        "1. قم بتحويل المقابل المادي لحسابي: @Jama2006A82\n"
        "2. بعد التحويل، أرسل كلمة 'تم التحويل' هنا.\n"
        "3. سأطلب منك رابط قناتك فوراً.")











