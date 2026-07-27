from app import create_app
from models import db, Admin
from werkzeug.security import generate_password_hash


app = create_app()


with app.app_context():

    admin = Admin(
        username="admin",
        email="admin@gmail.com",
        password=generate_password_hash("admin123")
    )

    db.session.add(admin)
    db.session.commit()


print("Admin created")