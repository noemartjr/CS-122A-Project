import mysql.connector as m
import sys

a = m.connect(host = "localhost", user = "root", password = "iL0v3BTS!")
if a.is_connected():
    print("success")
b = a.cursor()
b.execute("INSERT INTO users(UCINetID, Email) VALUES (%s, %s);")
a.commit()
