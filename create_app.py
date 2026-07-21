from flask import Flask
from config import Config
from database import db
from flask_login import LoginManager


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)


    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = "login"


    from routes import main_bp
    from admin_routes import admin_bp


    app.register_blueprint(main_bp)

    app.register_blueprint(admin_bp)


    return app



app = create_app()


if __name__ == "__main__":
    app.run(debug=True)