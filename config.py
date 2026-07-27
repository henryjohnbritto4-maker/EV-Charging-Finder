import os


class Config:

    # Security key
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "ev-charging-finder-secret-key"
    )


    # Database
    # Local development -> SQLite
    # Deployment -> PostgreSQL DATABASE_URL

    DATABASE_URL = os.environ.get(
        "DATABASE_URL"
    )


    if DATABASE_URL:
        # Fix Render PostgreSQL URL format
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
                1
            )

        SQLALCHEMY_DATABASE_URI = DATABASE_URL

    else:
        SQLALCHEMY_DATABASE_URI = (
            "sqlite:///database.db"
        )


    SQLALCHEMY_TRACK_MODIFICATIONS = False



    # ==========================
    # RAZORPAY CONFIGURATION
    # ==========================

    RAZORPAY_KEY_ID = os.environ.get(
        "RAZORPAY_KEY_ID",
        "YOUR_RAZORPAY_KEY_ID"
    )


    RAZORPAY_KEY_SECRET = os.environ.get(
        "RAZORPAY_KEY_SECRET",
        "YOUR_RAZORPAY_SECRET"
    )



    # ==========================
    # APPLICATION SETTINGS
    # ==========================

    UPLOAD_FOLDER = "static/uploads"


    MAX_CONTENT_LENGTH = (
        16 * 1024 * 1024
    )