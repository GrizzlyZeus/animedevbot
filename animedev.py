''' Главный файл бота с его поведением '''
import sqlite3

import config  # Файл с токеном
import telebot

bot = telebot.TeleBot(config.token) # Обьявляем токен

class DBConnector:
    """Класс для простого управления файлом БД"""

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise

db = DBConnector("username.db")

# Языковые словари
class Language:
    """Класс хранящий переводы"""
    rus = dict(reptop='Топ репутации', msgtop='Топ сообщений')
    eng = dict(reptop='Top of reputation', msgtop='Top of messages')
    all = dict(botinchat="🇷🇺 Привет! Чтобы начать использовать бота,"+\
    " его нужно [настроить](t.me/animedev_bot?start=123).\n"+\
    "🇺🇸 Hello! To use bot, you should [setup](t.me/animedev_bot?start=123).")

class Controller():
    """ Тут методы для работы с данными """
    def topbymsgform(self, page=1, PageIsChanged=False):
        """" Формирует и отправляет топ по сообщениям """
        l = topbymsg(page)

        if l is not None:
            rank = page*10-10
            msgs = " "
            for i in len(l):
                msgs = msgs + "{rank}.{username}: {karma}\n".format(username=l[i][0],\
                karma=l[i][1], rank=rank)
                rank = rank + 1

            keyboard = telebot.types.InlineKeyboardMarkup()

            if topbymsg(page+1) != None: # Проверяем, есть ли следующяя страница
                callback_next = telebot.types.InlineKeyboardButton(text="→",\
                callback_data=["next", page])
                keyboard.add(callback_next)

            if page != 1:
                callback_back = telebot.types.InlineKeyboardButton(text="←",\
                callback_data=["back", page])
                keyboard.add(callback_back)

            if page == 1 and not PageIsChanged:
                bot.send_message(telebot.msg.chat.id, "Страница", page,\
                "\n" + msgs, reply_markup=keyboard)

            elif PageIsChanged:
                return [msgs, page]

        def topbymsg(listnum):
            """ Возвращает список участников по номеру страницы """

            with open(db) as database:
                sql = database.execute("SELECT name FROM users ORDER BY msgvalue DESC")

                sortednames = sql.fetchall()[listnum * 10 - 10:10 * listnum]
                newsort = []

                for i in range(10):
                    try:
                        name = sortednames.pop()[0]
                    except IndexError:
                        return None
                    data = [name,
                            database.execute("SELECT msgvalue FROM users WHERE name = ?",\
                            [(name)]).fetchall()[0][0]]
                    newsort.insert(0, data)
                return newsort

class Handlers:
    """Класс со всеми хендлерами"""
    def __init__(self):
        @bot.message_handler(content_types=['new_chat_members'])
        def welcome_handler(msg):
            """" Приветствует новых участников """
            bot.send_message(msg.chat.id, Language.all.get("botinchat"), parse_mode='Markdown')

        @bot.message_handler(commands=['topmsg'])
        def handle_top_msg():
            """ Топ сообщений по количеству """
            Controller.topbymsgform(1)

        @bot.message_handler(commands=['warning'])
        def handle_send_warning(msg):
            """ ВНИМАНИЕ """
            bot.send_message(msg.chat.id, "!!! ВНИМАНИЕ !!!\n"\
            + "Спасибо за внимание.", parse_mode='Markdown')

        @bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            """" Обработка обратного вызова """
            keyboard = telebot.types.InlineKeyboardMarkup()

            if call.message:
                if "next" in call.data:
                    msg = Controller.topbymsgform(call.data[1]+1, True)
                    bot.edit_message_text(chat_id=call.message.chat.id,\
                    message_id=call.message.message_id,\
                    text="Страница {}\n{}".format(msg[1], msg[0]),\
                    reply_markup=keyboard)
                elif "back" in call.data:
                    msg = Controller.topbymsgform(call.data[1]-1, True)
                    bot.edit_message_text(chat_id=call.message.chat.id,\
                    message_id=call.message.message_id,\
                    text="Страница {}\n{}".format(msg[1], msg[0]),\
                    reply_markup=keyboard)


if __name__ == '__main__':
    handlers = Handlers()
    bot.polling(none_stop=True)
