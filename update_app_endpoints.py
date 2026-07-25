import re

new_routes = """
@app.route("/patient/treatment-proposal/<int:proposal_id>/shortlist", methods=['POST'])
def patient_proposal_shortlist(proposal_id):
    user_id = session.get("registration_user_id")
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    proposal = TreatmentProposal.query.get_or_404(proposal_id)
    if proposal.treatment_request.patient_profile.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.get_json()
    proposal.patient_shortlisted = data.get('shortlisted', False)
    db.session.commit()
    
    return jsonify({'success': True, 'shortlisted': proposal.patient_shortlisted})

@app.route("/patient/treatment-proposal/<int:proposal_id>/notes", methods=['POST'])
def patient_proposal_notes(proposal_id):
    user_id = session.get("registration_user_id")
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    proposal = TreatmentProposal.query.get_or_404(proposal_id)
    if proposal.treatment_request.patient_profile.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.get_json()
    proposal.patient_notes = data.get('notes', '')
    db.session.commit()
    
    return jsonify({'success': True})
"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('if __name__ == "__main__":', new_routes + '\n\nif __name__ == "__main__":')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
