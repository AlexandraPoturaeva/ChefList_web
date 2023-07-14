import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_migrate import Migrate
from webapp.forms import (
    AddIngredientForm,
    AddRecipeForm,
    AddShoppingItem,
    CreateListForm,
    EditQuantityOfShoppingItemForm,
    LoginForm,
    RegistrationForm,
    RenameElement,
    ChooseListForm,
)
from webapp.model import (
    db,
    User,
    Ingredient,
    Product,
    UNITS,
    Recipe,
    ShoppingList,
    ShoppingItem,
    RECIPE_CATEGORIES,
    PRODUCT_CATEGORIES,
)
from uuid import uuid4

database_uri = os.environ.get("DATABASE_URL")
secret_key = os.environ.get("FLASK_SECRET_KEY")


def flash_errors_from_form(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                'Ошибка в поле "{}": {}'.format(getattr(form, field).label.text, error),
                category="danger",
            )


def update_item_to_shopping_list(shopping_list, name, quantity, unit):
    exist_item = ShoppingItem.query.filter(
        ShoppingItem.shopping_list_id == shopping_list.id,
        ShoppingItem.name == name,
        ShoppingItem.unit == unit,
    ).one_or_none()

    if exist_item:
        exist_item.quantity += quantity
        db.session.commit()
    else:
        new_item = ShoppingItem(
            name=name,
            quantity=quantity,
            shopping_list_id=shopping_list.id,
            unit=unit,
        )
        db.session.add(new_item)
        db.session.commit()


def update_recipe_to_shopping_list(shopping_list, recipe, portions):
    for ingredient in recipe.ingredients:
        update_item_to_shopping_list(
            shopping_list=shopping_list,
            name=ingredient.product.name,
            quantity=ingredient.quantity * portions,
            unit=ingredient.unit,
        )


