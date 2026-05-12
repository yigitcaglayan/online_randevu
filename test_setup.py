from app import app, db, User
from werkzeug.security import generate_password_hash

def test_db():
    with app.app_context():
        # Create tables
        db.create_all()
        print("Tables created.")
        
        # Check if user exists, if not create one
        if not User.query.filter_by(username='test_owner').first():
            u = User(username='test_owner', password_hash=generate_password_hash('pass'), role='owner')
            db.session.add(u)
            db.session.commit()
            print("Test owner created.")
        else:
            print("Test owner already exists.")
            
        print("Database setup verified successfully.")

if __name__ == "__main__":
    test_db()
