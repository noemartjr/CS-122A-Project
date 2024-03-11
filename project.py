import sys
from common import *

# map a string to its function
FUNC_MAP = {
    "import": lambda *args, **kwargs: print(f"Missing import function"),
    "insertStudent": lambda *args, **kwargs: print(f"Missing insertStudent function"),
    "addEmail": lambda *args, **kwargs: print(f"Missing addEmail function"),
    "deleteStudent": lambda *args, **kwargs: print(f"Missing deleteStudent function"),
    "insertMachine": lambda *args, **kwargs: print(f"Missing insertMachine function"),
    "insertUse": lambda *args, **kwargs: print(f"Missing insertUse function"),
    "updateCourse": lambda *args, **kwargs: print(f"Missing updateCourse function"),
    "listCourse": lambda *args, **kwargs: print(f"Missing listCourse function"),
    "popularCourse": lambda *args, **kwargs: print(f"Missing popularCourse function"),
    "adminEmails": lambda *args, **kwargs: print(f"Missing adminEmails function"),
    "activeStudent": lambda *args, **kwargs: print(f"Missing activeStudent function"),
    "machineUsage": lambda *args, **kwargs: print(f"Missing machineUsage function")
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
    func(*sys.argv[2:])

    if db_connection.is_connected():
        cursor.close()
        db_connection.close()

    exit(0)