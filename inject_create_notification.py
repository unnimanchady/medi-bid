import os

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

helper_code = """
# =========================================================
# NOTIFICATION ENGINE HELPER
# =========================================================

def create_notification(recipient_type, recipient_user_id, title, message, notification_type, reference_type=None, reference_id=None, target_url=None):
    from models import db, Notification
    from datetime import datetime, timezone
    
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
            target_url=target_url,
            created_at=datetime.now(timezone.utc)
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
    # Let's insert it right before the notification routes
    target = '# =========================================================\n# NOTIFICATION ROUTES\n# ========================================================='
    if target in content:
        content = content.replace(target, helper_code + '\n' + target)
    else:
        # Fallback to before if __name__
        content = content.replace('if __name__ == "__main__":', helper_code + '\nif __name__ == "__main__":')
        
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected create_notification helper")
else:
    print("Already exists")
