import sys
from common import *

# map a string to its function
FUNC_MAP = {
    "import": import_data,
    "insertStudent": insert_student,
    "addEmail": add_email,
    "deleteStudent": delete_student,
    "insertMachine": insert_machine,
    "insertUse": insert_use_record,
    "updateCourse": update_course,
    "listCourse": course_attended,
    "popularCourse": popular_course,
    "adminEmails": emails_of_admin,
    "activeStudent": activeStudent,
    "machineUsage": machineUsage
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing function name")
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()
        exit(-1)

    func_name = sys.argv[1]

    if func_name not in FUNC_MAP.keys():
        print("Invalid function name provided")
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()
        exit(-1)

    func = FUNC_MAP[func_name]
    func(*[get_formatted_param(param) for param in sys.argv[2:]])

    if db_connection.is_connected():
        cursor.close()
        db_connection.close()

    exit(0)