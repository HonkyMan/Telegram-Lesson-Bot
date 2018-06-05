from datetime import datetime
import sqlite3


def save_ask(bot, db_name, message, user_id, ask):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # print(message.from_user)
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    cur.execute('INSERT INTO asks(text,date,first_name, username, last_name) VALUES(?,?,?,?,?)',
                (ask, date, first_name, username, last_name))
    cur.execute('SELECT * FROM asks WHERE text=?', (ask,))
    if len(cur.fetchall()) > 0:
        bot.send_message(user_id, "Ваш вопрос успешно отправлен.")
    else:
        bot.send_message(user_id, "Ошибка отправки вопроса.")
    conn.commit()
    conn.close()


def get_ask(bot, db_name, user_id):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('SELECT * FROM asks')
    asks = cur.fetchall()
    if len(asks) > 0:
        ask = asks[0]
        result = 'Вопрос: ' + ask[0] + '\n'
        result += 'Дата: ' + ask[1] + '\n'
        result += 'От: ' + ask[2]
        if ask[3]:
            result += ' ' + ask[3]
        if ask[4]:
            result += ' ' + ask[4]
        bot.send_message(user_id, result)
    else:
        bot.send_message(user_id, "Нет новых вопросов.")
    conn.close()
