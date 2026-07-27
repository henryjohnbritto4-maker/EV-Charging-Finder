from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import check_password_hash

from models import (
    db,
    Admin,
    Station,
    Booking
)


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)



# ==========================
# ADMIN LOGIN
# ==========================

@admin_bp.route(
    "/login",
    methods=["GET","POST"]
)
def login():


    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )


        admin = Admin.query.filter_by(
            username=username
        ).first()


        if admin and check_password_hash(
            admin.password,
            password
        ):

            session["admin_id"] = admin.id


            flash(
                "Login successful",
                "success"
            )


            return redirect(
                url_for(
                    "admin.dashboard"
                )
            )


        flash(
            "Invalid username or password",
            "danger"
        )


    return render_template(
        "admin/login.html"
    )



# ==========================
# ADMIN CHECK
# ==========================

def admin_required():

    return "admin_id" in session



# ==========================
# DASHBOARD
# ==========================

@admin_bp.route("/dashboard")
def dashboard():


    if not admin_required():

        return redirect(
            url_for(
                "admin.login"
            )
        )


    stations = Station.query.all()


    return render_template(
        "admin/dashboard.html",
        stations=stations
    )



# ==========================
# ADD STATION
# ==========================

@admin_bp.route(
    "/add_station",
    methods=["GET","POST"]
)
def add_station():


    if not admin_required():

        return redirect(
            url_for(
                "admin.login"
            )
        )


    if request.method=="POST":


        station = Station(

            name=request.form.get("name"),

            location=request.form.get("location"),

            charger_type=request.form.get(
                "charger_type"
            ),

            latitude=float(
                request.form.get(
                    "latitude"
                )
            ),

            longitude=float(
                request.form.get(
                    "longitude"
                )
            ),

            available_slots=int(
                request.form.get(
                    "available_slots"
                )
            ),

            price=float(
                request.form.get(
                    "price"
                )
            )
        )


        db.session.add(station)

        db.session.commit()


        flash(
            "Station added",
            "success"
        )


        return redirect(
            url_for(
                "admin.dashboard"
            )
        )


    return render_template(
        "admin/add_station.html"
    )



# ==========================
# BOOKINGS
# ==========================

@admin_bp.route("/bookings")
def bookings():


    if not admin_required():

        return redirect(
            url_for(
                "admin.login"
            )
        )


    bookings = Booking.query.all()


    return render_template(
        "admin/bookings.html",
        bookings=bookings
    )



# ==========================
# LOGOUT
# ==========================

@admin_bp.route("/logout")
def logout():

    session.pop(
        "admin_id",
        None
    )


    return redirect(
        url_for(
            "admin.login"
        )
    )