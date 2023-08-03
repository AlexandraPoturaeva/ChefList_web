from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from webapp.db import db
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.utils import flash_errors_from_form

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("/registration")
def registration():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    title = "Регистрация"
    return render_template(
        "user/registration.html",
        form=form,
        page_title=title,
    )


@blueprint.route("/process-reg", methods=["POST"])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_name = form.name.data
        if user_name.lower() == "admin":
            flash(
                "Регистрация под таким именем невозможна",
                category="danger",
            )
        else:
            user_email = form.email.data.lower()
            new_user = User(name=user_name, email=user_email)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash("Вы успешно зарегистрировались", category="success")
            return redirect(url_for("user.login"))

    else:
        flash_errors_from_form(form)
    return redirect(url_for("user.registration"))


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    email = form.email.data
    password = form.password.data

    if form.validate_on_submit():
        user = User.query.filter(User.email == email).one_or_none()
        if user:
            if user.check_password(password):
                login_user(user)
                flash("Вы успешно вошли на сайт", category="success")
                return redirect(url_for("index"))
            else:
                flash("Неверный пароль", category="danger")
        else:
            flash("Пользователь с таким email не зарегистрирован", category="danger")

    return render_template("user/login.html", form=form)


@blueprint.route("/profile")
@login_required
def profile():
    user = current_user
    title = "Моя страница"
    return render_template(
        "user/profile.html",
        page_title=title,
        user=user,
    )


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из аккаунта", category="success")
    return redirect(url_for("index"))
