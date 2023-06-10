from flask import Flask, flash, redirect, render_template, url_for
from webapp.forms import RegistrationForm
from webapp.model import db, User


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

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

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
