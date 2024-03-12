import mysql.connector as m
import sys

a = m.connect(host = "localhost", user = "test", password = "passwprd", database = "cs122a")
if a.is_connected():
    print("success")
b = a.cursor()
b.execute("Create Database if not exists cs122a;")
b.execute("USE cs122a;")
b.execute("DROP TABLE IF EXISTS users, machines, courses;")
b.execute("CREATE TABLE users(UCINetID VARCHAR(20) PRIMARY KEY NOT NULL, FirstName VARCHAR(50), MiddleName VARCHAR(50), LastName VARCHAR(50));")
b.execute("CREATE TABLE machines(MachineID INT PRIMARY KEY NOT NULL, IPAddress VARCHAR(15), OperationalStatus VARCHAR(50), Location VARCHAR(255));")
b.execute("CREATE TABLE courses(CourseID INT PRIMARY KEY NOT NULL, Title VARCHAR(100), Quarter VARCHAR(20));")
b.execute("SELECT 'Number of users', COUNT(*) FROM users UNION "
          "SELECT 'Number of machines', COUNT(*) FROM machines UNION "
          "SELECT 'Number of courses', COUNT(*) FROM courses;")
a.commit()



