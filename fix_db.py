import sqlite3
import os

db_path = 'medibid.db'
if not os.path.exists(db_path):
    print("Database not found!")
    exit(1)

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Verify TR-0CF7CF11FA references ID 21
c.execute("SELECT patient_profile_id FROM treatment_requests WHERE reference_id = 'TR-0CF7CF11FA'")
req = c.fetchone()
if not req or req[0] != 21:
    print(f"TR-0CF7CF11FA does not reference ID 21. It references: {req[0] if req else 'None'}")
else:
    print("Confirmed TR-0CF7CF11FA references ID 21.")
    
    # Reassign to ID 19
    c.execute("UPDATE treatment_requests SET patient_profile_id = 19 WHERE reference_id = 'TR-0CF7CF11FA'")
    print("Reassigned TR-0CF7CF11FA to patient_profile_id 19.")
    
    # Check if any other records reference ID 21
    c.execute("SELECT reference_id FROM treatment_requests WHERE patient_profile_id = 21")
    other_reqs = c.fetchall()
    if other_reqs:
        print(f"WARNING: Other requests reference ID 21: {other_reqs}")
    else:
        # Delete ID 21
        c.execute("DELETE FROM patient_profiles WHERE id = 21")
        print("Deleted duplicate PatientProfile ID 21.")
        
conn.commit()
conn.close()
