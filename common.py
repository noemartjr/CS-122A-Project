import mysql.connector


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
def print_table(table_input: list) -> None:
    print("\n".join([",".join([str(row_item) for row_item in row]) for row in table_input]))

def import_data(fpath, db_connection):
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


    TABLES = init_tables()

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

def delete_student(uci_net_id: str) -> None:
    try:
        cursor.execute(f"DELETE FROM Users WHERE UCINetID = \'{uci_net_id}\';")
        cursor.execute(f"DELETE FROM Students WHERE UCINetID = \'{uci_net_id}\';")
        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print("Fail")


def insert_machine(machine_id: int, *remainder_args) -> None:
    try:
        remainder_str = ",".join([f"\'{arg}\'" if arg != "NULL" else "NULL" for arg in remainder_args])
        cursor.execute(f"INSERT INTO Machines VALUES ({machine_id},{remainder_str});")
        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print("Fail")


def insert_use_record(proj_id: int, uci_net_id: str, machine_id: int, *remainder_args) -> None:
    try:
        remainder_str = ",".join([f"\'{arg}\'" if arg != "NULL" else "NULL" for arg in remainder_args])
        cursor.execute(f"INSERT INTO StudentUseMachinesInProject VALUES ({proj_id},\'{uci_net_id}\',{machine_id},{remainder_str})")
        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print("Fail")



def emails_of_admin( machine_id: int) -> None:
    try:
        cursor.execute(f"SELECT U.UCINetID, U.FirstName, U.MiddleName, U.LastName, UE.Email \
                        FROM Administrators A \
                        JOIN Users U ON A.UCINetID = U.UCINetID \
                        JOIN UserEmail UE ON A.UCINetID = UE.UCINetID \
                        JOIN AdministratorManageMachines AMM ON A.UCINetID = AMM.AdministratorUCINetID \
                        WHERE AMM.MachineID = \'{machine_id}\' \
                        ORDER BY U.UCINetID ASC;")
        db_connection.commit()
        print("Success")
    except mysql.connector.Error as error:
        print("Fail")
