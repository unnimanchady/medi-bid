import os

models_path = 'models.py'
with open(models_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_model = """
class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    recipient_type = db.Column(db.String(50), nullable=False) # 'patient', 'hospital', 'admin'
    recipient_user_id = db.Column(db.Integer, nullable=False, index=True)
    
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(100), nullable=False)
    
    reference_type = db.Column(db.String(100), nullable=True)
    reference_id = db.Column(db.String(100), nullable=True)
    target_url = db.Column(db.String(255), nullable=True)
    
    is_read = db.Column(db.Boolean, default=False, nullable=False, index=True)
    
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    
    def __repr__(self):
        return f"<Notification {self.id} {self.recipient_type}:{self.recipient_user_id} - {self.title}>"
"""

if 'class Notification(' not in content:
    with open(models_path, 'a', encoding='utf-8') as f:
        f.write("\n" + new_model)
    print("Added Notification model to models.py")
else:
    print("Notification model already exists.")
