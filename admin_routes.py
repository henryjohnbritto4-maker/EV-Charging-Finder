from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from database import db

from models import (
    Station,
    Booking
)



# ==========================
# ADMIN BLUEPRINT
# ==========================

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)





# ==========================
# ADMIN CHECK
# ==========================

def admin_required():

    if not current_user.is_authenticated:

        return False


    if current_user.role != "admin":

        flash(
            "Admin access required.",
            "danger"
        )

        return False


    return True







# ==========================
# ADMIN DASHBOARD
# ==========================

@admin_bp.route("/dashboard")
@login_required
def dashboard():


    if not admin_required():

        return redirect(
            url_for("main.home")
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

@login_required
def add_station():


    if not admin_required():

        return redirect(
            url_for("main.home")
        )



    if request.method == "POST":


        station = Station(

            name=request.form.get("name"),

            location=request.form.get("location"),

            charger_type=request.form.get("charger_type"),

            total_slots=int(
                request.form.get("total_slots")
            ),

            available_slots=int(
                request.form.get("available_slots")
            ),

            latitude=float(
                request.form.get("latitude")
            ),

            longitude=float(
                request.form.get("longitude")
            )

        )



        db.session.add(station)

        db.session.commit()



        flash(
            "Station added successfully.",
            "success"
        )


        return redirect(
            url_for("admin.dashboard")
        )



    return render_template(
        "admin/add_station.html"
    )









# ==========================
# EDIT STATION
# ==========================

@admin_bp.route(
    "/edit_station/<int:id>",
    methods=["GET","POST"]
)

@login_required
def edit_station(id):


    if not admin_required():

        return redirect(
            url_for("main.home")
        )



    station = Station.query.get_or_404(id)



    if request.method == "POST":


        station.name = request.form.get(
            "name"
        )


        station.location = request.form.get(
            "location"
        )


        station.charger_type = request.form.get(
            "charger_type"
        )


        station.total_slots = int(
            request.form.get(
                "total_slots"
            )
        )


        station.available_slots = int(
            request.form.get(
                "available_slots"
            )
        )


        station.latitude = float(
            request.form.get(
                "latitude"
            )
        )


        station.longitude = float(
            request.form.get(
                "longitude"
            )
        )



        db.session.commit()



        flash(
            "Station updated successfully.",
            "success"
        )



        return redirect(
            url_for("admin.dashboard")
        )



    return render_template(
        "admin/edit_station.html",
        station=station
    )









# ==========================
# DELETE STATION
# ==========================

@admin_bp.route(
    "/delete_station/<int:id>"
)

@login_required
def delete_station(id):


    if not admin_required():

        return redirect(
            url_for("main.home")
        )



    station = Station.query.get_or_404(id)



    db.session.delete(station)

    db.session.commit()



    flash(
        "Station deleted successfully.",
        "success"
    )



    return redirect(
        url_for("admin.dashboard")
    )









# ==========================
# VIEW BOOKINGS
# ==========================

@admin_bp.route("/bookings")
@login_required
def bookings():


    if not admin_required():

        return redirect(
            url_for("main.home")
        )



    bookings = Booking.query.order_by(
        Booking.id.desc()
    ).all()



    return render_template(
        "admin/bookings.html",
        bookings=bookings
    )









# ==========================
# UPDATE BOOKING STATUS
# ==========================

@admin_bp.route(
    "/update_booking/<int:id>/<status>"
)

@login_required
def update_booking(id, status):


    if not admin_required():

        return redirect(
            url_for("main.home")
        )



    booking = Booking.query.get_or_404(id)



    if status in [
        "Approved",
        "Rejected"
    ]:


        booking.status = status


        db.session.commit()



        flash(
            "Booking status updated.",
            "success"
        )


    else:


        flash(
            "Invalid booking status.",
            "danger"
        )



    return redirect(
        url_for("admin.bookings")
    )