def create_app(database_uri=database_uri, secret_key=secret_key):
    app = Flask(__name__)

    if database_uri and secret_key:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
        app.config["SECRET_KEY"] = secret_key
    else:
        app.config.from_pyfile("config.py")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            last_user_shopping_list = (
                ShoppingList.query.filter(ShoppingList.user_id == current_user.id)
                .order_by(ShoppingList.created_at.desc())
                .first()
            )

            if last_user_shopping_list:
                shopping_list_public_id = last_user_shopping_list.public_id
                return redirect(
                    url_for("show_shopping_list", public_id=shopping_list_public_id)
                )
            else:
                return redirect(url_for("show_my_shopping_lists"))

        return render_template("index.html")

    @app.route("/registration")
    def registration():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = RegistrationForm()
        title = "Регистрация"
        return render_template(
            "registration.html",
            form=form,
            page_title=title,
        )

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
            return redirect(url_for("login"))

        else:
            flash_errors_from_form(form)
        return redirect(url_for("registration"))

    @app.route("/login", methods=["GET", "POST"])
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
                flash(
                    "Пользователь с таким email не зарегистрирован", category="danger"
                )

        return render_template("login.html", form=form)

    @app.route("/profile")
    @login_required
    def profile():
        user = current_user
        title = "Моя страница"
        return render_template(
            "profile.html",
            page_title=title,
            user=user,
        )

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Вы успешно вышли из аккаунта", category="success")
        return redirect(url_for("index"))

    @app.route("/recipes")
    def recipes():
        admin = User.query.filter(User.name == "admin").one_or_none()
        if admin:
            public_recipes = Recipe.query.filter(Recipe.user_id == admin.id).all()
            return render_template("public_recipes.html", public_recipes=public_recipes)
        else:
            flash("Нет общедоступных рецептов!", category="danger")
            return redirect(url_for("index"))

    @app.route("/my_recipes")
    @login_required
    def my_recipes():
        user_recipes = Recipe.query.filter(Recipe.user_id == current_user.id).all()
        return render_template("my_recipes.html", user_recipes=user_recipes)

    @app.route("/add_recipe", methods=["POST", "GET"])
    @login_required
    def add_recipe():
        if request.method == "GET":
            form = AddRecipeForm()
            return render_template("add_recipe.html", form=form)

        form = AddRecipeForm()
        if form.validate_on_submit():
            name = form.name.data

            recipe_name_already_used = bool(
                Recipe.query.filter(
                    Recipe.name == name, Recipe.user_id == current_user.id
                ).count()
            )
            if recipe_name_already_used:
                flash("Рецепт с таким именем уже существует", category="danger")
                return render_template("add_recipe.html", form=form)

            category = form.category.data

            description = form.description.data
            preparation_time = form.preparation_time.data
            cooking_time = form.cooking_time.data

            recipe = Recipe(
                name=name,
                user_id=current_user.id,
                category=category,
                description=description,
                preparation_time=preparation_time,
                cooking_time=cooking_time,
            )
            db.session.add(recipe)
            db.session.commit()

            recipe_id = (
                Recipe.query.filter(
                    Recipe.name == recipe.name, Recipe.user_id == recipe.user_id
                )
                .one()
                .id
            )

            return redirect(
                url_for(
                    "add_ingredient",
                    recipe_id=recipe_id,
                    RECIPE_CATEGORIES=RECIPE_CATEGORIES,
                    PRODUCT_CATEGORIES=PRODUCT_CATEGORIES,
                )
            )
        else:
            flash_errors_from_form(form)
        return redirect(url_for("recipes", recipe_id=recipe_id))

    @app.route("/add_ingredient/<int:recipe_id>", methods=["POST", "GET"])
    @login_required
    def add_ingredient(recipe_id):
        print(Recipe.query.all())
        try:
            recipe = db.session.query(Recipe).get(recipe_id)
        except:
            flash("Неверный идентификатор рецепта")
            return redirect(url_for("my_recipes"))

        if request.method == "GET":
            form = AddIngredientForm()
            return render_template(
                "add_ingredient.html",
                form=form,
                recipe=recipe,
                PRODUCT_CATEGORIES=PRODUCT_CATEGORIES,
                RECIPE_CATEGORIES=RECIPE_CATEGORIES,
            )

        form = AddIngredientForm()
        if form.validate_on_submit():
            unit = form.unit.data

            product = Product.query.filter(
                Product.name == form.product.data
            ).one_or_none()
            if not product:
                product = Product(name=form.product.data, category=form.category.data)
                db.session.add(product)
                db.session.commit()
                product_id = (
                    Product.query.filter(Product.name == form.product.data).one().id
                )
            else:
                product_id = product.id

            quantity = form.quantity.data

            ingredient = Ingredient(
                product_id=product_id,
                quantity=quantity,
                unit=unit,
                recipe_id=recipe.id,
            )

            db.session.add(ingredient)
            db.session.commit()
            flash("Ингредиент добавлен", category="info")
            return redirect(
                url_for(
                    "add_ingredient",
                    recipe_id=recipe.id,
                )
            )
        else:
            flash_errors_from_form(form)
        return redirect(
            url_for(
                "add_ingredient",
                recipe_id=recipe.id,
            )
        )

    @app.route("/recipes/<int:recipe_id>")
    def recipe(recipe_id):
        try:
            recipe = db.session.query(Recipe).get(recipe_id)
        except:
            return redirect(url_for("recipes"))

        admin = User.query.filter(User.name == "admin").one_or_none()

        if admin:
            admin_id = admin.id
        else:
            admin_id = None

        if current_user.is_anonymous:
            if recipe.user_id != admin_id:
                flash("Рецепт доступен только авторизированным пользователям!")
                return redirect(url_for("recipes"))
        else:
            if recipe.user_id != admin_id and recipe.user_id != current_user.id:
                flash("У Вас нет прав на доступ к этому рецепту!")
                return redirect(url_for("recipes"))
        form = ChooseListForm()
        shopping_lists_count = ShoppingList.query.filter(
            ShoppingList.user_id == current_user.id
        ).count()
        if shopping_lists_count == 0:
            new_shopping_list = ShoppingList(
                name="Мой список покупок",
                user_id=current_user.id,
                public_id=str(uuid4()),
            )
            db.session.add(new_shopping_list)
            db.session.commit()
        shopping_lists = ShoppingList.query.filter(
            ShoppingList.user_id == current_user.id
        ).all()
        shopping_lists_names = [shopping_list.name for shopping_list in shopping_lists]
        form.name.choices = shopping_lists_names

        return render_template(
            "recipe.html",
            PRODUCT_CATEGORIES=PRODUCT_CATEGORIES,
            RECIPE_CATEGORIES=RECIPE_CATEGORIES,
            recipe=recipe,
            form=form,
        )

    @app.route("/delete_recipe/<int:recipe_id>")
    @login_required
    def delete_recipe(recipe_id):
        try:
            recipe_to_delete = Recipe.query.get(recipe_id)
            db.session.delete(recipe_to_delete)
            db.session.commit()
            flash("Рецепт удалён.", category="success")
        except:
            flash("При удалении рецепта возникла ошибка.", category="danger")

        return redirect(url_for("my_recipes"))

    @app.route("/my-lists")
    @login_required
    def show_my_shopping_lists():
        session["redirect_url_after_renaming_shopping_list"] = url_for(
            "show_my_shopping_lists"
        )
        create_shopping_list_form = CreateListForm()
        rename_shopping_list_form = RenameElement()
        user = current_user
        user_shopping_lists = user.shopping_lists
        title = "Мои списки покупок"
        return render_template(
            "my_shopping_lists.html",
            create_shopping_list_form=create_shopping_list_form,
            rename_shopping_list_form=rename_shopping_list_form,
            user_shopping_lists=user_shopping_lists,
            page_title=title,
        )

    @app.route("/create-new-list", methods=["POST"])
    def create_new_shopping_list():
        form = CreateListForm()
        public_id = str(uuid4())
        user = current_user

        if form.validate_on_submit():
            new_shopping_list_name = form.name.data

            shopping_list_already_exists = ShoppingList.query.filter(
                ShoppingList.name == new_shopping_list_name,
                ShoppingList.user_id == current_user.id,
            ).one_or_none()

            if shopping_list_already_exists:
                flash("Список покупок с таким именем уже существует", category="danger")

            else:
                new_shopping_list = ShoppingList(
                    name=new_shopping_list_name, user_id=user.id, public_id=public_id
                )
                db.session.add(new_shopping_list)
                db.session.commit()
                flash("Новый список успешно создан", category="success")
                return redirect(url_for("show_shopping_list", public_id=public_id))

        else:
            flash_errors_from_form(form)

        return redirect(url_for("show_my_shopping_lists"))

    @app.route("/delete-shopping-list/<shopping_list_id>")
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

    @app.route("/rename-shopping-list", methods=["POST"])
    def rename_shopping_list():
        form = RenameElement()

        if form.validate_on_submit():
            new_name = form.new_value.data
            shopping_list_id = form.element_id.data
            shopping_list_to_rename = ShoppingList.query.filter(
                ShoppingList.id == shopping_list_id
            ).one_or_none()

            if shopping_list_to_rename:
                shopping_list_to_rename.name = new_name
                db.session.commit()
                flash("Список переименован", category="success")
            else:
                flash("При переименовании списка возникла ошибка", category="danger")

        else:
            flash_errors_from_form(form)

        redirect_url = session.get(
            "redirect_url_after_renaming_shopping_list",
            url_for("show_my_shopping_lists"),
        )
        return redirect(redirect_url)

    @app.route("/my-lists/<public_id>")
    def show_shopping_list(public_id):
        session["redirect_url_after_renaming_shopping_list"] = url_for(
            "show_shopping_list", public_id=public_id
        )

        add_shopping_item_form = AddShoppingItem()
        rename_shopping_list_form = RenameElement()
        edit_quantity_of_shopping_item_form = EditQuantityOfShoppingItemForm()

        shopping_list = ShoppingList.query.filter(
            ShoppingList.public_id == public_id
        ).one_or_none()

        if shopping_list:
            return render_template(
                "shopping_list.html",
                add_shopping_item_form=add_shopping_item_form,
                rename_shopping_list_form=rename_shopping_list_form,
                edit_quantity_of_shopping_item_form=edit_quantity_of_shopping_item_form,
                shopping_list=shopping_list,
            )

        flash("При показе списка возникла ошибка", category="danger")
        return redirect(url_for("show_my_shopping_lists"))

    @app.route("/add-item/<shopping_list_public_id>", methods=["POST"])
    def add_item_to_shopping_list(shopping_list_public_id):
        form = AddShoppingItem()

        if form.validate_on_submit():
            shopping_list = ShoppingList.query.filter(
                ShoppingList.public_id == shopping_list_public_id
            ).one_or_none()

            if shopping_list:
                if not form.name.data:
                    form.name.data = 0
                update_item_to_shopping_list(
                    shopping_list=shopping_list,
                    name=form.name.data,
                    quantity=form.quantity.data,
                    unit=form.unit.data,
                )
                flash("Новый продукт успешно добавлен", category="success")

            else:
                flash("При добавлении продукта возникла ошибка", category="danger")
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

    @app.route("/shopping-item-checkbox", methods=["POST"])
    def shopping_item_checkbox():
        item_id = request.form.get("item_id")

        item_to_check = ShoppingItem.query.filter(
            ShoppingItem.id == item_id
        ).one_or_none()

        if item_to_check:
            item_to_check.checked = int(request.form.get("state_of_checkbox"))
            db.session.commit()
            return "ok"
        else:
            return "failed"

    @app.route("/edit-quantity-of-shopping-item", methods=["POST"])
    def edit_quantity_of_shopping_item():
        form = EditQuantityOfShoppingItemForm()

        if form.validate_on_submit():
            new_quantity = form.new_value.data
            shopping_item_id = form.element_id.data
            shopping_item_to_edit_quantity = ShoppingItem.query.filter(
                ShoppingItem.id == shopping_item_id
            ).one_or_none()

            if shopping_item_to_edit_quantity:
                shopping_item_to_edit_quantity.quantity = new_quantity
                db.session.commit()
                flash("Количество изменено", category="success")
            else:
                flash("При изменении количества возникла ошибка", category="danger")

        else:
            flash_errors_from_form(form)

        redirect_url = session.get(
            "redirect_url_after_renaming_shopping_list",
            url_for("show_my_shopping_lists"),
        )
        return redirect(redirect_url)

    @app.route("/add_recipe_to_shopping_list/<int:recipe_id>", methods=["POST"])
    def add_recipe_to_shopping_list(recipe_id):
        form = ChooseListForm()

        shopping_lists = ShoppingList.query.filter(
            ShoppingList.user_id == current_user.id
        ).all()
        shopping_lists_names = [shopping_list.name for shopping_list in shopping_lists]
        form.name.choices = shopping_lists_names
        if form.validate_on_submit():
            chosen_shopping_list = ShoppingList.query.filter(
                ShoppingList.name == form.name.data,
                ShoppingList.user_id == current_user.id,
            ).one()
            recipe = Recipe.query.get(recipe_id)
            portions = form.portions.data
            update_recipe_to_shopping_list(
                shopping_list=chosen_shopping_list, recipe=recipe, portions=portions
            )
            flash(
                f"Ингредиенты рецепта добавлены в список {chosen_shopping_list.name}",
                category="success",
            )

        else:
            flash_errors_from_form(form)

        return redirect(
            url_for(
                "recipe",
                recipe_id=recipe.id,
            )
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
