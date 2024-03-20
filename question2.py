def insert_student(UCINetID, email, first, middle, last):
    try:
        cursor.execute('''INSERT INTO students(UCINetID, email, first, middle, last)
                      VALUES(?, ?, ?, ?, ?)''',(UCINetID, email, first, middle, last))
        db_connection.commit()
        print("Success")
    except mysql.Error as e:
        print("Fail")
