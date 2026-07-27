import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, UPLOAD_FOLDER
from models import db, TreatmentRequest, MedicalDocument

def diagnose_document():
    with app.app_context():
        req = TreatmentRequest.query.filter_by(reference_id='TR-UEL6NYULN8').first()
        if not req:
            print("Request TR-UEL6NYULN8 not found.")
            return
            
        docs = req.medical_documents
        print(f"Found {len(docs)} documents for TR-UEL6NYULN8")
        
        for doc in docs:
            print(f"Doc ID: {doc.id}")
            print(f"Original filename: {doc.original_filename}")
            print(f"Storage filename: {doc.storage_filename}")
            file_path = os.path.join(UPLOAD_FOLDER, doc.storage_filename)
            exists = os.path.exists(file_path)
            print(f"Physical file exists at {file_path}: {exists}")

if __name__ == '__main__':
    diagnose_document()
