from datetime import datetime
import hmac
import hashlib
import razorpay

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
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

from models import (
    User,
    Station,
    Booking,
    Payment
)


main_bp = Blueprint(
    "main",
    __name__
)



# ==========================
# RAZORPAY CLIENT
# ==========================

def get_razorpay_client():

    return razorpay.Client(
        auth=(
            current_app.config["RAZORPAY_KEY_ID"],
            current_app.config["RAZORPAY_KEY_SECRET"]
        )
    )



# ==========================
# HOME
# ==========================

@main_bp.route("/")
def home():

    search=request.args.get("search","")
    charger=request.args.get("charger","")

    query=Station.query


    if search:

        query=query.filter(
            Station.location.ilike(
                f"%{search}%"
            )
        )


    if charger:

        query=query.filter_by(
            charger_type=charger
        )


    stations=query.all()


    return render_template(
        "index.html",
        stations=stations,
        search=search,
        charger=charger
    )



# ==========================
# REGISTER
# ==========================
# ==========================
# REGISTER
# ==========================

@main_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        try:

            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            password = request.form.get("password")


            # ==========================
            # VALIDATION
            # ==========================

            if not name or not email or not password:

                flash(
                    "Name, Email and Password are required",
                    "danger"
                )

                return redirect(
                    url_for("main.register")
                )


            # ==========================
            # CHECK EXISTING USER
            # ==========================

            existing_user = User.query.filter_by(
                email=email
            ).first()


            if existing_user:

                flash(
                    "Email already registered",
                    "danger"
                )

                return redirect(
                    url_for("main.register")
                )


            # ==========================
            # CREATE USER
            # ==========================

            user = User(

                name=name,

                email=email,

                phone=phone,

                password=generate_password_hash(
                    password
                ),

                role="user"

            )


            # ==========================
            # SAVE DATABASE
            # ==========================

            db.session.add(user)

            db.session.commit()



            flash(
                "Registration successful. Please login.",
                "success"
            )


            return redirect(
                url_for("main.login")
            )


        except Exception as e:


            db.session.rollback()


            print(
                "REGISTER ERROR:",
                e
            )


            flash(
                "Registration failed: " + str(e),
                "danger"
            )


            return redirect(
                url_for("main.register")
            )


    return render_template(
        "register.html"
    )

# ==========================
# LOGIN
# ==========================

@main_bp.route(
    "/login",
    methods=["GET","POST"]
)

def login():

    if request.method=="POST":


        user=User.query.filter_by(
            email=request.form.get("email")
        ).first()


        if user and check_password_hash(
            user.password,
            request.form.get("password")
        ):

            login_user(user)


            if user.role=="admin":

                return redirect(
                    url_for("admin.dashboard")
                )


            return redirect(
                url_for("main.dashboard")
            )


        flash(
            "Invalid login",
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

    return redirect(
        url_for("main.home")
    )



# ==========================
# DASHBOARD
# ==========================

@main_bp.route("/dashboard")
@login_required

def dashboard():

    bookings=Booking.query.filter_by(
        user_id=current_user.id
    ).all()


    return render_template(
        "dashboard.html",
        bookings=bookings
    )



# ==========================
# MAP
# ==========================

@main_bp.route("/map")
@login_required

def map_view():

    stations=Station.query.all()

    return render_template(
        "map.html",
        stations=stations
    )



# ==========================
# STATION DETAILS
# ==========================

@main_bp.route(
    "/station/<int:id>"
)

@login_required

def station_details(id):

    station=Station.query.get_or_404(id)


    return render_template(
        "station_details.html",
        station=station
    )



# ==========================
# BOOK + CREATE PAYMENT
# ==========================

@main_bp.route(
    "/book/<int:id>",
    methods=["GET","POST"]
)

@login_required

def book(id):

    station=Station.query.get_or_404(id)



    if request.method=="POST":


        if station.available_slots<=0:

            flash(
                "No slots available",
                "danger"
            )

            return redirect(
                url_for("main.home")
            )



        booking=Booking(

            user_id=current_user.id,

            station_id=station.id,

            booking_date=datetime.strptime(

                request.form.get("date"),

                "%Y-%m-%d"

            ).date(),


            booking_time=datetime.strptime(

                request.form.get("time"),

                "%H:%M"

            ).time(),


            status="Payment Pending"

        )


        db.session.add(booking)

        db.session.flush()



        # Amount in paise

        price = station.price_per_unit or 10

        amount = int(price * 10 * 100)



        client=get_razorpay_client()



        order=client.order.create({

            "amount":amount,

            "currency":"INR",

            "payment_capture":1,

            "receipt":
            f"booking_{booking.id}"

        })



        payment=Payment(

            booking_id=booking.id,

            razorpay_order_id=order["id"],

            amount=amount,

            status="created"

        )


        db.session.add(payment)

        db.session.commit()



        return render_template(

            "pay.html",

            booking=booking,

            station=station,

            payment=payment,

            razorpay_key_id=
            current_app.config["RAZORPAY_KEY_ID"],

            amount=amount

        )



    return render_template(
        "book.html",
        station=station
    )



# ==========================
# PAYMENT SUCCESS
# ==========================

@main_bp.route(
    "/payment/success",
    methods=["POST"]
)

@login_required

def payment_success():


    payment_id=request.form.get(
        "razorpay_payment_id"
    )


    order_id=request.form.get(
        "razorpay_order_id"
    )


    signature=request.form.get(
        "razorpay_signature"
    )


    payment=Payment.query.filter_by(
        razorpay_order_id=order_id
    ).first()



    if not payment:

        flash(
            "Payment not found",
            "danger"
        )

        return redirect(
            url_for("main.dashboard")
        )



    generated=hmac.new(

        current_app.config[
            "RAZORPAY_KEY_SECRET"
        ].encode(),

        f"{order_id}|{payment_id}".encode(),

        hashlib.sha256

    ).hexdigest()



    if generated != signature:


        payment.status="failed"

        db.session.commit()


        flash(
            "Payment verification failed",
            "danger"
        )


        return redirect(
            url_for("main.dashboard")
        )



    payment.razorpay_payment_id=payment_id

    payment.razorpay_signature=signature

    payment.status="paid"



    booking=payment.booking


    booking.status="Confirmed"



    booking.station.available_slots -= 1



    db.session.commit()



    flash(
        "Payment successful. Booking confirmed",
        "success"
    )


    return redirect(
        url_for("main.dashboard")
    )



# ==========================
# PAYMENT FAILURE
# ==========================

@main_bp.route(
    "/payment/failure"
)

@login_required

def payment_failure():


    flash(
        "Payment cancelled",
        "danger"
    )


    return redirect(
        url_for("main.dashboard")
    )