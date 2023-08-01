from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from webapp.db import db
from webapp.recipe.forms import AddIngredientForm, AddRecipeForm
from webapp.recipe.models import (
    Ingredient,
    PRODUCT_CATEGORIES,
    Product,
    RECIPE_CATEGORIES,
    Recipe,
)
from webapp.shopping_list.forms import ChooseListForm
from webapp.shopping_list.models import ShoppingList
from webapp.user.models import User
from webapp.utils import flash_errors_from_form
from uuid import uuid4

blueprint = Blueprint("recipe", __name__, url_prefix="/recipe")


@blueprint.route("/recipe")
def recipes():
    admin = User.query.filter(User.name == "admin").one_or_none()
    if admin:
        public_recipes = Recipe.query.filter(Recipe.user_id == admin.id).all()
        return render_template("public_recipes.html", public_recipes=public_recipes)
    else:
        flash("Нет общедоступных рецептов!", category="danger")
        return redirect(url_for("index"))


@blueprint.route("/my_recipes")
@login_required
def my_recipes():
    user_recipes = Recipe.query.filter(Recipe.user_id == current_user.id).all()
    return render_template("recipe/my_recipes.html", user_recipes=user_recipes)


@blueprint.route("/add_recipe", methods=["POST", "GET"])
@login_required
def add_recipe():
    if request.method == "GET":
        form = AddRecipeForm()
        return render_template("recipe/add_recipe.html", form=form)

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
            return render_template("recipe/add_recipe.html", form=form)

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
                "recipe.add_ingredient",
                recipe_id=recipe_id,
                RECIPE_CATEGORIES=RECIPE_CATEGORIES,
                PRODUCT_CATEGORIES=PRODUCT_CATEGORIES,
            )
        )
    else:
        flash_errors_from_form(form)
    return redirect(url_for("recipe.recipe", recipe_id=recipe_id))


@blueprint.route("/add_ingredient/<int:recipe_id>", methods=["POST", "GET"])
@login_required
def add_ingredient(recipe_id):
    print(Recipe.query.all())
    try:
        recipe = db.session.query(Recipe).get(recipe_id)
    except:
        flash("Неверный идентификатор рецепта")
        return redirect(url_for("recipe.my_recipes"))

    if request.method == "GET":
        form = AddIngredientForm()
        return render_template(
            "recipe/add_ingredient.html",
            form=form,
            recipe=recipe,
            PRODUCT_CATEGORIES=PRODUCT_CATEGORIES,
            RECIPE_CATEGORIES=RECIPE_CATEGORIES,
        )

    form = AddIngredientForm()
    if form.validate_on_submit():
        unit = form.unit.data

        product = Product.query.filter(Product.name == form.product.data).one_or_none()
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
                "recipe.add_ingredient",
                recipe_id=recipe.id,
            )
        )
    else:
        flash_errors_from_form(form)
    return redirect(
        url_for(
            "recipe.add_ingredient",
            recipe_id=recipe.id,
        )
    )


@blueprint.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    try:
        recipe = db.session.query(Recipe).get(recipe_id)
    except:
        return redirect(url_for("recipe.recipe"))

    admin = User.query.filter(User.name == "admin").one_or_none()

    if admin:
        admin_id = admin.id
    else:
        admin_id = None

    if current_user.is_anonymous:
        if recipe.user_id != admin_id:
            flash("Рецепт доступен только авторизированным пользователям!")
            return redirect(url_for("recipe.recipe"))
    else:
        if recipe.user_id != admin_id and recipe.user_id != current_user.id:
            flash("У Вас нет прав на доступ к этому рецепту!")
            return redirect(url_for("recipe.recipe"))
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
        "recipe/recipe.html",
        PRODUCT_CATEGORIES=PRODUCT_CATEGORIES,
        RECIPE_CATEGORIES=RECIPE_CATEGORIES,
        recipe=recipe,
        form=form,
    )


@blueprint.route("/delete_recipe/<int:recipe_id>")
@login_required
def delete_recipe(recipe_id):
    try:
        recipe_to_delete = Recipe.query.get(recipe_id)
        db.session.delete(recipe_to_delete)
        db.session.commit()
        flash("Рецепт удалён.", category="success")
    except:
        flash("При удалении рецепта возникла ошибка.", category="danger")

    return redirect(url_for("recipe.my_recipes"))
