from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    DateField,
    TimeField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)



# ==========================
# REGISTER FORM
# ==========================

class RegisterForm(FlaskForm):

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )


    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )


    phone = StringField(
        "Phone",
        validators=[
            DataRequired(),
            Length(min=10, max=15)
        ]
    )


    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )


    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match"
            )
        ]
    )


    submit = SubmitField("Register")





# ==========================
# LOGIN FORM
# ==========================

class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )


    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )


    submit = SubmitField("Login")





# ==========================
# BOOKING FORM
# ==========================

class BookingForm(FlaskForm):

    booking_date = DateField(
        "Booking Date",
        validators=[
            DataRequired()
        ]
    )


    booking_time = TimeField(
        "Booking Time",
        validators=[
            DataRequired()
        ]
    )


    submit = SubmitField("Book Slot")