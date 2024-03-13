import mysql.connector as m
import sys

a = m.connect(host = "localhost", user = "root", password = "iL0v3BTS!")
if a.is_connected():
    print("success")
b = a.cursor()
b.execute("DROP TABLE IF EXISTS students;")
b.execute("CREATE TABLE students(UCINetID STR(20) PRIMARY KEY NOT NULL, Email STR(1024), FirstName STR(50), MiddleName VARCHAR(50), LastName VARCHAR(50), FOREIGN KEY (UCINetID) REFERENCES Users(UCINetID) ON DELETE CASCADE, FOREIGN KEY (Email) REFERENCES Emails(Email) ON DELETE CASCADE);")
b.execute("INSERT INTO students(UCINetID, Email, FirstName, MiddleName, LastName) VALUES (%s, %s);")
a.commit()
