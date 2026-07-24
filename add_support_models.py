import os

models_path = 'models.py'
with open(models_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_models = """

class SupportTicket(db.Model):
    __tablename__ = "support_tickets"

    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    subject = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    attachment_filename = db.Column(db.String(255), nullable=True)
    
    status = db.Column(db.String(20), nullable=False, default="Open")
    
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user = db.relationship('User', backref=db.backref('support_tickets', lazy=True, cascade='all, delete-orphan'))


class SupportTicketMessage(db.Model):
    __tablename__ = "support_ticket_messages"

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('support_tickets.id'), nullable=False, index=True)
    
    sender_type = db.Column(db.String(20), nullable=False)  # 'patient' or 'admin'
    message = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    ticket = db.relationship('SupportTicket', backref=db.backref('messages', lazy=True, cascade='all, delete-orphan', order_by='SupportTicketMessage.created_at.asc()'))

"""

if 'class SupportTicket(' not in content:
    with open(models_path, 'a', encoding='utf-8') as f:
        f.write(new_models)
    print("Appended SupportTicket and SupportTicketMessage to models.py")
else:
    print("Models already exist")
