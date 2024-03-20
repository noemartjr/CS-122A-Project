import mysql.connector 

db_connection = mysql.connector.connect(user=Constants.USER, password=Constants.PASSWORD, database=Constants.DATABASE)
cursor = db_connection.cursor()

def import_data(fpath, db_connection):
    cursor = db_connection.cursor()
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
             






