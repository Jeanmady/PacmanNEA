import sqlite3 as sql

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
cur.execute("SELECT * FROM Users")
record = cur.fetchall()
for item in record:
    print(item)
conn.commit()
conn.close()



class DatabaseActions():
    def __init__(self, menu):
        self.menu = menu

    def create_username(self):
        conn = sql.connect('usernamedatabase')
        c = conn.cursor()
        c.execute("SELECT UserID FROM Users WHERE Username = ?", (self.menu.inp_username,))
        data=c.fetchall()
        if len(data)!=0:
            print('Username already exists')# add error messege
        elif self.menu.inp_repass != self.menu.inp_pass:
            print("Passwords dont match")# add error message
        else:
            print("lol")
            c.execute(""" INSERT INTO Users
                        (Username, Password)
                        VALUES
                        (?,?)
                        """,(self.menu.inp_username, self.menu.inp_repass))
            
        
            conn.commit()
        conn.close()

    def check_login(self):
        conn = sql.connect('usernamedatabase')
        c = conn.cursor()
        c.execute("SELECT Password FROM Users WHERE Username = ?", (self.menu.inp_username,))
        data=c.fetchall()
        if len(data)!=0:
            print(data)
            for item in data:
                acc_pass = ','.join(item) # changes tuple output into string to be able to compare
        else:
            print('Username does not exists')# add error messege
        if str(self.menu.inp_pass) == acc_pass:
            print("accepted")
        else:
            print("incorrect password")
        conn.close()
            
            


        
    
 
