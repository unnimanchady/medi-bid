import sqlite3

def run_diagnostics():
    conn = sqlite3.connect('medibid.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1 & 2. Find Mayo Clinic
    print("--- 1 & 2. MAYO CLINIC INFO ---")
    cursor.execute("SELECT id, legal_name, display_name, verification_status FROM hospitals WHERE display_name LIKE '%Mayo%' OR legal_name LIKE '%Mayo%'")
    mayo = cursor.fetchone()
    if not mayo:
        print("Mayo Clinic not found!")
        return
    
    hospital_id = mayo['id']
    print(f"ID: {hospital_id}")
    print(f"Name (Display): {mayo['display_name']}")
    print(f"Name (Legal): {mayo['legal_name']}")
    print(f"Verification Status: {mayo['verification_status']}")

    # Get Specialties
    cursor.execute("""
        SELECT s.id, s.name 
        FROM specialties s 
        JOIN hospital_specialty hs ON s.id = hs.specialty_id 
        WHERE hs.hospital_id = ?
    """, (hospital_id,))
    specialties = cursor.fetchall()
    print("Registered Specialties:")
    for spec in specialties:
        print(f"  - [{spec['id']}] {spec['name']}")

    # 3. All Treatment Requests
    print("\n--- 3. ALL TREATMENT REQUESTS ---")
    cursor.execute("SELECT id, reference_id, specialty, condition, status, created_at FROM treatment_requests")
    requests = cursor.fetchall()
    for req in requests:
        print(f"DB ID: {req['id']}, Ref: {req['reference_id']}, Specialty: {req['specialty']}, Condition: {req['condition']}, Status: {req['status']}, Created: {req['created_at']}")

    # 4. Check TR-60B44F95ED
    print("\n--- 4. CHECK TR-60B44F95ED ---")
    cursor.execute("SELECT id, reference_id, specialty, status, patient_profile_id FROM treatment_requests WHERE reference_id = 'TR-60B44F95ED'")
    tr = cursor.fetchone()
    if tr:
        print(f"Found TR-60B44F95ED:")
        print(f"  DB ID: {tr['id']}")
        print(f"  Specialty: {tr['specialty']}")
        print(f"  Status: {tr['status']}")
        print(f"  Patient Profile ID: {tr['patient_profile_id']}")
        
        # Does Mayo match this specialty?
        mayo_matches = any(s['name'] == tr['specialty'] for s in specialties)
        print(f"  Mayo matches specialty: {mayo_matches}")
        
        # Did Mayo submit a proposal?
        cursor.execute("SELECT id, status FROM treatment_proposals WHERE hospital_id = ? AND treatment_request_id = ?", (hospital_id, tr['id']))
        prop = cursor.fetchone()
        if prop:
            print(f"  Mayo submitted proposal: Yes (ID: {prop['id']}, Status: {prop['status']})")
        else:
            print(f"  Mayo submitted proposal: No")
    else:
        print("TR-60B44F95ED NOT FOUND")

    # 5. TreatmentProposals for Mayo Clinic
    print("\n--- 5. MAYO CLINIC PROPOSALS ---")
    cursor.execute("""
        SELECT p.id as prop_id, p.status as prop_status, p.submitted_at, 
               r.id as req_id, r.reference_id 
        FROM treatment_proposals p
        JOIN treatment_requests r ON p.treatment_request_id = r.id
        WHERE p.hospital_id = ?
    """, (hospital_id,))
    proposals = cursor.fetchall()
    if proposals:
        for p in proposals:
            print(f"Proposal ID: {p['prop_id']}, Req ID: {p['req_id']} ({p['reference_id']}), Status: {p['prop_status']}, Submitted: {p['submitted_at']}")
    else:
        print("No proposals found for Mayo Clinic.")
        
    conn.close()

if __name__ == '__main__':
    run_diagnostics()
