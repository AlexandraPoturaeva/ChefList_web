from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager, login_user
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

    @app.route('/login')
    def login():
        form = LoginForm()
        return render_template('login.html', form=form)

    @app.route('/profile', methods=['POST'])
    def profile():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли на сайт')
                return f'<h1> ' \
                       f'Логин: {user.email} <br> ' \
                       f'Дата регистрации: {user.created_at.strftime("%d.%m.%Y")}' \
                       f'</h1>'

        flash('Неверное имя и/или пароль')
        return redirect(url_for('login', next='profile'))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
