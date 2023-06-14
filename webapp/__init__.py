from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager,current_user, login_required, login_user, logout_user
from webapp.forms import LoginForm, RegistrationForm
from webapp.model import db, User


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/registration")
    def registration():
        form = RegistrationForm()
        return render_template('registration.html', form=form)

    @app.route("/process-reg", methods=['POST'])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(name=form.name.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались')
            return redirect(url_for('index'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": {}'.format(
                        getattr(form, field).label.text,
                        error
                    ))
        return redirect(url_for('registration'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('profile'))

        form = LoginForm()
        email = form.email.data
        password = form.password.data

        if form.validate_on_submit():
            user = User.query.filter(User.email == email).one_or_none()
            if user:
                if user.check_password(password):
                    login_user(user)
                    flash('Вы успешно вошли на сайт')
                    return redirect(url_for('profile'))
                else:
                    flash('Неверный пароль')
            else:
                flash('Пользователь с таким email не зарегистрирован')

        return render_template('login.html', form=form)

    @app.route('/profile')
    @login_required
    def profile():
        email = current_user.email
        created_at = current_user.created_at.strftime("%d.%m.%Y")
        return render_template('profile.html', user_email=email, user_created_at=created_at)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Вы успешно вышли из аккаунта')
        return redirect(url_for('index'))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
