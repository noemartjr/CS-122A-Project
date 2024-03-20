import mysql.connector as m
import sys

a = m.connect(host = "localhost", user = "root", password = "iL0v3BTS!", database = "cs122a_project")
if a.is_connected():
    print("success")

def import_data(fpath, a):
    db = a.cursor()
    u = 0;
    m = 0;
    c = 0;

    drop = "DROP TABLE IF EXISTS {}"
    insert = "INSERT INTO {table} ()"

    db.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.execute("SHOW TABLES")

    for t in db.fetchall():
        name = t[0]

    db.execute(drop.format(name))
    db.execute("SET FOREIGN_KEY_CHECKS = 1")


    TABLES = init_tables()

    for name in TABLES:
        desc = TABLES[name]
        db.execute(desc)


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

                db.execute(insert, temp)

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

                    db.execute(insert, temp)

        db.close()

        print("{}, {}, {}".format(u, m, c))
             



