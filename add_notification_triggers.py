import os

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update hospital_proposal_submit
# Find: proposal.submitted_at = datetime.now(timezone.utc)
#       db.session.commit()
if 'create_notification(' not in content.split('def hospital_proposal_submit(')[1].split('def hospital_proposal_view(')[0]:
    target1 = '    proposal.submitted_at = datetime.now(timezone.utc)\n    db.session.commit()'
    replacement1 = target1 + """
    
    # Notify patient
    create_notification(
        recipient_type='patient',
        recipient_user_id=req.patient_profile.user_id,
        title='New Hospital Proposal',
        message=f"{hospital.display_name or hospital.name} submitted a treatment proposal.",
        notification_type='proposal_submitted',
        reference_type='treatment_request',
        reference_id=req.reference_id,
        target_url=url_for('patient_hospital_responses', reference_id=req.reference_id)
    )
"""
    content = content.replace(target1, replacement1)


# 2. Update hospital_proposal_edit
# Let's find db.session.commit() inside hospital_proposal_edit and insert the notification right after it
# To be safe, I'll search for flash("Proposal updated successfully.", "success")
if 'def hospital_proposal_edit(' in content:
    if 'create_notification(' not in content.split('def hospital_proposal_edit(')[1].split('def hospital_proposal_review(')[0]:
        target2 = 'flash("Proposal updated successfully.", "success")'
        replacement2 = """# Notify patient
    create_notification(
        recipient_type='patient',
        recipient_user_id=req.patient_profile.user_id,
        title='Proposal Updated',
        message=f"{hospital.display_name or hospital.name} updated their proposal.",
        notification_type='proposal_updated',
        reference_type='treatment_request',
        reference_id=req.reference_id,
        target_url=url_for('patient_hospital_responses', reference_id=req.reference_id)
    )
    
    flash("Proposal updated successfully.", "success")"""
        content = content.replace(target2, replacement2)


# 3. Update hospital_send_message
if 'def hospital_send_message(' in content:
    if 'create_notification(' not in content.split('def hospital_send_message(')[1].split('def hospital_dashboard(')[0]:
        target3 = '    db.session.add(new_msg)\n    db.session.commit()'
        replacement3 = target3 + """
    
    # Notify patient
    hospital = Hospital.query.get(hospital_user.hospital_id)
    create_notification(
        recipient_type='patient',
        recipient_user_id=thread.patient_profile.user_id,
        title='New Secure Message',
        message=f"New message from {hospital.display_name or hospital.name}.",
        notification_type='new_message',
        reference_type='message_thread',
        reference_id=str(thread.id),
        target_url=url_for('patient_message_thread', thread_id=thread.id)
    )
"""
        content = content.replace(target3, replacement3)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py with notification triggers")
