from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import db, User


auth_bp = Blueprint(
    "auth",
    __name__
)



# ======================
# REGISTER
# ======================

@auth_bp.route(
    "/register",
    methods=["GET","POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")


        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password)
        )


        db.session.add(user)
        db.session.commit()


        flash(
            "Registration successful",
            "success"
        )


        return redirect(
            url_for("auth.login")
        )


    return render_template(
        "register.html"
    )



# ======================
# LOGIN
# ======================

@auth_bp.route(
    "/login",
    methods=["GET","POST"]
)
def login():

    if request.method == "POST":

        email=request.form.get("email")
        password=request.form.get("password")


        user = User.query.filter_by(
            email=email
        ).first()


        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)


            return redirect(
                url_for("main.dashboard")
            )


        flash(
            "Invalid login details",
            "danger"
        )


    return render_template(
        "login.html"
    )



# ======================
# LOGOUT
# ======================

@auth_bp.route(
    "/logout"
)
@login_required
def logout():

    logout_user()


    return redirect(
        url_for("auth.login")
    )