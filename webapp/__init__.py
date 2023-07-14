from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from webapp.forms import (
    AddIngredientForm,
    AddRecipeForm,
    AddShoppingItem,
    CreateListForm,
    EditQuantityOfShoppingItemForm,
    LoginForm,
    RegistrationForm,
    RenameElement,
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
import os


basedir = os.path.abspath(os.path.dirname(__file__))
database_uri = "sqlite:///" + os.path.join(basedir, "..", "webapp.db")


def flash_errors_from_form(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                'Ошибка в поле "{}": {}'.format(getattr(form, field).label.text, error),
                category="danger",
            )


def create_app(database_uri=database_uri):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
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
            return redirect(url_for("my_recipes"))

        to_view = {}
        to_view["name"] = recipe.name
        to_view["category"] = recipe.category
        to_view["description"] = recipe.description
        to_view["cooking_time"] = recipe.cooking_time
        to_view["preparation_time"] = recipe.preparation_time
        to_view["recipe_color"] = RECIPE_CATEGORIES[recipe.category].lower()

        ingredients = Ingredient.query.filter(Ingredient.recipe_id == recipe_id).all()
        to_view["ingredients"] = []
        for ingredient in ingredients:
            category = Product.query.get(ingredient.product_id).category
            color = PRODUCT_CATEGORIES[category].lower()
            to_view["ingredients"].append((str(ingredient), color))

        if request.method == "GET":
            recipe_name = db.session.query(Recipe).get(recipe_id).name
            ingredients = (
                db.session.query(Ingredient)
                .filter(Ingredient.recipe_id == recipe_id)
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
                to_view=to_view,
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
                    to_view=to_view,
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

    @app.route("/recipe/<int:recipe_id>")
    @login_required
    def recipe(recipe_id):
        try:
            recipe = db.session.query(Recipe).get(recipe_id)
        except:
            return redirect(url_for("recipes"))
        to_view = {}
        to_view["name"] = recipe.name
        to_view["category"] = recipe.category
        to_view["description"] = recipe.description
        to_view["cooking_time"] = recipe.cooking_time
        to_view["preparation_time"] = recipe.preparation_time
        to_view["recipe_color"] = RECIPE_CATEGORIES[recipe.category].lower()

        ingredients = Ingredient.query.filter(Ingredient.recipe_id == recipe_id).all()
        to_view["ingredients"] = []
        for ingredient in ingredients:
            category = Product.query.get(ingredient.product_id).category
            color = PRODUCT_CATEGORIES[category].lower()
            to_view["ingredients"].append((str(ingredient), color))
        return render_template(
            "recipe.html",
            to_view=to_view,
        )

    @app.route("/delete_recipe/<int:recipe_id>")
    @login_required
    def delete_recipe(recipe_id):
        return redirect(url_for("recipe", recipe_id=recipe_id))

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
                shopping_list_id = shopping_list.id
                new_item = ShoppingItem(
                    name=form.name.data,
                    quantity=form.quantity.data,
                    shopping_list_id=shopping_list_id,
                )
                db.session.add(new_item)
                db.session.commit()
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

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
