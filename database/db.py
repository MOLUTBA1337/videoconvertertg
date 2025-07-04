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



    def return_users(self):
        return self.c.execute("SELECT user_id FROM users;").fetchall()





