import os

content = '''

class MessageThread(db.Model):
    __tablename__ = 'message_threads'
    
    id = db.Column(db.Integer, primary_key=True)
    treatment_request_id = db.Column(db.Integer, db.ForeignKey('treatment_requests.id'), nullable=False, index=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    treatment_request = db.relationship('TreatmentRequest', backref=db.backref('message_threads', lazy=True, cascade='all, delete-orphan'))
    hospital = db.relationship('Hospital', backref=db.backref('message_threads', lazy=True, cascade='all, delete-orphan'))
    messages = db.relationship('Message', backref='thread', lazy='dynamic', cascade='all, delete-orphan', order_by='Message.created_at.asc()')
    
    __table_args__ = (
        db.UniqueConstraint('treatment_request_id', 'hospital_id', name='uq_thread_request_hospital'),
    )
    
    def __repr__(self):
        return f"<MessageThread {self.id} Req:{self.treatment_request_id} Hosp:{self.hospital_id}>"


class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('message_threads.id'), nullable=False, index=True)
    
    sender_type = db.Column(db.String(20), nullable=False) # 'patient' or 'hospital'
    sender_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # If patient
    sender_hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=True) # If hospital
    
    message_body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"<Message {self.id} Thread:{self.thread_id} Sender:{self.sender_type}>"
'''

with open('models.py', 'a', encoding='utf-8') as f:
    f.write(content)

print('Appended models!')
