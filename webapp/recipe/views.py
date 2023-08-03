from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from webapp.db import db, UNITS
from webapp.recipe.forms import AddRecipeForm
from webapp.recipe.models import (
    Ingredient,
    PRODUCT_CATEGORIES,
    Product,
    RECIPE_CATEGORIES,
    Recipe,
    RecipeDescription,
)
from webapp.shopping_list.forms import ChooseListForm
from webapp.shopping_list.models import ShoppingList
from webapp.utils import flash_errors_from_form, get_admin_id, object_does_not_exist
from uuid import uuid4

blueprint = Blueprint("recipe", __name__, url_prefix="/recipes")


@blueprint.route("/public")
def public_recipes():
    admin_id = get_admin_id()
    public_recipes = Recipe.query.filter(Recipe.user_id == admin_id).all()
    return render_template("recipe/public_recipes.html", public_recipes=public_recipes)


@blueprint.route("/my_recipes")
@login_required
def my_recipes():
    user_recipes = Recipe.query.filter(Recipe.user_id == current_user.id).all()
    return render_template("recipe/my_recipes.html", user_recipes=user_recipes)


@blueprint.route("/add_recipe", methods=["POST", "GET"])
@login_required
def add_recipe():
    form = AddRecipeForm()
    if request.method == "GET":
        return render_template("recipe/add_recipe.html", form=form)

    if form.validate_on_submit():
        name = form.name.data

        recipe_name_already_used = bool(
            Recipe.query.filter(
                Recipe.name == name, Recipe.user_id == current_user.id
            ).count()
        )
        if recipe_name_already_used:
            flash("Рецепт с таким именем уже существует", category="danger")
            return render_template("/recipe/add_recipe.html", form=form)

        category = form.category.data
        cooking_time = form.cooking_time.data

        recipe = Recipe(
            name=name,
            user_id=current_user.id,
            category=category,
            cooking_time=cooking_time,
        )
        db.session.add(recipe)
        db.session.commit()

        recipe = Recipe.query.filter(
            Recipe.name == recipe.name, Recipe.user_id == recipe.user_id
        ).one()

        return render_template(
            "recipe/add_ingredients&cooking_steps.html",
            recipe=recipe,
            PRODUCT_CATEGORIES=PRODUCT_CATEGORIES,
            RECIPE_CATEGORIES=RECIPE_CATEGORIES,
            UNITS=UNITS,
        )
    else:
        flash_errors_from_form(form)

    return redirect(url_for("recipe.my_recipes"))


@blueprint.route("/add_ingredient/<int:recipe_id>", methods=["POST"])
@login_required
def add_ingredient(recipe_id):
    recipe = Recipe.query.filter(Recipe.id == recipe_id).one_or_none()
    if not recipe:
        flash("При добавлении ингредиента произошла ошибка")
        return redirect(url_for("recipe.my_recipes"))

    product_name = request.form.get("product_name")
    product_category = request.form.get("product_category")
    ingredient_quantity = request.form.get("ingredient_quantity")
    ingredient_unit = request.form.get("ingredient_unit")

    if all([product_name, product_category, ingredient_quantity, ingredient_unit]):
        product = Product.query.filter(Product.name == product_name).one_or_none()

        if not product:
            product = Product(name=product_name, category=product_category)
            db.session.add(product)
            db.session.commit()
            product = Product.query.filter(Product.name == product_name).one()

        product_id = product.id

        quantity = ingredient_quantity

        ingredient = Ingredient(
            product_id=product_id,
            quantity=quantity,
            unit=ingredient_unit,
            recipe_id=recipe.id,
        )

        db.session.add(ingredient)
        db.session.commit()
        return "ok"

    else:
        return "failed"


@blueprint.route("/add_recipe_description/<int:recipe_id>", methods=["POST"])
def add_recipe_description(recipe_id):
    cooking_step_text = request.form.get("cooking_step_text")

    if cooking_step_text:
        cooking_step_obj = RecipeDescription(
            recipe_id=recipe_id, text=cooking_step_text
        )
        db.session.add(cooking_step_obj)
        db.session.commit()
        return "ok"

    else:
        return "failed"


@blueprint.route("/<int:recipe_id>")
def recipe(recipe_id):
    form = ChooseListForm()
    recipe = Recipe.query.filter(Recipe.id == recipe_id).one_or_none()

    if not recipe:
        return redirect(url_for("recipe.public_recipes"))

    admin_id = get_admin_id()

    current_user_id = None
    if current_user.is_authenticated:
        current_user_id = current_user.id

    if recipe.user_id != admin_id and recipe.user_id != current_user_id:
        flash("Этот рецепт Вам недоступен")
        return redirect(url_for("recipe.public_recipes"))

    elif current_user.is_authenticated:
        if not current_user.shopping_lists:
            new_shopping_list = ShoppingList(
                name="Мой список покупок",
                user_id=current_user.id,
                public_id=str(uuid4()),
            )
            db.session.add(new_shopping_list)
            db.session.commit()
        form.name.choices = [
            shopping_list.name for shopping_list in current_user.shopping_lists
        ]

    return render_template(
        "/recipe/recipe.html",
        PRODUCT_CATEGORIES=PRODUCT_CATEGORIES,
        RECIPE_CATEGORIES=RECIPE_CATEGORIES,
        recipe=recipe,
        form=form,
    )


@blueprint.route("/delete_recipe/<int:recipe_id>")
@login_required
def delete_recipe(recipe_id):
    recipe_to_delete = Recipe.query.filter(Recipe.id == recipe_id).one_or_none()

    if recipe_to_delete:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        flash("Рецепт удалён.", category="success")

    return redirect(url_for("recipe.my_recipes"))


@blueprint.route("/copy_to_my_recipes/<int:recipe_id>")
@login_required
def copy_to_my_recipes(recipe_id):
    admin_id = get_admin_id()
    recipe = Recipe.query.filter(
        Recipe.id == recipe_id, Recipe.user_id == admin_id
    ).one_or_none()

    if recipe:
        if object_does_not_exist(Recipe, recipe.name):
            recipe_obj = Recipe(
                name=recipe.name,
                user_id=current_user.id,
                category=recipe.category,
                cooking_time=recipe.cooking_time,
            )
            db.session.add(recipe_obj)
            recipe_copy = Recipe.query.filter(
                Recipe.name == recipe.name, Recipe.user_id == current_user.id
            ).one()

            for ingredient in recipe.ingredients:
                ingredient_copy = Ingredient(
                    product_id=ingredient.product_id,
                    quantity=ingredient.quantity,
                    unit=ingredient.unit,
                    recipe_id=recipe_copy.id,
                )
                db.session.add(ingredient_copy)

            for step in recipe.description:
                step_copy = RecipeDescription(recipe_id=recipe_copy.id, text=step.text)
                db.session.add(step_copy)
            db.session.commit()

            flash("Рецепт успешно добавлен в Ваши рецепты", category="success")
            return redirect(url_for("recipe.recipe", recipe_id=recipe_copy.id))
    else:
        flash("Что-то пошло не так")

    return redirect(url_for("recipe.public_recipes"))
