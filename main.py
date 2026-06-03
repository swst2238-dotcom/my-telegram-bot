# 1. استبدلي الزر في دالة start (غيرنا كلمة buy_100 إلى new_order)
btn = telebot.types.InlineKeyboardButton("طلب تمويل 100 عضو", callback_data="new_order")

# 2. استبدلي دالة المعالجة بهذا الكود (غيرنا الاسم لـ new_order)
@bot.callback_query_handler(func=lambda call: call.data == "new_order")
def buy_info(call):
    # هذا السطر ينهي التفاعل تماماً ويمنع تعليق الرسالة
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 
        "⭐ لطلب 100 عضو:\n\n"
        "1. قم بتحويل المقابل المادي لحسابي: @Jama2006A82\n"
        "2. بعد التحويل، أرسل كلمة 'تم التحويل' هنا.\n"
        "3. سأطلب منك رابط قناتك فوراً.")











