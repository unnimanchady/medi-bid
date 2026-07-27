import sqlite3

def check_all():
    conn = sqlite3.connect('medibid.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for t in tables:
        table_name = t['name']
        try:
            cursor.execute(f"SELECT count(*) as cnt FROM {table_name}")
            cnt = cursor.fetchone()['cnt']
            print(f"Table {table_name}: {cnt} rows")
        except Exception as e:
            print(f"Table {table_name}: Error {e}")
            
    conn.close()

if __name__ == '__main__':
    check_all()
