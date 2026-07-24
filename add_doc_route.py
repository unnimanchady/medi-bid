import re

app_py = 'app.py'
with open(app_py, 'r', encoding='utf-8') as f:
    content = f.read()

new_route = """
@app.route("/patient/request/<reference_id>/add-document", methods=["POST"])
@login_required
def patient_request_add_document(reference_id):
    user_id = session.get('user_id')
    req = TreatmentRequest.query.filter_by(reference_id=reference_id).first_or_404()
    
    # Check authorization
    if req.patient_profile.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    if 'document' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['document']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    document_type = request.form.get('document_type', 'Other Medical Document')
    
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        ext = original_filename.rsplit('.', 1)[1].lower()
        storage_filename = f"{uuid.uuid4().hex}.{ext}"
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], storage_filename)
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        new_doc = MedicalDocument(
            original_filename=original_filename,
            storage_filename=storage_filename,
            document_type=document_type,
            mime_type=file.content_type,
            file_size=file_size,
            patient_profile_id=req.patient_profile_id,
            treatment_request_id=req.id,
            uploaded_by_id=user_id
        )
        db.session.add(new_doc)
        db.session.commit()
        
        return jsonify({'success': True})
        
    return jsonify({'error': 'Invalid file type'}), 400
"""

if 'if __name__ == "__main__":' in content:
    content = content.replace('if __name__ == "__main__":', new_route + '\n\nif __name__ == "__main__":')
    with open(app_py, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added patient_request_add_document to app.py")
else:
    print("Could not find anchor to insert route.")
