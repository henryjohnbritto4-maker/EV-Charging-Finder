from flask import Flask

from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config
from models import db, User


print("APP FILE STARTED")


# ==========================
# EXTENSIONS
# ==========================

login_manager = LoginManager()
migrate = Migrate()



# ==========================
# USER LOGIN LOADER
# ==========================

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(
        int(user_id)
    )



# ==========================
# APP FACTORY
# ==========================

def create_app():

    app = Flask(__name__)


    # Configuration

    app.config.from_object(
        Config
    )


    # Extensions

    db.init_app(app)

    login_manager.init_app(
        app
    )

    migrate.init_app(
        app,
        db
    )


    login_manager.login_view = "auth.login"



    # ==========================
    # USER ROUTES
    # ==========================

    from routes import main_bp

    app.register_blueprint(
        main_bp
    )



    # ==========================
    # AUTH ROUTES
    # ==========================

    try:

        from auth_routes import auth_bp

        app.register_blueprint(
            auth_bp,
            url_prefix="/auth"
        )

        print("Auth loaded")


    except Exception as e:

        print(
            "Auth error:",
            e
        )



    # ==========================
    # ADMIN ROUTES
    # ==========================

    try:

        from admin_routes import admin_bp

        app.register_blueprint(
            admin_bp
        )

        print("Admin loaded")


    except Exception as e:

        print(
            "Admin error:",
            e
        )



    # ==========================
    # PAYMENT ROUTES
    # ==========================

    try:

        from payment_routes import payment_bp

        app.register_blueprint(
            payment_bp
        )

        print("Payment loaded")


    except Exception as e:

        print(
            "Payment error:",
            e
        )



    # Create tables

    with app.app_context():

        db.create_all()



    return app





# ==========================
# RUN
# ==========================

app = create_app()


if __name__ == "__main__":

    app.run(
        debug=True
    )