# coding=utf-8
import time
import random
import telebot
from telebot import types

bot = telebot.TeleBot("token")

print("Бот запущен\nСоедениние")
bot.send_message(-1001160331786, "Бот запущен")

@bot.message_handler(content_types=["new_chat_members"])
def default_test(message):
    bot.send_message(message.chat.id, "Привет! Обязательно прочитай [правила](https://t.me/animedev/101159).", parse_mode='Markdown')

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
                         + "Извините, вы администратор чата.\nИли уже забанены.",
                         parse_mode='Markdown')

@bot.message_handler(commands = ["mute"])
def mute(msg):
    try:
        if bot.get_chat_member(msg.chat.id, msg.from_user.id).status != "member":
            if bot.get_chat_member(msg.chat.id, msg.reply_to_message.from_user.id).status == "member":
                if msg.reply_to_message is not None:
                    if 1 < len(msg.text.split(" ")) < 3:
                        bantime = int(" ".join(msg.text.split(' ')[1:]))
                        if bantime > 30 and bantime < 9999999:
                            bot.send_message(msg.chat.id, "[{0}](tg://user?id={1}) "
                                             .format(msg.reply_to_message.from_user.first_name,
                                                     msg.reply_to_message.from_user.id, ) +
                                             "Забанен на " + str(bantime) + " сек ",
                                             parse_mode='Markdown')
                            bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id,
                                                     int(time.time() + bantime),
                                                     can_send_messages=False)
                        else:
                            bot.send_message(msg.chat.id,
                                             "Число " + str(
                                                 bantime) + " слишком большое или маленькое.\nДиапозон 30-9999999")
                    else:
                        bot.send_message(msg.chat.id, "Некоректное время")
                else:
                    bot.send_message(msg.chat.id, "Используй только реплаем!")
            else:
                bot.send_message(msg.chat.id, "Пользователь является администратором")
        else:
            bot.send_message(msg.chat.id, "Вы не администратор чата.")
    except ValueError:
        bot.send_message(msg.chat.id, "Некоректное время бана")


@bot.message_handler(commands = ["stop"])
def stop(msg):
    bot.send_message(-1001160331786, "Бот отключен")

if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=120)
