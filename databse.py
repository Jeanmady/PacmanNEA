import sqlite3 as sql
from Current_score import *

"""cur.execute( CREATE TABLE Users (
            UserID integer PRIMARY KEY AUTOINCREMENT,
            Username text NOT NULL,
            Password text NOT NULL,
             Highscore integer,
            FOREIGN KEY(UserID)
               REFERENCES friends(AddresseeID)
            FOREIGN KEY(UserID)
               REFERENCES friends(RequesteeID)))"""





#c.execute(""" CREATE TABLE Friends(
#            AddresseeID integer PRIMARY KEY,
#            RequesteeID integer NOT NULL,
#            Accepted integer NOT NULL
#            )""")
"""conn = sql.connect('usernamedatabase')
c = conn.cursor()
c.execute(INSERT INTO Users (Username, Password)
            VALUES 
                ("Jeanmady", "password")
            )
conn.commit()
conn.close()"""

conn = sql.connect("usernamedatabase")
cur = conn.cursor()
"""cur.execute( CREATE TABLE Current (
            Playing integer PRIMARY KEY AUTOINCREMENT,
            Username text NOT NULL,
            UserID integer NOT NULL,
            Highscore integer,
            Score integer )"""

"""cur.execute(INSERT INTO Current(Username, UserID, Highscore, Score)
                VALUES("test", 5, 5, 0)"""


cur.execute("SELECT * FROM Users")
record = cur.fetchall()
for item in record:
    print(item)
conn.commit()
conn.close()



class DatabaseActions():
    def __init__(self, menu):
        self.menu = menu
        self.currentID = ''
        self.currentHighscore = ''

    ################ Users table#############################

    def create_username(self, username, passw, repassw):
        conn = sql.connect('usernamedatabase')
        c = conn.cursor()
        c.execute("SELECT UserID FROM Users WHERE Username = ?", (username,))
        data=c.fetchall()
        if len(data)!=0:
            print('Username already exists')# add error messege
        elif repassw != passw:
            print("Passwords dont match")# add error message
        else:
            print("created")
            c.execute(""" INSERT INTO Users
                        (Username, Password, Highscore)
                        VALUES
                        (?,?,?)
                        """,(username, passw, '0'))
            conn.commit()
            conn.close()
            return True
        conn.close()

    def get_highscore(self, username):
        conn = sql.connect('usernamedatabase')
        c = conn.cursor()
        c.execute("SELECT Highscore FROM Users WHERE Username = ?", (username,))
        check_highscore = c.fetchall()
        check_highscore = str(check_highscore)
        High = check_highscore[2:-3]
        return High

    def get_ID(self, username):
        conn = sql.connect('usernamedatabase')
        c = conn.cursor()
        c.execute("SELECT UserID FROM Users WHERE Username = ?", (username,))
        data=c.fetchall()
        data = str(data)
        ID = data[2:-3]
        conn.close()
        return ID

    def check_login(self, username, passw):
        conn = sql.connect('usernamedatabase')
        c = conn.cursor()
        c.execute("SELECT Password FROM Users WHERE Username = ?", (username,))
        check_pass = c.fetchall()
        if len(check_pass)!=0:
            for item in check_pass:
                acc_pass = ','.join(item) # changes tuple output into string to be able to compare
        else:
            print('Username does not exists')# add error messege
        if str(passw) == acc_pass:
            print("accepted")
            c.execute("SELECT UserID FROM Users WHERE Username = ?", (username,))
            data=c.fetchall()
            data = str(data)
            self.currentID = data[2:-3]
            self.currentHighscore = self.get_highscore(currentID)
            return True
        else:
            print("incorrect password")
        conn.close()

    def move_to_playing_database(self, username, currentID, currentHighscore):
        conn = sql.connect("usernamedatabase")
        cur = conn.cursor()
        cur.execute("""UPDATE Current
                        SET Username = ?, 
                            UserID = ?, 
                            Highscore = ?
                        WHERE Playing = 1
                        """, (username, currentID, currentHighscore))
        conn.commit()
        conn.close()

    ################# Current Table #######################

    def update_score(self, score):
        conn = sql.connect("usernamedatabase")
        cur = conn.cursor()
        cur.execute("""UPDATE Current SET Score = ? WHERE Playing = 1""", (score,))
        conn.commit()
        conn.close()

    def get_current_score(self):
        conn = sql.connect('usernamedatabase')
        c = conn.cursor()
        c.execute("SELECT Score FROM Current WHERE Playing = 1")
        check_score = c.fetchall()
        check_score = str(check_score)
        Score = check_score[2:-3]
        return Score

    def get_current_highscore(self):
        conn = sql.connect('usernamedatabase')
        c = conn.cursor()
        c.execute("SELECT Highscore FROM Current WHERE Playing = 1")
        check_score = c.fetchall()
        check_score = str(check_score)
        Score = check_score[2:-3]
        return Score



    

            
            


        
    
 
