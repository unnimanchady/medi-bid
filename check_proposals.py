import sqlite3

conn = sqlite3.connect('medibid.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("SELECT * FROM treatment_requests WHERE reference_id='TR-R5PDRXK8WW'")
tr = c.fetchone()
print(f"TR ID: {tr['id'] if tr else 'None'}")

if tr:
    c.execute('''SELECT p.id as p_id, p.hospital_id as p_h_id, h.id as h_id, h.display_name, h.legal_name 
                 FROM treatment_proposals p 
                 JOIN hospitals h ON p.hospital_id = h.id 
                 WHERE p.treatment_request_id = ?''', (tr['id'],))
    proposals = c.fetchall()
    print("\nProposals:")
    for row in proposals:
        print(dict(row))
