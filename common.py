import mysql.connector
import os
import csv

class Constants:
    USER = "root"

    PASSWORD = "Y9shk*qG"

    DATABASE = "cs122a"

try:
    db_connection = mysql.connector.connect(user=Constants.USER, password=Constants.PASSWORD,
                                            database=Constants.DATABASE)
    cursor = db_connection.cursor()

except mysql.connector.Error as error:
    print(f"Failed to execute SQL script: {error}")
    exit(-1)


# will add functions to be used

def import_data(fpath):
    u = 0;
    m = 0;
    c = 0;

    drop = "DROP TABLE IF EXISTS {}"
    insert = "INSERT INTO {table} ()"

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("SHOW TABLES")

    for t in cursor.fetchall():
        name = t[0]

    cursor.execute(drop.format(name))
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


    TABLES = print_table()

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

                    cursor.execute(insert, temp)

        cursor.close()

        print("{}, {}, {}".format(u, m, c))

def insert_student(uci_net_id: str, email: str, First: str, Middle: str, Last: str) -> None:
    try:
        # insert to user table first
        query = "INSERT INTO users VALUES ('%s', '%s', '%s', '%s');" % (uci_net_id, First, Middle, Last)
        cursor.execute(query)

        # insert to email table
        query2 = "INSERT INTO userEmail VALUES ('%s', '%s');" % (uci_net_id, email)
        cursor.execute(query2)

        # insert to userID to student table
        query3 = "INSERT INTO students VALUES ('%s');" % (uci_net_id)
        cursor.execute(query3)

        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print(f"Failed to execute SQL script insert_student: {error}")


def add_email(UCINetID, email):
    try:
        cursor.execute("SELECT UCINetID FROM students WHERE UCINetID=?", (UCINetID,))
        user = cursor.fetchone()

        if user:
            cursor.execute("UPDATE students SET Email=? WHERE UCINetID=?", (email, UCINetID))
            db_connection.commit()
            db_connection.close()
            print("Success")
        else:
            print("User with UCINetID '{}' not found.".format(UCINetID))
            db_connection.close()
            print("User not found")
    except mysql.connector.Error as e:
        print("mysql error:", e)
        print("Fail")

def delete_student(uci_net_id: str) -> None:
    try:
        cursor.execute(f"DELETE FROM users WHERE UCINetID = \'{uci_net_id}\';")
        cursor.execute(f"DELETE FROM students WHERE UCINetID = \'{uci_net_id}\';")
        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print("Fail")


def insert_machine(machine_id: int, *remainder_args) -> None:
    try:
        remainder_str = ",".join([f"\'{arg}\'" if arg != "NULL" else "NULL" for arg in remainder_args])
        cursor.execute(f"INSERT INTO machines VALUES ({machine_id},{remainder_str});")
        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print("Fail")


def insert_use_record(proj_id: int, uci_net_id: str, machine_id: int, *remainder_args) -> None:
    try:
        remainder_str = ",".join([f"\'{arg}\'" if arg != "NULL" else "NULL" for arg in remainder_args])
        cursor.execute(f"INSERT INTO studentUse VALUES ({proj_id},\'{uci_net_id}\',{machine_id},{remainder_str})")
        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print("Fail")

def update_course(course_id: int, title: str) -> None:
    try:
        query = ("UPDATE courses \
                SET Title = '%s' \
                WHERE CourseID = %s;"
                 % (title, course_id))
        cursor.execute(query)

        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print(f"Fail")
def course_attended(uci_net_id: str) -> None:
    cursor.execute(f"SELECT DISTINCT c.CourseID, c.Title, c.Quarter \
            FROM studentUse su \
            JOIN projects p ON su.ProjectID = p.ProjectID \
            JOIN courses c ON p.CourseID = c.CourseID \
            WHERE su.StudentUCINetID = '{uci_net_id}' \
            ORDER BY c.CourseID ASC;")

    print_table(cursor)

def popular_course(N: int) -> None:
    cursor.execute(f"SELECT c.CourseID, c.Title, COUNT(*) AS studentCount \
                    FROM courses c \
                   JOIN projects p ON c.CourseID = p.CourseID \
                   JOIN studentUse SU ON p.ProjectID = SU.ProjectID \
                   GROUP BY c.CourseID, c.Title \
                   ORDER BY studentCount DESC, c.CourseID DESC \
                   LIMIT {N};")
    print_table(cursor)

def emails_of_admin( machine_id: int) -> None:
    cursor.execute(f"SELECT U.UCINetID, U.FirstName, U.MiddleName, U.LastName, UE.Email \
                            FROM administrators A \
                            JOIN users U ON A.UCINetID = U.UCINetID \
                            JOIN userEmail UE ON A.UCINetID = UE.UCINetID \
                            JOIN adminManageMachines AMM ON A.UCINetID = AMM.AdminUCINetID \
                            WHERE AMM.MachineID = \'{machine_id}\' \
                            ORDER BY U.UCINetID ASC;")
    print_table(cursor)

def activeStudent(machine_id: int, numTimes: int, startDate: str, endDate: str) -> None:
    cursor.execute(f"SELECT * FROM users U \
                     JOIN studentUse SU ON U.UCINetID = SU.UCINetID \
                     WHERE SU.MachineID = {machine_id} AND \
                     SU.startDate >= '{startDate}' AND SU.EndDate <= '{endDate}' \
                     GROUP BY U.UCINetID, U.FirstName, U.MiddleName, U.LastName \
                     HAVING COUNT(*) >= {numTimes} \
                     ORDER BY U.UCINetID ASC;")
    print_table(cursor)
    
def machineUsage(courseId: int) -> None:
    cursor.execute(f"SELECT M.MachineID, M.Hostname, M.IPAddress, M.OperationalStatus, \
                     SUM(CASE WHEN SU.ProjectID IS NOT NULL THEN 1 ELSE 0 END) AS Count \
                     FROM machines M \
                     LEFT JOIN (SELECT * FROM studentUse WHERE ProjectID IN( \
                                SELECT ProjectID from Project WHERE CourseID = {courseId})) \
                     AS SU ON SU.MachineID = M.MachineID \
                     GROUP BY M.MachineID, M.Hostname, M.IPAddress \
                     ORDER BY M.MachineID DESC;")
    print_table(cursor)

def print_table(cursor):
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(",".join(str(cell) for cell in row))
    else:
        print("No results found")

