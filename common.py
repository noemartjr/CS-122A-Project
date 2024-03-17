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


def delete_student(uci_net_id: str) -> None:
    try:
        cursor.execute(f"SELECT UCINetID FROM Students WHERE UCINetID = \'{uci_net_id}\';")
        if len(cursor.fetchall()) == 0:
            print("Fail")
            return
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
