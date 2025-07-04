import sqlite3

class Users:
    def __init__(self,id: int):
        self.db = sqlite3.connect('database/all.db')
        self.c = self.db.cursor()
        self.id = id
        self.c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        count INTEGER,
        ref_id INTEGER
        )
        """)

    def add_user(self,ref_id=None):
        if not ref_id or not ref_id.isdigit():

            check = self.c.execute("SELECT * FROM users WHERE user_id = ?;",(self.id,)).fetchone()
            if not check:
                self.c.execute("INSERT INTO users(user_id,count,ref_id) VALUES(?,?,?)",(self.id,1,0))
                self.db.commit()
        else:
            check1 = self.c.execute("SELECT * FROM users WHERE user_id = ?;", (ref_id,)).fetchone()
            check2 = self.c.execute("SELECT * FROM users WHERE user_id = ?;", (self.id,)).fetchone()
            if check1 and not check2:
                self.c.execute("UPDATE users SET count = count + ? WHERE user_id = ?;",(1,ref_id,))
                self.c.execute("INSERT INTO users(user_id,count,ref_id) VALUES(?,?,?)",(self.id,1,ref_id))
                self.db.commit()
            elif not check1 and not check2:
                self.c.execute("INSERT INTO users(user_id,count,ref_id) VALUES(?,?,?)", (self.id, 1, 0))
                self.db.commit()

    def return_count(self) -> int:
        return self.c.execute("SELECT count FROM users WHERE user_id = ?;", (self.id,)).fetchone()

    def add_count(self,count):
        self.c.execute('UPDATE users SET count = count + ? WHERE user_id = ?;',(count,self.id))
        self.db.commit()

    def minus_count(self,count):
        self.c.execute('UPDATE users SET count = count - ? WHERE user_id = ?;',(count,self.id))
        self.db.commit()

    def return_users(self):
        return self.c.execute("SELECT user_id FROM users;").fetchall()


class Promo:
    def __init__(self):
        self.db = sqlite3.connect('database/all.db')
        self.c = self.db.cursor()

        self.c.execute("""CREATE TABLE IF NOT EXISTS promocode(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        promo TEXT,
        count INTEGER,
        words TEXT
        )
        """)
        self.c.execute("""CREATE TABLE IF NOT EXISTS used_promo(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        promo TEXT
        )
        """)

    def add_promo(self, promo: str, count: int, words: str):
        self.c.execute("INSERT INTO promocode(promo,count,words) VALUES(?,?,?);",(promo,count,words))
        self.db.commit()
        return '<b>Промокод успешно добавлен!</b>'

    def use_promo(self,user_id: int,promo: str):

        check_user = self.c.execute("SELECT user_id FROM used_promo WHERE user_id = ? AND promo = ?;", (user_id,promo)).fetchone()
        if check_user:
            return '<b>Вы уже использовали этот промокод!</b>'

        check_promo = self.c.execute("SELECT count FROM promocode WHERE promo = ?;", (promo,)).fetchone()

        if not check_promo:
            self.c.execute("DELETE FROM used_promo WHERE promo = ?;", (promo,))
            self.db.commit()
            return '<b>Такого промокода либо не существует, либо он исчерпан!</b>'

        elif int(check_promo[0]) == 0:
            self.c.execute("DELETE FROM promocode WHERE promo = ?;", (promo,))
            self.c.execute("DELETE FROM used_promo WHERE promo = ?;", (promo,))
            self.db.commit()
            return '<b>Такого промокода либо не существует, либо он исчерпан!</b>'

        elif 'count' in promo.lower():
            counts = self.c.execute("SELECT words FROM promocode WHERE promo = ?;", (promo,)).fetchone()
            self.c.execute('UPDATE users SET count = count + ? WHERE user_id = ?;', (int(counts[0]), user_id))

            self.c.execute("UPDATE promocode SET count = count - 1 WHERE promo = ?", (promo,))
            self.c.execute("INSERT INTO used_promo(user_id,promo) VALUES(?,?)", (user_id,promo))
            self.db.commit()
            return f'<b>Вы активировали {counts[0]} видео-конвертации!</b>'


        else:
            words = self.c.execute("SELECT words FROM promocode WHERE promo = ?;",(promo,)).fetchone()
            self.c.execute("UPDATE promocode SET count = count - 1 WHERE promo = ?", (promo,))
            self.c.execute("INSERT INTO used_promo(user_id,promo) VALUES(?,?)", (user_id,promo))
            self.db.commit()
            return words[0]


