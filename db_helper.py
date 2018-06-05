import sqlite3


def prepare_db(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS students(
                  number TEXT PRIMARY KEY NOT NULL,
                  last_name TEXT NOT NULL,
                  first_name TEXT NOT NULL,
                  middle_name TEXT NOT NULL);''')

    cur.execute('''CREATE TABLE IF NOT EXISTS homeworks(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                name TEXT NOT NULL,
                description TEXT NOT NULL
                );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS ratings(
                number TEXT PRIMARY KEY NOT NULL,
                CONSTRAINT ratings_students_number_fk FOREIGN KEY (number) 
                REFERENCES students (number) ON DELETE CASCADE ON UPDATE CASCADE
                );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS absents(
                number TEXT PRIMARY KEY NOT NULL,
                CONSTRAINT absents_students_number_fk FOREIGN KEY (number)
                REFERENCES students (number) ON DELETE CASCADE ON UPDATE CASCADE
                );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS asks(
                  text TEXT NOT NULL,
                  date TEXT NOT NULL,
                  first_name TEXT NOT NULL,
                  username TEXT,
                  last_name TEXT
                  );''')
    cur.execute('SELECT * FROM homeworks;')
    hws_count = len(cur.fetchall())
    cur.execute('UPDATE sqlite_sequence SET seq=? WHERE name=\'homeworks\';', (hws_count,))
    cur.execute('SELECT * FROM absents;')
    days_count = len(list(map(lambda x: x[0], cur.description))) - 1
    cur.execute('SELECT * FROM sqlite_sequence WHERE name=\'absents\'')
    if len(cur.fetchall()) == 0:
        cur.execute('INSERT INTO sqlite_sequence(name, seq) VALUES (\'absents\', ?);', (days_count,))
    else:
        cur.execute('UPDATE sqlite_sequence SET seq=? WHERE name=\'absents\';', (days_count,))

    conn.commit()
    conn.close()


def execute_select(db_name, sql):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    result = cur.execute(sql).fetchall()
    conn.close()
    return result


def add_student(db_name, args):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('SELECT * FROM students WHERE number=?', (args[0],))
    if len(cur.fetchall()) == 0:
        cur.execute(
            'INSERT INTO students(number, last_name, first_name, middle_name) VALUES (?,?,?,?);',
            (args[0], args[1], args[2], args[3]))
        cur.execute('INSERT INTO ratings(number) VALUES (?)', (args[0],))
        cur.execute('INSERT INTO absents(number) VALUES (?)', (args[0],))
        conn.commit()
    conn.close()


def delete_student(db_name, arg):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('SELECT * FROM students WHERE number=?', (arg,))
    if len(cur.fetchall()) > 0:
        cur.execute('DELETE FROM students WHERE number=?', (arg,))
        cur.execute('DELETE FROM ratings WHERE number=?', (arg,))
        cur.execute('DELETE FROM absents WHERE number=?', (arg,))
    conn.commit()
    conn.close()


def add_hw(db_name, args):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('INSERT INTO homeworks(name, description) VALUES (?,?);', (args[0], args[1]))
    cur.execute('SELECT seq FROM sqlite_sequence WHERE name=\'homeworks\';')
    count = cur.fetchall()
    cur.execute('ALTER TABLE ratings ADD hw_{} TEXT DEFAULT \'-\' NOT NULL;'.format(count[0][0]))
    conn.commit()
    conn.close()


def delete_hw(db_name, id):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('SELECT * FROM homeworks WHERE id=?', (id,))
    if len(cur.fetchall()) > 0:

        cur.execute('DELETE FROM homeworks WHERE id=?;', (id,))
        cur.execute('SELECT id FROM homeworks')

        hw_ids = cur.fetchall()
        cur.execute('''CREATE TABLE ratings_tmp(number TEXT PRIMARY KEY NOT NULL,
                        CONSTRAINT ratings_students_number_fk FOREIGN KEY (number) REFERENCES students(number)
                        ON DELETE CASCADE ON UPDATE CASCADE);''')

        for i in range(len(hw_ids)):
            cur.execute('ALTER TABLE ratings_tmp ADD hw_{} TEXT DEFAULT \'-\' NOT NULL;'.format(str(i + 1)))

        query = 'INSERT INTO ratings_tmp SELECT number'
        for hw_id in hw_ids:
            query += ', hw_' + str(hw_id[0])
        query += ' FROM ratings;'
        cur.execute(query)

        cur.execute('DROP TABLE ratings;')
        cur.execute('ALTER TABLE ratings_tmp RENAME TO ratings;')

        for i in range(len(hw_ids)):
            cur.execute('UPDATE homeworks SET id={} WHERE id=?'.format(str(i + 1)), (str(hw_ids[i][0]),))
        cur.execute('UPDATE sqlite_sequence SET seq={} WHERE name=\'homeworks\''.format(len(hw_ids)))
        conn.commit()

    conn.close()


def delete_hws(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute('DELETE FROM homeworks;')
    cur.execute(
        'CREATE TABLE ratings_tmp(number TEXT PRIMARY KEY NOT NULL, CONSTRAINT ratings_students_number_fk FOREIGN KEY (number) REFERENCES students(number) ON DELETE CASCADE ON UPDATE CASCADE);')

    cur.execute('INSERT INTO ratings_tmp SELECT number FROM ratings;')
    query = 'DROP TABLE ratings;'
    cur.execute(query)

    query = 'ALTER TABLE ratings_tmp RENAME TO ratings;'
    cur.execute(query)

    cur.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name = \'homeworks\'')

    conn.commit()
    conn.close()


def add_absents_column(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('SELECT seq FROM sqlite_sequence WHERE name=\'absents\';')
    count = cur.fetchall()[0][0] + 1
    cur.execute('ALTER TABLE absents ADD day_{} TEXT DEFAULT \'-\' NOT NULL;'.format(count, ))
    cur.execute('UPDATE sqlite_sequence SET seq = ? WHERE name = \'absents\';', (count,))
    conn.commit()
    conn.close()


def delete_students(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('DELETE FROM students;')
    cur.execute('DELETE FROM ratings;')
    cur.execute('DELETE FROM absents')
    conn.commit()
    conn.close()


def recreate_absents(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('DROP TABLE absents')
    cur.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name=\'absents\'')
    cur.execute(
        '''CREATE TABLE absents(
            number TEXT PRIMARY KEY NOT NULL,
            CONSTRAINT absents_students_number_fk FOREIGN KEY (number)
            REFERENCES students (number) ON DELETE CASCADE ON UPDATE CASCADE)''')
    conn.commit()
    conn.close()


def recreate_ratings(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('DROP TABLE ratings')
    cur.execute(
        '''CREATE TABLE ratings(
            number TEXT PRIMARY KEY NOT NULL,
            CONSTRAINT ratings_students_number_fk FOREIGN KEY (number)
            REFERENCES students (number) ON DELETE CASCADE ON UPDATE CASCADE);''')
    cur.execute('SELECT seq FROM sqlite_sequence WHERE name=\'homeworks\';')
    count = cur.fetchall()[0][0]
    for i in range(count):
        cur.execute('ALTER TABLE ratings ADD hw_{} TEXT DEFAULT \'-\' NOT NULL;'.format(i + 1))
    conn.commit()
    conn.close()


def add_absent(db_name, val):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('INSERT INTO absents VALUES (' + ','.join(val) + ');')
    conn.commit()
    conn.close()


def update_rating(db_name, val):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('DELETE FROM ratings WHERE number=?;',(val[0],))
    cur.execute('INSERT INTO ratings VALUES (' + ','.join(val) + ');')
    conn.commit()
    conn.close()
