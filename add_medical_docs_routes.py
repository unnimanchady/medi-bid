import os

app_py_path = 'app.py'

with open(app_py_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_routes = """
# =========================================================
# PATIENT MEDICAL DOCUMENTS
# =========================================================

@app.route("/patient/medical-documents")
def patient_medical_documents():
    user_id = session.get('registration_user_id')
    if not user_id:
        return redirect(url_for('patient_registration_step1'))
        
    profiles = PatientProfile.query.filter_by(user_id=user_id).all()
    profile_ids = [p.id for p in profiles]
    
    docs = MedicalDocument.query.filter(MedicalDocument.patient_profile_id.in_(profile_ids)).order_by(MedicalDocument.uploaded_at.desc()).all()
    
    return render_template("patient-medical-documents.html", docs=docs, profiles=profiles)

@app.route("/patient/document/upload", methods=["POST"])
def patient_medical_documents_upload():
    user_id = session.get('registration_user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    if 'document' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['document']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    document_type = request.form.get('document_type', 'Other')
    title = request.form.get('title')
    description = request.form.get('description')
    profile_id = request.form.get('patient_profile_id')
    treatment_request_id = request.form.get('treatment_request_id')
    
    if not profile_id:
        return jsonify({'error': 'Patient Profile is required'}), 400
        
    # Verify profile belongs to user
    profile = PatientProfile.query.filter_by(id=profile_id, user_id=user_id).first()
    if not profile:
        return jsonify({'error': 'Invalid Patient Profile'}), 400
        
    # Verify treatment request if provided
    if treatment_request_id:
        req = TreatmentRequest.query.filter_by(id=treatment_request_id, patient_profile_id=profile_id).first()
        if not req:
            return jsonify({'error': 'Invalid Treatment Request for this profile'}), 400
    
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        ext = original_filename.rsplit('.', 1)[1].lower()
        storage_filename = f"{uuid.uuid4().hex}.{ext}"
        
        file_path = os.path.join(UPLOAD_FOLDER, storage_filename)
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        new_doc = MedicalDocument(
            original_filename=original_filename,
            storage_filename=storage_filename,
            document_type=document_type,
            title=title,
            description=description,
            mime_type=file.content_type,
            file_size=file_size,
            patient_profile_id=profile_id,
            treatment_request_id=treatment_request_id if treatment_request_id else None,
            uploaded_by_id=user_id
        )
        db.session.add(new_doc)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Document uploaded successfully!'})
        
    return jsonify({'error': 'Invalid file type'}), 400

@app.route("/patient/document/<int:doc_id>/delete", methods=["POST"])
def patient_medical_document_delete(doc_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    doc = MedicalDocument.query.get_or_404(doc_id)
    
    if doc.uploaded_by_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    try:
        file_path = os.path.join(UPLOAD_FOLDER, doc.storage_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
        db.session.delete(doc)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/patient/document/<int:doc_id>/view")
def view_document(doc_id):
    user_id = session.get('registration_user_id')
    if not user_id:
        from flask import abort
        abort(401)
        
    doc = MedicalDocument.query.get_or_404(doc_id)
    if doc.uploaded_by_id != user_id:
        from flask import abort
        abort(403)
        
    return send_from_directory(UPLOAD_FOLDER, doc.storage_filename, as_attachment=False)

"""

if "# PATIENT MEDICAL DOCUMENTS" not in content:
    content = content.replace('if __name__ == "__main__":', new_routes + '\\nif __name__ == "__main__":')
    with open(app_py_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected patient medical documents routes.")
else:
    print("Routes already present.")
