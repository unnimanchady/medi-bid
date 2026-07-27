import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix the auth logic in the 3 hospital message routes
def replacer(match):
    original = match.group(0)
    fixed = original.replace("user_id = session.get('registration_user_id')", "hospital_user_id = session.get('hospital_user_id')")
    fixed = fixed.replace("if not user_id:", "if not hospital_user_id:")
    fixed = fixed.replace("return redirect(url_for('hospital_registration_step1'))", "return redirect(url_for('hospital_login'))")
    
    # We need to query HospitalUser first to get the hospital
    if 'HospitalUser' not in fixed:
        fixed = fixed.replace("from models import MessageThread", "from models import MessageThread, HospitalUser")
        
    fixed = re.sub(r'hospital = Hospital\.query.*?\.first\(\)\n\s+if not hospital:\n\s+return redirect\(url_for\(\'hospital_login\'\)\)', 
                   """hospital_user = HospitalUser.query.get(hospital_user_id)
    if not hospital_user:
        return redirect(url_for('hospital_login'))
    hospital = hospital_user.hospital""", fixed)
    
    return fixed

c = re.sub(r'@app\.route\("/hospital/messages"\).*?return render_template\("hospital-messages\.html", hospital=hospital, sidebar_threads=sidebar_threads\)', replacer, c, flags=re.DOTALL)
c = re.sub(r'@app\.route\("/hospital/messages/<int:thread_id>"\).*?return render_template\("hospital-message-thread\.html", hospital=hospital, thread=thread, messages=messages\)', replacer, c, flags=re.DOTALL)
c = re.sub(r'@app\.route\("/hospital/messages/<int:thread_id>/send", methods=\["POST"\]\).*?return redirect\(url_for\(\'hospital_message_thread\', thread_id=thread_id\)\)', replacer, c, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
