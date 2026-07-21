from datetime import datetime

from database import db

from flask_login import UserMixin





# ==========================
# USER TABLE
# ==========================

class User(
    db.Model,
    UserMixin
):

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



    phone = db.Column(
        db.String(20),
        nullable=False
    )



    password = db.Column(
        db.String(255),
        nullable=False
    )



    role = db.Column(
        db.String(20),
        default="user"
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
# STATION TABLE
# ==========================

class Station(db.Model):

    __tablename__ = "stations"



    id = db.Column(
        db.Integer,
        primary_key=True
    )



    name = db.Column(
        db.String(100),
        nullable=False
    )



    location = db.Column(
        db.String(200),
        nullable=False
    )



    charger_type = db.Column(
        db.String(50),
        nullable=False
    )



    total_slots = db.Column(
        db.Integer,
        nullable=False
    )



    available_slots = db.Column(
        db.Integer,
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
        db.Date,
        nullable=False
    )



    booking_time = db.Column(
        db.Time,
        nullable=False
    )



    status = db.Column(
        db.String(20),
        default="Pending"
    )



    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )