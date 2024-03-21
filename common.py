import mysql.connector
import os
import csv
from collections import OrderedDict


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

sql_file_path = 'cs122a_project.sql'


def get_formatted_param(param: str) -> str:
    if param == "NULL":
        return "NULL"
    elif param.isdigit():
        return param
    else:
        return f"'{param}'"


def import_data(fpath: str) -> None:
    try:
        fpath = fpath.strip("\'")
        u = 0
        m = 0
        c = 0

        sql_script = open(sql_file_path, 'r').read()
        # Execute each statement in the SQL file
        for statement in sql_script.split(';'):
            # Ignore empty statements (which can occur due to splitting by ';')
            if statement.strip():
                cursor.execute(statement)

        db_connection.commit()

        # (file name, table name)
        tnames = [('users', 'users'),
                  ('emails', 'userEmail'),
                  ('admins', 'administrators'),
                  ('students', 'students'),
                  ('machines', 'machines'),
                  ('courses', 'courses'),
                  ('projects', 'projects'),
                  ('manage', 'adminManageMachines'),
                  ('use', 'studentUse')]

        for filename, name in tnames:
            path = os.path.join(fpath, filename + '.csv')

            with open(path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                values_list = []
                for row in reader:
                    if (name == "users"):
                        u += 1
                    elif (name == "machines"):
                        m += 1
                    elif (name == "courses"):
                        c += 1

                    values_list.append("(" + ",".join([get_formatted_param(item) for item in row]) + ")")

                cursor.execute(f"INSERT INTO {name} VALUES {','.join(values_list)};")

        db_connection.commit()
        print(f"{u},{m},{c}")
    except mysql.connector.Error as error:
        pass


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
        cursor.execute(f"SELECT c.CourseID, c.Title, COUNT(DISTINCT SU.StudentUCINetID) AS studentCount \
                        FROM courses c \
                       JOIN projects p ON c.CourseID = p.CourseID \
                       JOIN studentUse SU ON p.ProjectID = SU.ProjectID \
                       GROUP BY c.CourseID, c.Title \
                       ORDER BY studentCount DESC, c.CourseID DESC \
                       LIMIT {N};")
        print_table()
    except mysql.connector.Error as error:
        pass


def emails_of_admin(machine_id: int) -> None:
    try:
        cursor.execute(f"SELECT U.UCINetID, U.FirstName, U.MiddleName, U.LastName, UE.Email \
                                FROM administrators A \
                                JOIN users U ON A.UCINetID = U.UCINetID \
                                JOIN userEmail UE ON A.UCINetID = UE.UCINetID \
                                JOIN adminManageMachines AMM ON A.UCINetID = AMM.AdminUCINetID \
                                WHERE AMM.MachineID = {machine_id} \
                                ORDER BY U.UCINetID ASC;")

        email_dict = OrderedDict()
        for row in cursor.fetchall():
            row_strs = [str(item) if item is not None else "NULL" for item in row]
            row_key = ",".join(row_strs[:-1])
            if row_key not in email_dict:
                email_dict[row_key] = []
            email_dict[row_key].append(row_strs[-1])
        print("\n".join([f"{dict_key},{';'.join(email_values)}" for dict_key, email_values in email_dict.items()]))

    except mysql.connector.Error as error:
        pass


def activeStudent(machine_id: int, numTimes: int, startDate: str, endDate: str) -> None:
    try:
        cursor.execute(f"SELECT U.UCINetID, U.FirstName, U.MiddleName, U.LastName FROM users U \
                         JOIN studentUse SU ON U.UCINetID = SU.StudentUCINetID \
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
                                    SELECT ProjectID from projects WHERE CourseID = {courseId})) \
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
            print(",".join(str(cell) if cell is not None else "NULL" for cell in row))
