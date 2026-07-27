import sqlite3

def check_backup_tables():
    conn = sqlite3.connect('medibid_before_schema_fix.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in backup db:")
    for t in tables:
        print(t[0])
    conn.close()

if __name__ == '__main__':
    check_backup_tables()
