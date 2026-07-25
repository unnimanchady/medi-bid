import sqlite3

conn = sqlite3.connect('medibid.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("SELECT * FROM hospitals WHERE display_name IN ('Mayo Clinic', 'Cleveland Clinic') OR legal_name IN ('Mayo Clinic', 'Cleveland Clinic')")
hospitals = c.fetchall()

print("Hospitals:")
for h in hospitals:
    print(dict(h))

c.execute("SELECT * FROM treatment_proposals WHERE hospital_id IN (SELECT id FROM hospitals WHERE display_name IN ('Mayo Clinic', 'Cleveland Clinic') OR legal_name IN ('Mayo Clinic', 'Cleveland Clinic'))")
proposals = c.fetchall()

print("\nProposals:")
for p in proposals:
    print(dict(p))
