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
