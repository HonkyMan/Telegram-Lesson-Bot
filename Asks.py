from datetime import datetime
import sqlite3


def get_delete_ask(bot, db_name, user_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute('SELECT * FROM asks')
    asks = cur.fetchall()
    if len(asks) > 0:
        ask = asks[0]
        result = 'Вопрос: ' + ask[0] + '\n'
        result += 'Дата: ' + ask[1] + '\n'
        result += 'От: ' + ask[2]
        if (ask[3]):
            result += ' ' + ask[3]
        if (ask[4]):
            result += ' ' + ask[4]
        bot.send_message(user_id, result)
        cur.execute('delete from asks where id =(select min(id) from asks)')
        # cur.execute('DELETE FROM asks WHERE text='+ask[0])
        bot.send_message(user_id, "Вопрос удален.")
    else:
        bot.send_message(user_id, "Нет новых вопросов.")
    con.commit()
    con.close()


def send_answer(bot, db_name, user_id, channel, answer):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute('SELECT * FROM asks')
    asks = cur.fetchall()
    if len(asks) > 0:
        ask = asks[0]
        result = 'Вопрос: ' + ask[0] + '\n'
        result += answer
        bot.send_message(channel, result)
        cur.execute('delete from asks where id =(select min(id) from asks)')
        bot.send_message(user_id, "Вопрос удален.")

    con.commit()
    con.close()
