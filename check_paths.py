import os
import sys

def check_environment():
    print("--- Diagnostic Report ---")
    
    # 1. Current working directory
    cwd = os.getcwd()
    print(f"Current Working Directory: {cwd}")
    
    # 2. Location of this script
    script_loc = os.path.abspath(os.path.dirname(__file__))
    print(f"Script Location: {script_loc}")
    
    # 3. Expected instance path
    expected_instance = os.path.join(script_loc, 'instance')
    print(f"Expected Instance Directory: {expected_instance}")
    
    # 4. Check if exists
    if os.path.exists(expected_instance):
        print(" -> Directory EXISTS")
        # 5. Check writability
        if os.access(expected_instance, os.W_OK):
            print(" -> Directory is WRITABLE (OK)")
        else:
            print(" -> Directory is NOT WRITABLE (FAIL)")
    else:
        print(" -> Directory does NOT exist (FAIL)")
        try:
            os.makedirs(expected_instance)
            print(" -> Attempted to create directory... Created!")
        except Exception as e:
            print(f" -> Failed to create directory: {e}")

    # 6. Check Database File
    db_path = os.path.join(expected_instance, 'db.sqlite')
    print(f"Database File Path: {db_path}")
    if os.path.exists(db_path):
        print(" -> File EXISTS")
        if os.access(db_path, os.R_OK | os.W_OK):
             print(" -> File is Readable/Writable (OK)")
        else:
             print(" -> File permission issues (FAIL)")
    else:
        print(" -> File does NOT exist (Flask should create it)")

if __name__ == "__main__":
    check_environment()
