import razorpay

from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
    current_app
)

from models import db, Payment, Booking


payment_bp = Blueprint(
    "payment",
    __name__
)


@payment_bp.route(
    "/create-payment/<int:booking_id>"
)
def create_payment(booking_id):

    booking = Booking.query.get_or_404(
        booking_id
    )


    client = razorpay.Client(
        auth=(
            current_app.config["RAZORPAY_KEY_ID"],
            current_app.config["RAZORPAY_KEY_SECRET"]
        )
    )


    order = client.order.create(
        {
            "amount": int(booking.amount * 100),
            "currency": "INR",
            "payment_capture": 1
        }
    )


    payment = Payment(
        booking_id=booking.id,
        razorpay_order_id=order["id"],
        amount=booking.amount,
        status="Created"
    )


    db.session.add(payment)
    db.session.commit()


    return render_template(
        "payment.html",
        booking=booking,
        payment=payment,
        key=current_app.config["RAZORPAY_KEY_ID"]
    )



@payment_bp.route(
    "/payment-success",
    methods=["POST"]
)
def payment_success():

    payment_id = request.form.get(
        "razorpay_payment_id"
    )

    order_id = request.form.get(
        "razorpay_order_id"
    )


    payment = Payment.query.filter_by(
        razorpay_order_id=order_id
    ).first()


    if payment:

        payment.razorpay_payment_id = payment_id
        payment.status = "Paid"

        payment.booking.status = "Confirmed"

        db.session.commit()


    return render_template(
        "payment_success.html"
    )