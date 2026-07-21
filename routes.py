from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database import db
from models import User, Station, Booking


main_bp = Blueprint("main", __name__)


# ==========================
# HOME
# ==========================


@main_bp.route("/")
def home():

    search = request.args.get("search", "")

    charger = request.args.get("charger", "")

    query = Station.query

    if search:

        query = query.filter(
            Station.location.ilike(f"%{search}%")
        )

    if charger:

        query = query.filter_by(
            charger_type=charger
        )

    stations = query.all()

    return render_template(
        "index.html",
        stations=stations,
        search=search,
        charger=charger
    )


# ==========================
# REGISTER
# ==========================

@main_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))


    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")


        existing_user = User.query.filter_by(
            email=email
        ).first()


        if existing_user:

            flash(
                "Email already registered.",
                "danger"
            )

            return redirect(
                url_for("main.register")
            )


        user = User(

            name=name,
            email=email,
            phone=phone,
            role="user"

        )


        user.password = generate_password_hash(
            password
        )


        db.session.add(user)

        db.session.commit()


        flash(
            "Registration successful. Please login.",
            "success"
        )


        return redirect(
            url_for("main.login")
        )


    return render_template(
        "register.html"
    )



# ==========================
# LOGIN
# ==========================

@main_bp.route("/login", methods=["GET", "POST"])
def login():


    if current_user.is_authenticated:


        if current_user.role == "admin":

            return redirect(
                url_for("admin.dashboard")
            )


        return redirect(
            url_for("main.dashboard")
        )



    if request.method == "POST":


        email = request.form.get("email")

        password = request.form.get("password")



        user = User.query.filter_by(
            email=email
        ).first()



        if user and check_password_hash(
            user.password,
            password
        ):


            login_user(user)



            flash(
                "Login successful.",
                "success"
            )



            if user.role == "admin":

                return redirect(
                    url_for("admin.dashboard")
                )



            return redirect(
                url_for("main.dashboard")
            )



        flash(
            "Invalid email or password.",
            "danger"
        )


    return render_template(
        "login.html"
    )



# ==========================
# LOGOUT
# ==========================

@main_bp.route("/logout")
@login_required
def logout():


    logout_user()


    flash(
        "Logged out successfully.",
        "success"
    )


    return redirect(
        url_for("main.home")
    )



# ==========================
# USER DASHBOARD
# ==========================

@main_bp.route("/dashboard")
@login_required
def dashboard():


    bookings = Booking.query.filter_by(

        user_id=current_user.id

    ).order_by(

        Booking.id.desc()

    ).all()



    return render_template(

        "dashboard.html",

        bookings=bookings

    )



# ==========================
# MAP VIEW
# ==========================

@main_bp.route("/map")
@login_required
def map_view():


    stations = Station.query.all()



    return render_template(

        "map.html",

        stations=stations

    )



# ==========================
# BOOK STATION
# ==========================

@main_bp.route(
    "/book/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def book(id):


    station = Station.query.get_or_404(id)



    if request.method == "POST":


        if station.available_slots <= 0:


            flash(
                "No charging slots available.",
                "danger"
            )


            return redirect(
                url_for("main.home")
            )



        booking_date = datetime.strptime(

            request.form.get("date"),

            "%Y-%m-%d"

        ).date()



        booking_time = datetime.strptime(

            request.form.get("time"),

            "%H:%M"

        ).time()



        booking = Booking(


            user_id=current_user.id,

            station_id=station.id,

            booking_date=booking_date,

            booking_time=booking_time,

            status="Pending"

        )



        db.session.add(booking)



        station.available_slots -= 1



        db.session.commit()



        flash(

            "Charging slot booked successfully.",

            "success"

        )



        return redirect(

            url_for("main.dashboard")

        )



    return render_template(

        "book.html",

        station=station

    )