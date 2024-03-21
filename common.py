import mysql.connector
import os
import csv

class Constants:
    USER = "test"

    PASSWORD = "password"

    DATABASE = "cs122a"

try:
    db_connection = mysql.connector.connect(user=Constants.USER, password=Constants.PASSWORD,
                                            database=Constants.DATABASE)
    cursor = db_connection.cursor()

except mysql.connector.Error as error:
    print(f"Failed to execute SQL script: {error}")
    exit(-1)


# will add functions to be used
schema = {
    'users': '''
        CREATE TABLE IF NOT EXISTS users(
            UCINetID VARCHAR(20) PRIMARY KEY NOT NULL,
            FirstName VARCHAR(50),
            MiddleName VARCHAR(50),
            LastName VARCHAR(50)
        )
    ''',

    'machines':'''
        CREATE TABLE IF NOT EXISTS machines(
            MachineID INT PRIMARY KEY NOT NULL,
            Hostname VARCHAR(255),
            IPAddress VARCHAR(15),
            OperationalStatus VARCHAR(50),
            Location VARCHAR(255)
        )
    ''',
    'courses':'''
        CREATE TABLE IF NOT EXISTS courses(
            CourseID INT PRIMARY KEY NOT NULL,
            Title VARCHAR(100),
            Quarter VARCHAR(20)
        )
    ''',

    'emails':'''
        CREATE TABLE IF NOT EXISTS email (
            UCINetID VARCHAR(20) NOT NULL,
            Email VARCHAR(100),
            PRIMARY KEY (UCINetID, Email),
            FOREIGN KEY (UCINetID) REFERENCES users (UCINetID)
            ON DELETE CASCADE
        )
    ''',

    'students':'''
        CREATE TABLE IF NOT EXISTS students (
           UCINetID VARCHAR(20) PRIMARY KEY NOT NULL,
           FOREIGN KEY (UCINetID) REFERENCES users(UCINetID)
             ON DELETE CASCADE
        )
    ''',

    'admins':'''
        CREATE TABLE IF NOT EXISTS administrators (
           UCINetID VARCHAR(20) PRIMARY KEY NOT NULL,
           FOREIGN KEY (UCINetID) REFERENCES users(UCINetID)
             ON DELETE CASCADE
        )
    ''',

    'projects':'''
        CREATE TABLE IF NOT EXISTS projects (
           ProjectID INT PRIMARY KEY NOT NULL,
           Name VARCHAR(100),
           Description TEXT,
           CourseID INT NOT NULL,
           FOREIGN KEY (CourseID) REFERENCES courses(CourseID)
        )
    ''',

    'use':'''
        CREATE TABLE IF NOT EXISTS use (
           ProjectID INT,
           StudentUCINetID VARCHAR(20),
           MachineID INT,
           StartDate DATE,
           EndDate DATE,
           PRIMARY KEY (ProjectID, StudentUCINetID, MachineID),
           FOREIGN KEY (ProjectID) REFERENCES projects(ProjectID),
           FOREIGN KEY (StudentUCINetID) REFERENCES students(UCINetID),
           FOREIGN KEY (MachineID) REFERENCES machines(MachineID)
        )
    ''',

    'manage':'''
        CREATE TABLE IF NOT EXISTS manage (
           AdminUCINetID VARCHAR(20),
           MachineID INT,
           PRIMARY KEY (AdminUCINetID, MachineID),
           FOREIGN KEY (AdminUCINetID) REFERENCES administrators(UCINetID),
           FOREIGN KEY (MachineID) REFERENCES machines(MachineID)
        )
    ''',
}

def import_data(fpath):
    u = 0;
    m = 0;
    c = 0;
    a = 0;
    e = 0;
    p = 0;
    s = 0;
    use = 0;
    man = 0;

    drop = "DROP TABLE IF EXISTS {}"
    insert = "INSERT INTO {table} ()"

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("SHOW TABLES")

    for t in cursor.fetchall():
        name = t[0]

    cursor.execute(drop.format(name))
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


    TABLES = schema()

    for name in TABLES:
        desc = TABLES[name]
        cursor.execute(desc)


    tnames = [('users', 'User'),
             ('emails', 'email'),
             ('admins', 'Administrator'),
             ('students', 'Student'),
             ('machines', 'Machine'),
             ('courses', 'Course'),
             ('projects', 'Project'),
             ('manage', 'Manage'),
             ('use', 'Uses')]

    for filename, name in tnames:
        path = os.path.join(fpath, filename + '.csv')

        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            first = next(reader)
            col = len(first)

            insert = format(name, col)
            temp = []

            for val in first:
                if(val == 'NULL'):
                    row.append(None)
                else:
                    row.append(val)

                if(name == "User"):
                    u += 1
                elif(name == "Machine"):
                    m += 1
                elif(name == "Course"):
                    c += 1
                elif(name == "Administrator"):
                    a += 1
                elif(name == "email"):
                    e += 1
                elif(name == "Project"):
                    p += 1
                elif(name == "Student"):
                    s += 1
                elif(name == "Uses"):
                    use += 1;
                elif(name == "Manage"):
                    man += 1

                cursor.execute(insert, temp)

                for row in reader:
                    temp = []
                    for val in row:
                        if(val == 'NULL'):
                            temp.append(None)
                        else:
                            temp.append(val)


                    if(name == "User"):
                        u += 1
                    elif(name == "Machine"):
                        m += 1
                    elif(name == "Course"):
                        c += 1
                    elif(name == "Administrator"):
                        a += 1
                    elif(name == "email"):
                        e += 1
                    elif(name == "Project"):
                        p += 1
                    elif(name == "Student"):
                        s += 1
                    elif(name == "Uses"):
                        use += 1;
                    elif(name == "Manage"):
                        man += 1

                    cursor.execute(insert, temp)

        cursor.close()

        print("{}, {}, {}, {}, {}, {}, {}, {}, {}".format(u, m, c, a, e, p, s, use, man))

