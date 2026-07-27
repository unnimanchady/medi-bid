import sqlite3

def check_db():
    conn = sqlite3.connect('medibid.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT count(*) as cnt FROM specialties;")
    cnt = cursor.fetchone()['cnt']
    print("Specialties table count:", cnt)
    
    cursor.execute("SELECT count(*) as cnt FROM treatment_requests;")
    cnt = cursor.fetchone()['cnt']
    print("Requests table count:", cnt)
    
    cursor.execute("SELECT * FROM specialties LIMIT 5;")
    rows = cursor.fetchall()
    for r in rows:
        print(dict(r))
        
    conn.close()

if __name__ == '__main__':
    check_db()
