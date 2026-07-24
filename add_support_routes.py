import os

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_routes = """
# =========================================================
# SUPPORT MODULE
# =========================================================

@app.route("/patient/support")
def patient_support():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    user = User.query.get(user_id)
    tickets = SupportTicket.query.filter_by(user_id=user_id).order_by(SupportTicket.updated_at.desc()).all()
    
    return render_template("patient-support.html", user=user, tickets=tickets)


@app.route("/patient/support/submit", methods=["POST"])
def patient_support_submit():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    subject = request.form.get("subject", "").strip()
    category = request.form.get("category", "").strip()
    message = request.form.get("message", "").strip()
    
    if not subject or not category or not message:
        flash("All fields are required.", "error")
        return redirect(url_for('patient_support') + '#contact')
        
    import random
    import string
    
    # Generate unique ticket number
    while True:
        ticket_number = 'TKT-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not SupportTicket.query.filter_by(ticket_number=ticket_number).first():
            break
            
    attachment = request.files.get("attachment")
    attachment_filename = None
    if attachment and attachment.filename:
        # In a real app we'd save it properly. For V1 MVP, just store the filename
        attachment_filename = attachment.filename
        
    new_ticket = SupportTicket(
        ticket_number=ticket_number,
        user_id=user_id,
        subject=subject,
        category=category,
        message=message,
        attachment_filename=attachment_filename,
        status="Open"
    )
    db.session.add(new_ticket)
    db.session.commit()
    
    flash(f"Support ticket {ticket_number} created successfully.", "success")
    return redirect(url_for('patient_support') + '#tickets')


@app.route("/patient/support/ticket/<string:ticket_number>", methods=["GET", "POST"])
def patient_support_ticket_detail(ticket_number):
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    ticket = SupportTicket.query.filter_by(ticket_number=ticket_number).first_or_404()
    
    # IDOR Prevention
    if ticket.user_id != user_id:
        from flask import abort
        abort(403)
        
    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if not message:
            flash("Message cannot be empty.", "error")
            return redirect(url_for('patient_support_ticket_detail', ticket_number=ticket.ticket_number))
            
        new_msg = SupportTicketMessage(
            ticket_id=ticket.id,
            sender_type="patient",
            message=message
        )
        ticket.updated_at = datetime.now(timezone.utc)
        db.session.add(new_msg)
        db.session.commit()
        
        return redirect(url_for('patient_support_ticket_detail', ticket_number=ticket.ticket_number))
        
    return render_template("patient-support-ticket.html", ticket=ticket)

"""

if 'def patient_support():' not in content:
    content = content.replace('if __name__ == "__main__":', new_routes + '\nif __name__ == "__main__":')
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added Support routes to app.py")
else:
    print("Routes already exist")
