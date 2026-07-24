import unittest
from app import app, db
from models import User, PatientProfile

class TestProfileSettings(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            
            # Create a mock user
            u = User(email="test@example.com", first_name="John", last_name="Doe", country_of_residence="US", password_hash="hash")
            db.session.add(u)
            db.session.commit()
            
            from datetime import date
            p = PatientProfile(user_id=u.id, relationship_type="Self", first_name="John", last_name="Doe", date_of_birth=date(1990, 1, 1), gender="Male", nationality="US", country_of_residence="US")
            db.session.add(p)
            db.session.commit()
            
            self.user_id = u.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_settings_page_loads(self):
        with self.client.session_transaction() as sess:
            sess['registration_user_id'] = self.user_id
        
        res = self.client.get('/patient/profile/settings')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Profile Completion', res.data)
        self.assertIn(b'John', res.data)

if __name__ == '__main__':
    unittest.main()
