import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Root",
    database="testdatabase"
    )

mycursor = db.cursor()

