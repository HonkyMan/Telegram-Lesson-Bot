import sqlite3
def add_student(db_name, args):
    conn= sqlite3.connect(db_name)
    cur=conn.cursor()
    cur.execute('SELECT * FROM WHERE number=?', (args[0],))
    if len(cur.fetchall)==0:
        cur.execute('INSERT INTO students(number,last_name, first_name, middle_name) VALUES (?,?,?,?);', (args[0],args[1],args[2],args[3]))
        cur.execute('INSERT INTO ratings(number) VALUES(?)', (args[0],))
        cur.execute('INSERT INTO absents(number) VALUES(?)', (args[0],))
    conn.commit()
    conn.close()

def delete_student(db_name, arg):
    conn= sqlite3.connect(db_name)
    cur=conn.cursor()
    cur.execute('SELECT * FROM WHERE number=?', (arg,))
    if len(cur.fetchall)>0:
        cur.execute('DELETE FROM students WHERE number=?',(arg,))
        cur.execute('DELETE FROM ratings WHERE number=?', (arg,))
        cur.execute('DELETE FROM absents WHERE number=?', (arg,))
    conn.commit()
    conn.close()
