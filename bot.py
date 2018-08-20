import telebot
import time
import sqlite3
import config #файл с токеном
import text
from telebot import types

textrus = dict(reptop='Топ репутации', msgtop='Топ сообщений')
texteng = dict(reptop='Top of reputation', msgtop='Top of message')
textruseng = dict(botinchat='''🇷🇺 Привет, что бы испльзовать мои функции,
вам сначало надо [настроить](t.me/animedev_bot?start=123) меня.
🇺🇸 Hello, if you want to use a bot, 
you should [set settings](t.me/animedev_bot?start=123) for me.''')

bot = telebot.TeleBot(config.token) #обьявляем токен

class DataConn:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise

@bot.message_handler(content_types = ['new_chat_members'])
def message_handler(msg):
    bot.send_message(msg.chat.id, textruseng.get("botinchat") , parse_mode= 'Markdown')

@bot.message_handler(commands=['topmsg'])
def handle_top_ms(msg):
    def topbymsg(listnum):
        conn = sqlite3.connect("username.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()
        sql = cursor.execute("SELECT name FROM users ORDER BY msgvalue DESC")
        sortednames = sql.fetchall()[listnum * 10 - 10:10 * listnum]
        newsort = []
        for i in range(10):
            try:
                name = sortednames.pop()[0]
            except IndexError:
                return None
            data = [name,
                    cursor.execute("SELECT msgvalue FROM users WHERE name = ?", [(name)]).fetchall()[0][0]]
            newsort.insert(0, data)
        return newsort
    l1 = topbymsg(2)
    l = topbymsg(1)
    if l1 is not None:
        msgs = " "
        for i in range(10):
            msgs = msgs + "{username}: {karma}\n".format(username=l[i][0], karma=l[i][1])
            print(msgs)
        keyboard = types.InlineKeyboardMarkup()
        callback_next = types.InlineKeyboardButton(text="▶", callback_data="next")
        keyboard.add(callback_next)
        bot.send_message(msg.chat.id, "страница 1\n" + msgs, reply_markup=keyboard)
    if l1 is None:
        msgs = " "
        for i in range(10):
            msgs = msgs + "{username}: {karma}\n".format(username=l[i][0], karma=l[i][1])
            print(msgs)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    def topbymsg(listnum):
        conn = sqlite3.connect("username.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()
        sql = cursor.execute("SELECT name FROM users ORDER BY msgvalue DESC")
        sortednames = sql.fetchall()[listnum * 10 - 10:10 * listnum]
        newsort = []
        for i in range(10):
            try:
                name = sortednames.pop()[0]
            except IndexError:
                return None
            data = [name,
                    cursor.execute("SELECT msgvalue FROM users WHERE name = ?", [(name)]).fetchall()[0][0]]
            newsort.insert(0, data)
        return newsort
    keyboard = types.InlineKeyboardMarkup()
    if call.message:
        if call.data == "next":
            l1 = 1
            l = topbymsg(l1)
            msgs = " "
            l1 = l1 + 1
            for i in range(10):
                if l1 is not None:
                    msgs = " "
                    for i in range(10):
                        msgs = msgs + "{username}: {karma}\n".format(username=l[i][0], karma=l[i][1])
                        print(msgs)
                    keyboard = types.InlineKeyboardMarkup()
                    callback_next = types.InlineKeyboardButton(text="▶", callback_data="next")
                    keyboard.add(callback_next)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Страница {}\n{}".format(str(l1), msgs), reply_markup=keyboard)





if __name__ == '__main__':
   bot.polling(none_stop=True)

