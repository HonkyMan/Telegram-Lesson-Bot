import sqlite3

def get_hws(db_name, number):
    answ = {'isok':False}
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute('SELECT * FROM students WHERE number=?', (number,))
    # print(cur.fetchall())
    if len(cur.fetchall())>0:
        answ['isok']=True
        hws = cur.execute('SELECT * FROM homeworks')
        hws = hws.fetchall()
        # print(hws.fetchall())
        rat = cur.execute('SELECT * FROM ratings WHERE number=?', (number,))
        # print(rat.fetchall())
        number_completed_tasks = 0
        outstanding_tasks = []
        rating = rat.fetchall()
        for i in range(len(rating)):
            for j in range(1, len(rating[i])):
                if ((str)(rating[i][j]) == '+'):
                    number_completed_tasks += 1
                else:
                    outstanding_tasks.append(hws[j-1])
        answ['done']=number_completed_tasks
        answ['hws']=outstanding_tasks
    con.close()
    return answ


def get_abs(db_name, number):
    ans = {'isok':False}
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute('SELECT * FROM students WHERE number=?', (number,))
    if len(cur.fetchall())>0:
        ans['isok']=True
        abs = cur.execute('SELECT * FROM absents WHERE number=?', (number,))
        abs = abs.fetchall()
        number_missed_classes = 0
        for i in range(len(abs)):
            for j in range(len(abs[i])):
                if ((str)(abs[i][j]) == '-'):
                    number_missed_classes += 1
        ans['absents']=number_missed_classes
    con.close()
    return ans



# if __name__=='__main__':
#     print(get_hws(db_name='db/lessons_db.db', number=222))
#
# if __name__=='__main__':
#     print(get_abs(db_name='db/lessons_db.db', number=222))