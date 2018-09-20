import time
import random
import telebot
from telebot import types

bot = telebot.TeleBot("634522342:AAHWAJrI3Mkp1_2KcHkwkQg7SwURtoA2nlA")


@bot.message_handler(content_types=["new_chat_members"])
def default_test(message):
    bot.restrict_chat_member(message.chat.id, message.from_user.id, 1, False)
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Зайти в чат", callback_data="test")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и прочитай [правила](https://t.me/animedev/101159).", reply_markup=keyboard, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "test":
            bot.restrict_chat_member(call.message.chat.id, call.from_user.id, can_send_messages = True)


@bot.message_handler(commands=["banme"])
def default_tesdt(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status == "member":
        rand = random.randint(100, 1000)
        bot.send_message(message.chat.id,
                         "[{0}](tg://user?id={1}) ".format(message.from_user.first_name, message.from_user.id)
                         + "СОЖЖЕН. По собственному желанию." + "\nНа " + str(rand) + " сек.",
                         parse_mode='Markdown')
        bot.restrict_chat_member(message.chat.id, message.from_user.id, int(time.time() + rand),
                                 can_send_messages=False)
    else:
        bot.reply_to(message,
                         "[{0}](tg://user?id={1}) ".format(message.from_user.first_name, message.from_user.id)
                         + "Извините, вы администратор чата.",
                         parse_mode='Markdown')


if __name__ == '__main__':
    bot.polling(none_stop=True)
