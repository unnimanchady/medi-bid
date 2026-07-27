import sqlite3

def explore_specialties():
    conn = sqlite3.connect('medibid.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM specialties;")
    rows = cursor.fetchall()
    print("All Specialties in DB:")
    for r in rows:
        print(f"ID: {r['id']}, Name: {r['name']}")
        
    conn.close()

if __name__ == '__main__':
    explore_specialties()
