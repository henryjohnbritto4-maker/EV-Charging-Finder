from flask import Flask

from flask_login import LoginManager

from database import db

from config import Config



login_manager = LoginManager()



def create_app():


    app = Flask(__name__)


    # SECRET KEY FIX

    app.config["SECRET_KEY"] = "ev_charging_finder_secret_key_2026"



    # DATABASE

    app.config.from_object(Config)



    db.init_app(app)



    # LOGIN MANAGER

    login_manager.init_app(app)


    login_manager.login_view = "main.login"



    # USER LOADER

    from models import User


    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))





    # BLUEPRINTS


    from routes import main_bp

    from admin_routes import admin_bp



    app.register_blueprint(
        main_bp
    )


    app.register_blueprint(
        admin_bp
    )





    # CREATE DATABASE

    with app.app_context():

        db.create_all()



    return app





app = create_app()



if __name__ == "__main__":

    app.run(
        debug=True
    )