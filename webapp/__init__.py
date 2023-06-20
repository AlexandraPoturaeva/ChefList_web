from uuid import uuid4
from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from webapp.forms import LoginForm, RegistrationForm, CreateListForm, AddShoppingItem
from webapp.model import db, User, ShoppingList, ShoppingItem


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

    @app.route('/my-lists')
    @login_required
    def show_my_shopping_lists():
        form = CreateListForm()
        user_id = current_user.id
        user_shopping_lists = ShoppingList.query.filter(ShoppingList.user_id == user_id).all()
        return render_template('my_shopping_lists.html', form=form, user_shopping_lists=user_shopping_lists)

    @app.route('/create-new-list', methods=['GET', 'POST'])
    def create_new_shopping_list():
        form = CreateListForm()
        public_id = str(uuid4())
        user_id = current_user.id
        if form.validate_on_submit():
            new_shopping_list = ShoppingList(name=form.name.data, user_id=user_id, public_id=public_id)
            db.session.add(new_shopping_list)
            db.session.commit()
            flash('Новый список успешно создан')
            return redirect(url_for('show_shopping_list', public_id=public_id))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": {}'.format(
                        getattr(form, field).label.text,
                        error
                    ))
        return redirect(url_for('show_my_lists'))

    @app.route('/my-lists/<public_id>', methods=['GET', 'POST'])
    @login_required
    def show_shopping_list(public_id):
        form = AddShoppingItem()
        shopping_list = ShoppingList.query.filter(ShoppingList.public_id == public_id).one_or_none()
        shopping_list_id = shopping_list.id
        shopping_items = ShoppingItem.query.filter(ShoppingItem.shopping_list_id == shopping_list_id).all()
        if shopping_list:
            page_title = shopping_list.name
            return render_template('shopping_list.html',
                                   page_title=page_title,
                                   form=form,
                                   shopping_list_public_id=public_id,
                                   shopping_items=shopping_items)
        else:
            flash('При создании списка возникла ошибка')
            return redirect(url_for('show_my_shopping_lists'))

    @app.route('/add-item/<shopping_list_public_id>', methods=['GET', 'POST'])
    def add_item_to_shopping_list(shopping_list_public_id):
        form = AddShoppingItem()
        if form.validate_on_submit():
            shopping_list = ShoppingList.query.filter(ShoppingList.public_id == shopping_list_public_id).one_or_none()
            shopping_list_id = shopping_list.id
            new_item = ShoppingItem(name=form.name.data, shopping_list_id=shopping_list_id)
            db.session.add(new_item)
            db.session.commit()
            flash('Новый продукт успешно добавлен')
            return redirect(url_for('show_shopping_list', public_id=shopping_list_public_id))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": {}'.format(
                        getattr(form, field).label.text,
                        error
                    ))
        return redirect(url_for('show_shopping_list', public_id=shopping_list_public_id))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
