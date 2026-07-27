from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()


# ==========================
# USER TABLE
# ==========================

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    bookings = db.relationship(
        "Booking",
        backref="user",
        lazy=True
    )



# ==========================
# ADMIN TABLE
# ==========================

class Admin(db.Model):

    __tablename__ = "admins"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )


    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )


    password = db.Column(
        db.String(255),
        nullable=False
    )



# ==========================
# EV STATION TABLE
# ==========================

class Station(db.Model):

    __tablename__ = "stations"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    name = db.Column(
        db.String(150),
        nullable=False
    )


    location = db.Column(
        db.String(255),
        nullable=False
    )


    latitude = db.Column(
        db.Float,
        nullable=False
    )


    longitude = db.Column(
        db.Float,
        nullable=False
    )


    charger_type = db.Column(
        db.String(100)
    )


    price = db.Column(
        db.Float,
        default=0
    )


    available_slots = db.Column(
        db.Integer,
        default=0
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    bookings = db.relationship(
        "Booking",
        backref="station",
        lazy=True
    )



# ==========================
# BOOKING TABLE
# ==========================

class Booking(db.Model):

    __tablename__ = "bookings"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


    station_id = db.Column(
        db.Integer,
        db.ForeignKey("stations.id"),
        nullable=False
    )


    booking_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    slot_time = db.Column(
        db.String(50)
    )


    amount = db.Column(
        db.Float,
        default=0
    )


    status = db.Column(
        db.String(50),
        default="Pending"
    )


    payment = db.relationship(
        "Payment",
        backref="booking",
        uselist=False
    )



# ==========================
# PAYMENT TABLE
# ==========================

class Payment(db.Model):

    __tablename__ = "payments"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    booking_id = db.Column(
        db.Integer,
        db.ForeignKey("bookings.id"),
        nullable=False
    )


    razorpay_order_id = db.Column(
        db.String(200)
    )


    razorpay_payment_id = db.Column(
        db.String(200)
    )


    razorpay_signature = db.Column(
        db.String(255)
    )


    amount = db.Column(
        db.Float,
        default=0
    )


    status = db.Column(
        db.String(50),
        default="Created"
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )