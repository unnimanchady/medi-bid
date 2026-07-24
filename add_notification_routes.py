import os

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
content = content.replace(
    'HospitalAccreditation, HospitalVerificationDocument, TreatmentProposal, CostLineItem, MessageThread, Message',
    'HospitalAccreditation, HospitalVerificationDocument, TreatmentProposal, CostLineItem, MessageThread, Message, Notification'
)

# 2. Add create_notification helper function
helper_code = """
# =========================================================
# NOTIFICATION ENGINE
# =========================================================

def create_notification(recipient_type, recipient_user_id, title, message, notification_type, reference_type=None, reference_id=None, target_url=None):
    from models import db, Notification
    
    # Just a safety check to ensure it's not missing required fields
    if not recipient_type or not recipient_user_id or not title or not message or not notification_type:
        return None
        
    try:
        new_notif = Notification(
            recipient_type=recipient_type,
            recipient_user_id=recipient_user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            reference_type=reference_type,
            reference_id=reference_id,
            target_url=target_url
        )
        db.session.add(new_notif)
        db.session.commit()
        return new_notif
    except Exception as e:
        db.session.rollback()
        print(f"Failed to create notification: {str(e)}")
        return None

"""

if 'def create_notification(' not in content:
    # insert before Patient Portal section
    if '# PATIENT PORTAL' in content:
        content = content.replace('# PATIENT PORTAL', helper_code + '\n# PATIENT PORTAL')

# 3. Add API and Page routes
routes_code = """
# =========================================================
# NOTIFICATION ROUTES
# =========================================================

@app.route("/api/notifications")
def api_get_notifications():
    user_id = session.get("registration_user_id")
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    notifications = Notification.query.filter_by(
        recipient_type='patient', 
        recipient_user_id=user_id
    ).order_by(Notification.created_at.desc()).limit(5).all()
    
    unread_count = Notification.query.filter_by(
        recipient_type='patient', 
        recipient_user_id=user_id,
        is_read=False
    ).count()
    
    data = []
    for n in notifications:
        data.append({
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat(),
            'target_url': n.target_url
        })
        
    return jsonify({
        'notifications': data,
        'unread_count': unread_count
    })

@app.route("/api/notifications/<int:notif_id>/read", methods=['POST'])
def api_mark_notification_read(notif_id):
    user_id = session.get("registration_user_id")
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    notif = Notification.query.filter_by(
        id=notif_id,
        recipient_type='patient',
        recipient_user_id=user_id
    ).first()
    
    if notif:
        notif.is_read = True
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@app.route("/api/notifications/read-all", methods=['POST'])
def api_mark_all_notifications_read():
    user_id = session.get("registration_user_id")
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    Notification.query.filter_by(
        recipient_type='patient',
        recipient_user_id=user_id,
        is_read=False
    ).update({'is_read': True})
    
    db.session.commit()
    return jsonify({'success': True})

@app.route("/patient/notifications")
def patient_notifications():
    user_id = session.get("registration_user_id")
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    # We will fetch from client side or pass to template
    notifications = Notification.query.filter_by(
        recipient_type='patient', 
        recipient_user_id=user_id
    ).order_by(Notification.created_at.desc()).all()
    
    unread_count = sum(1 for n in notifications if not n.is_read)
    
    return render_template("patient-notifications.html", notifications=notifications, unread_count=unread_count)

"""

if 'def api_get_notifications(' not in content:
    content = content.replace(
        'if __name__ == "__main__":',
        routes_code + '\nif __name__ == "__main__":'
    )

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py with imports, helper, and routes")
