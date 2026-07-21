from app import app
from database import db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    existing = User.query.filter_by(email="admin@gmail.com").first()

    if existing:
        print("Admin already exists.")
    else:
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            phone="9999999999",
            role="admin"
        )

        admin.password = generate_password_hash("admin123")

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully!")