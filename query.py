import sqlite3
conn = sqlite3.connect('medibid.db')
c = conn.cursor()
req = c.execute("SELECT patient_profile_id, height_cm, weight_kg, pregnancy_status FROM treatment_requests LEFT JOIN patient_profiles ON treatment_requests.patient_profile_id = patient_profiles.id WHERE reference_id='TR-0CF7CF11FA'").fetchone()
print('Request TR-0CF7CF11FA:', req)

req2 = c.execute("SELECT patient_profile_id FROM treatment_requests WHERE reference_id='TR-0CF7CF11FA'").fetchone()
if req2:
    prof = c.execute("SELECT id, first_name, last_name, date_of_birth, gender, nationality, country_of_residence, city, passport_number, pregnancy_status FROM patient_profiles WHERE id=?", (req2[0],)).fetchone()
    print('Profile:', prof)
else:
    print('No request found')
