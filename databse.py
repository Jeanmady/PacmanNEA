import sqlite3 as sql

#c.execute(""" CREATE TABLE Users (
#            UserID integer PRIMARY KEY,
#            Username text NOT NULL,
#            Password text NOT NULL,
#            Highscore integer,
 #           FOREIGN KEY(UserID)
 #              REFERENCES friends(AddresseeID)
 #           FOREIGN KEY(UserID)
#               REFERENCES friends(RequesteeID))""")


#c.execute(""" CREATE TABLE Friends(
#            AddresseeID integer PRIMARY KEY,
#            RequesteeID integer NOT NULL,
#            Accepted integer NOT NULL
#            )""")
conn = sql.connect('usernamedatabase')
c = conn.cursor()

conn.commit()
conn.close()

class DatabaseActions():
    def __init__(self, menu):
        self.menu = menu
        
    def create_username(self):
        conn = sql.connect('usernamedatabase')
        c = conn.cursor()
        
        conn.commit()
        conn.close()
 
