import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Instead of relying on top level imports, let's just make sure each route imports HospitalUser
def fix_unbound(match):
    original = match.group(0)
    fixed = original.replace("hospital_user = HospitalUser.query.get(hospital_user_id)", "from models import HospitalUser\n    hospital_user = HospitalUser.query.get(hospital_user_id)")
    return fixed

c = re.sub(r'def hospital_messages\(\):.*?return render_template', fix_unbound, c, flags=re.DOTALL)
c = re.sub(r'def hospital_message_thread\(thread_id\):.*?return render_template', fix_unbound, c, flags=re.DOTALL)
c = re.sub(r'def hospital_send_message\(thread_id\):.*?return redirect', fix_unbound, c, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
