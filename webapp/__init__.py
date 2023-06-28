from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from webapp.forms import (
    LoginForm,
    RegistrationForm,
    RenameShoppingList,
    AddIngredientForm,
    AddRecipeForm,
    CreateListForm,
    AddShoppingItem,
)
from webapp.model import (
    db,
    User,
    Ingredient,
    Product,
    Unit,
    ProductCategorie,
    Recipe,
    RecipeCategory,
    ShoppingList,
    ShoppingItem,
)
from webapp.utils import get_id_by_name
from uuid import uuid4


def flash_errors_from_form(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                'Ошибка в поле "{}": {}'.format(getattr(form, field).label.text, error),
                category="danger",
            )


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/registration")
    def registration():
        form = RegistrationForm()
        title = "Регистрация"
        return render_template("registration.html", form=form, page_title=title)

    @app.route("/process-reg", methods=["POST"])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            user_name = form.name.data
            user_email = form.email.data.lower()
            new_user = User(name=user_name, email=user_email)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash("Вы успешно зарегистрировались", category="success")
            return redirect(url_for("index"))

        else:
            flash_errors_from_form(form)
        return redirect(url_for("registration"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))

        form = LoginForm()
        email = form.email.data
        password = form.password.data

        if form.validate_on_submit():
            user = User.query.filter(User.email == email).one_or_none()
            if user:
                if user.check_password(password):
                    login_user(user)
                    flash("Вы успешно вошли на сайт", category="success")
                    return redirect(url_for("profile"))
                else:
                    flash("Неверный пароль", category="danger")
            else:
                flash(
                    "Пользователь с таким email не зарегистрирован", category="danger"
                )

        return render_template("login.html", form=form)

    @app.route("/profile")
    @login_required
    def profile():
        email = current_user.email
        created_at = current_user.created_at.strftime("%d.%m.%Y")
        title = "Моя страница"
        return render_template(
            "profile.html",
            page_title=title,
            user_email=email,
            user_created_at=created_at,
        )

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Вы успешно вышли из аккаунта", category="success")
        return redirect(url_for("index"))

    @app.route("/recipes")
    def recipes():
        return "Страница с рецептами"  # TODO: Сделать реальную страницу

    @app.route("/add_recipe", methods=["POST", "GET"])
    @login_required
    def add_recipe():
        if request.method == "GET":
            form = AddRecipeForm()
            return render_template("add_recipe.html", form=form)

        form = AddRecipeForm()
        if form.validate_on_submit():
            name = form.name.data

            category_id = get_id_by_name(
                form.category.data, db.session.query(RecipeCategory).all()
            )
            if not category_id:
                category = RecipeCategory(name=form.name.data)
                db.session.add(category)
                db.session.commit()
                category_id = get_id_by_name(
                    form.category.data, db.session.query(RecipeCategory).all()
                )

            description = form.description.data
            preparation_time = form.preparation_time.data
            cooking_time = form.cooking_time.data

            recipe = Recipe(
                name=name,
                user=current_user.id,
                category=category_id,
                description=description,
                preparation_time=preparation_time,
                cooking_time=cooking_time,
            )
            db.session.add(recipe)
            db.session.commit()

            recipe_id = get_id_by_name(recipe.name, db.session.query(Recipe).all())

            return redirect(url_for("add_ingredient", recipe_id=str(recipe_id)))
        else:
            flash_errors_from_form(form)
        return redirect(url_for("recipe", recipe_id=recipe_id))

    @app.route("/add_ingredient/<int:recipe_id>", methods=["POST", "GET"])
    @login_required
    def add_ingredient(recipe_id):
        print(Recipe.query.all())
        try:
            recipe = db.session.query(Recipe).get(recipe_id)
            print(recipe)
        except:
            flash("Неверный идентификатор рецепта")
            return redirect(url_for("recipes"))

        if request.method == "GET":
            recipe_name = db.session.query(Recipe).get(recipe_id).name
            ingredients = (
                db.session.query(Ingredient)
                .filter(Ingredient.recipe == recipe_id)
                .all()
            )
            ingredients_str = [str(ingredient) for ingredient in ingredients]
            form = AddIngredientForm()
            return render_template(
                "add_ingredient.html",
                recipe_id=recipe_id,
                form=form,
                recipe_name=recipe_name,
                ingredients=ingredients_str,
            )

        form = AddIngredientForm()
        if form.validate_on_submit():
            unit_id = get_id_by_name(form.unit.data, db.session.query(Unit).all())
            if not unit_id:
                unit = Unit(name=form.unit.data)
                db.session.add(unit)
                db.session.commit()
                unit_id = get_id_by_name(form.unit.data, db.session.query(Unit).all())

            product_id = get_id_by_name(
                form.product.data, db.session.query(Product).all()
            )
            if not product_id:
                product = Product(
                    name=form.product.data, category=1
                )  # TODO: Добавить работу с категориями
                db.session.add(product)
                db.session.commit()
                product_id = get_id_by_name(
                    form.product.data, db.session.query(Product).all()
                )

            quantity = form.quantity.data

            ingredient = Ingredient(
                product=product_id,
                quantity=quantity,
                unit=unit_id,
                recipe=recipe.id,
            )

            db.session.add(ingredient)
            db.session.commit()
            flash("Ингредиент добавлен", category="info")
            return redirect(url_for("add_ingredient", recipe_id=recipe.id))
        else:
            flash_errors_from_form(form)
        return redirect(url_for("add_ingredient", recipe_id=recipe.id))

    @app.route("/recipe/<int:recipe_id>")
    @login_required
    def recipe(recipe_id):
        try:
            recipe = db.session.query(Recipe).get(recipe_id)
        except:
            return redirect(url_for("recipes"))
        to_view = {}
        to_view["name"] = recipe.name
        to_view["description"] = recipe.description
        to_view["cooking_time"] = recipe.cooking_time
        to_view["preparation_time"] = recipe.preparation_time
        ingredients = (
            db.session.query(Ingredient).filter(Ingredient.recipe == recipe_id).all()
        )
        to_view["ingredients"] = [str(ingredient) for ingredient in ingredients]
        return render_template("recipe.html", to_view=to_view)

    @app.route("/my-lists")
    @login_required
    def show_my_shopping_lists():
        session["url"] = url_for("show_my_shopping_lists")
        form = CreateListForm()
        form_2 = RenameShoppingList()
        user_id = current_user.id
        user_shopping_lists = ShoppingList.query.filter(
            ShoppingList.user_id == user_id
        ).all()
        title = "Мои списки покупок"
        return render_template(
            "my_shopping_lists.html",
            form=form,
            form_2=form_2,
            user_shopping_lists=user_shopping_lists,
            page_title=title,
        )

    @app.route("/create-new-list", methods=["GET", "POST"])
    def create_new_shopping_list():
        form = CreateListForm()
        public_id = str(uuid4())
        user_id = current_user.id
        if form.validate_on_submit():
            new_shopping_list = ShoppingList(
                name=form.name.data, user_id=user_id, public_id=public_id
            )
            db.session.add(new_shopping_list)
            db.session.commit()
            flash("Новый список успешно создан", category="success")
            return redirect(url_for("show_shopping_list", public_id=public_id))
        else:
            flash_errors_from_form(form)
        return redirect(url_for("show_my_shopping_lists"))

    @app.route("/delete-shopping-list/<shopping_list_id>", methods=["GET", "POST"])
    def delete_shopping_list(shopping_list_id):
        shopping_list_to_delete = ShoppingList.query.filter(
            ShoppingList.id == shopping_list_id
        ).one_or_none()

        if shopping_list_to_delete:
            db.session.delete(shopping_list_to_delete)
            db.session.commit()
            flash("Список удалён", category="success")
        else:
            flash("При удалении списка возникла ошибка", category="danger")

        return redirect(url_for("show_my_shopping_lists"))

    @app.route("/rename-shopping-list/", methods=["POST"])
    def rename_shopping_list():
        form = RenameShoppingList()

        if form.validate_on_submit():
            new_name = form.new_name.data
            shopping_list_id = form.shopping_list_id.data
            shopping_list_to_rename = ShoppingList.query.filter(
                ShoppingList.id == shopping_list_id
            ).one_or_none()
            shopping_list_to_rename.name = new_name
            db.session.commit()
            flash("Список переименован", category="success")

        else:
            flash_errors_from_form(form)

        return redirect(session["url"])

    @app.route("/my-lists/<public_id>", methods=["GET", "POST"])
    def show_shopping_list(public_id):
        form = AddShoppingItem()
        shopping_list = ShoppingList.query.filter(
            ShoppingList.public_id == public_id
        ).one_or_none()
        shopping_list_id = shopping_list.id
        shopping_items = ShoppingItem.query.filter(
            ShoppingItem.shopping_list_id == shopping_list_id
        ).all()
        if shopping_list:
            page_title = shopping_list.name
            return render_template(
                "shopping_list.html",
                page_title=page_title,
                form=form,
                shopping_list_public_id=public_id,
                shopping_items=shopping_items,
            )
        else:
            flash("При создании списка возникла ошибка", category="danger")
            return redirect(url_for("show_my_shopping_lists"))

    @app.route("/add-item/<shopping_list_public_id>", methods=["GET", "POST"])
    def add_item_to_shopping_list(shopping_list_public_id):
        form = AddShoppingItem()
        if form.validate_on_submit():
            shopping_list = ShoppingList.query.filter(
                ShoppingList.public_id == shopping_list_public_id
            ).one_or_none()
            shopping_list_id = shopping_list.id
            new_item = ShoppingItem(
                name=form.name.data, shopping_list_id=shopping_list_id
            )
            db.session.add(new_item)
            db.session.commit()
            flash("Новый продукт успешно добавлен", category="success")
        else:
            flash_errors_from_form(form)

        return redirect(
            url_for("show_shopping_list", public_id=shopping_list_public_id)
        )

    @app.route("/delete-item/<shopping_list_public_id>/<item_id>")
    def delete_item_from_shopping_list(shopping_list_public_id, item_id):
        item_to_delete = ShoppingItem.query.filter(
            ShoppingItem.id == item_id
        ).one_or_none()

        if item_to_delete:
            db.session.delete(item_to_delete)
            db.session.commit()
            flash("Продукт удалён", category="success")
        else:
            flash("При удалении продукта возникла ошибка", category="danger")

        return redirect(
            url_for("show_shopping_list", public_id=shopping_list_public_id)
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