def insert_student(uci_net_id: str, email: str, First: str, Middle: str, Last: str) -> None:
    try:
        # insert to user table first
        query = "INSERT INTO users VALUES (%s, %s, %s, %s);" % (uci_net_id, First, Middle, Last)
        cursor.execute(query)

        # insert to email table
        query2 = "INSERT INTO userEmail VALUES (%s, %s);" % (uci_net_id, email)
        cursor.execute(query2)

        # insert to userID to student table
        query3 = "INSERT INTO students VALUES (%s);" % (uci_net_id)
        cursor.execute(query3)

        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print(f"Fail")


def add_email(UCINetID, email):
    try:
        query = "INSERT INTO userEmail VALUES (%s, %s);" % (UCINetID, email)
        cursor.execute(query)
        db_connection.commit()
        print("Success")
    except mysql.connector.Error as e:
        print("Fail")

def delete_student(uci_net_id: str) -> None:
    try:
        cursor.execute(f"DELETE FROM users WHERE UCINetID = {uci_net_id};")
        cursor.execute(f"DELETE FROM students WHERE UCINetID = {uci_net_id};")
        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print("Fail")


def insert_machine(*remainder_args) -> None:
    try:
        remainder_str = ",".join(remainder_args)
        cursor.execute(f"INSERT INTO machines VALUES ({remainder_str});")
        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print("Fail")


def insert_use_record(*remainder_args) -> None:
    try:
        remainder_str = ",".join(remainder_args)
        cursor.execute(f"INSERT INTO studentUse VALUES ({remainder_str})")
        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print("Fail")

def update_course(course_id: int, title: str) -> None:
    try:
        query = ("UPDATE courses \
                SET Title = %s \
                WHERE CourseID = %s;"
                 % (title, course_id))
        cursor.execute(query)

        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print(f"Fail")

def course_attended(uci_net_id: str) -> None:
    try:
        cursor.execute(f"SELECT DISTINCT c.CourseID, c.Title, c.Quarter \
                FROM studentUse su \
                JOIN projects p ON su.ProjectID = p.ProjectID \
                JOIN courses c ON p.CourseID = c.CourseID \
                WHERE su.StudentUCINetID = {uci_net_id} \
                ORDER BY c.CourseID ASC;")

        print_table()
    except mysql.connector.Error as error:
        pass

def popular_course(N: int) -> None:
    try:
        cursor.execute(f"SELECT c.CourseID, c.Title, COUNT(*) AS studentCount \
                        FROM courses c \
                       JOIN projects p ON c.CourseID = p.CourseID \
                       JOIN studentUse SU ON p.ProjectID = SU.ProjectID \
                       GROUP BY c.CourseID, c.Title \
                       ORDER BY studentCount DESC, c.CourseID DESC \
                       LIMIT {N};")
        print_table()
    except mysql.connector.Error as error:
        pass

def emails_of_admin( machine_id: int) -> None:
    try:
        cursor.execute(f"SELECT U.UCINetID, U.FirstName, U.MiddleName, U.LastName, UE.Email \
                                FROM administrators A \
                                JOIN users U ON A.UCINetID = U.UCINetID \
                                JOIN userEmail UE ON A.UCINetID = UE.UCINetID \
                                JOIN adminManageMachines AMM ON A.UCINetID = AMM.AdminUCINetID \
                                WHERE AMM.MachineID = {machine_id} \
                                ORDER BY U.UCINetID ASC;")
        print_table()
    except mysql.connector.Error as error:
        pass

def activeStudent(machine_id: int, numTimes: int, startDate: str, endDate: str) -> None:
    try:
        cursor.execute(f"SELECT U.UCINetID, U.FirstName, U.MiddleName, U.LastName FROM users U \
                         JOIN studentUse SU ON U.UCINetID = SU.UCINetID \
                         WHERE SU.MachineID = {machine_id} AND \
                         SU.startDate >= {startDate} AND SU.EndDate <= {endDate} \
                         GROUP BY U.UCINetID, U.FirstName, U.MiddleName, U.LastName \
                         HAVING COUNT(*) >= {numTimes} \
                         ORDER BY U.UCINetID ASC;")
        print_table()
    except mysql.connector.Error as error:
        pass
    
def machineUsage(courseId: int) -> None:
    try:
        cursor.execute(f"SELECT M.MachineID, M.Hostname, M.IPAddress, \
                         SUM(CASE WHEN SU.ProjectID IS NOT NULL THEN 1 ELSE 0 END) AS Count \
                         FROM machines M \
                         LEFT JOIN (SELECT * FROM studentUse WHERE ProjectID IN( \
                                    SELECT ProjectID from Project WHERE CourseID = {courseId})) \
                         AS SU ON SU.MachineID = M.MachineID \
                         GROUP BY M.MachineID, M.Hostname, M.IPAddress \
                         ORDER BY M.MachineID DESC;")
        print_table()
    except mysql.connector.Error as error:
        pass

def print_table():
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(",".join(str(cell) for cell in row))

