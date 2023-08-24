from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from webapp.forms import RenameElement
from webapp.db import db
from webapp.recipe.models import Recipe
from webapp.shopping_list.forms import (
    AddShoppingItem,
    ChooseListForm,
    CreateListForm,
    EditQuantityOfShoppingItemForm,
)
from webapp.shopping_list.models import ShoppingItem, ShoppingList
from webapp.utils import (
    flash_errors_from_form,
    object_does_not_exist,
    update_item_to_shopping_list,
    update_recipe_to_shopping_list,
)
from uuid import uuid4
import json

blueprint = Blueprint("shopping_list", __name__, url_prefix="/shopping_lists")


@blueprint.route("/my-lists")
@login_required
def show_my_shopping_lists():
    session["redirect_url_after_renaming_shopping_list"] = url_for(
        "shopping_list.show_my_shopping_lists"
    )
    create_shopping_list_form = CreateListForm()
    rename_shopping_list_form = RenameElement()
    user = current_user
    user_shopping_lists = user.shopping_lists
    title = "Мои списки покупок"
    return render_template(
        "shopping_list/my_shopping_lists.html",
        create_shopping_list_form=create_shopping_list_form,
        rename_shopping_list_form=rename_shopping_list_form,
        user_shopping_lists=user_shopping_lists,
        page_title=title,
    )


@blueprint.route("/create-new-list", methods=["POST"])
def create_new_shopping_list():
    form = CreateListForm()
    public_id = str(uuid4())
    user = current_user

    if form.validate_on_submit():
        new_shopping_list_name = form.name.data.lower()

        if object_does_not_exist(ShoppingList, new_shopping_list_name):
            new_shopping_list = ShoppingList(
                name=new_shopping_list_name, user_id=user.id, public_id=public_id
            )
            db.session.add(new_shopping_list)
            db.session.commit()
            flash("Новый список успешно создан", category="success")
            return redirect(
                url_for("shopping_list.show_shopping_list", public_id=public_id)
            )

    else:
        flash_errors_from_form(form)

    return redirect(url_for("shopping_list.show_my_shopping_lists"))


@blueprint.route("/delete-shopping-list/<shopping_list_id>")
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

    return redirect(url_for("shopping_list.show_my_shopping_lists"))


@blueprint.route("/rename-shopping-list", methods=["POST"])
def rename_shopping_list():
    form = RenameElement()

    if form.validate_on_submit():
        new_name = form.new_value.data.lower()

        if object_does_not_exist(ShoppingList, new_name):
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
        url_for("shopping_list.show_my_shopping_lists"),
    )
    return redirect(redirect_url)


@blueprint.route("/my-lists/<public_id>")
def show_shopping_list(public_id):
    session["redirect_url_after_renaming_shopping_list"] = url_for(
        "shopping_list.show_shopping_list", public_id=public_id
    )

    add_shopping_item_form = AddShoppingItem()
    rename_shopping_list_form = RenameElement()
    edit_quantity_of_shopping_item_form = EditQuantityOfShoppingItemForm()

    shopping_list = ShoppingList.query.filter(
        ShoppingList.public_id == public_id
    ).one_or_none()

    if shopping_list:
        return render_template(
            "shopping_list/shopping_list.html",
            add_shopping_item_form=add_shopping_item_form,
            rename_shopping_list_form=rename_shopping_list_form,
            edit_quantity_of_shopping_item_form=edit_quantity_of_shopping_item_form,
            shopping_list=shopping_list,
        )

    flash("При показе списка возникла ошибка", category="danger")
    return redirect(url_for("shopping_list.show_my_shopping_lists"))


@blueprint.route("/add-item/<shopping_list_public_id>", methods=["POST"])
def add_item_to_shopping_list(shopping_list_public_id):
    form = AddShoppingItem()

    if form.validate_on_submit():
        shopping_list = ShoppingList.query.filter(
            ShoppingList.public_id == shopping_list_public_id
        ).one_or_none()

        if shopping_list:
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
        url_for("shopping_list.show_shopping_list", public_id=shopping_list_public_id)
    )


@blueprint.route("/delete-item/<shopping_list_public_id>/<item_id>")
def delete_item_from_shopping_list(shopping_list_public_id, item_id):
    item_to_delete = ShoppingItem.query.filter(ShoppingItem.id == item_id).one_or_none()

    if item_to_delete:
        db.session.delete(item_to_delete)
        db.session.commit()
        flash("Продукт удалён", category="success")
    else:
        flash("При удалении продукта возникла ошибка", category="danger")

    return redirect(
        url_for("shopping_list.show_shopping_list", public_id=shopping_list_public_id)
    )


@blueprint.route("/shopping-item-checkbox", methods=["POST"])
def shopping_item_checkbox():
    item_id = request.form.get("item_id")

    item_to_check = ShoppingItem.query.filter(ShoppingItem.id == item_id).one_or_none()

    if item_to_check:
        item_to_check.checked = int(request.form.get("state_of_checkbox"))
        db.session.commit()
        return "ok"
    else:
        return "failed"


@blueprint.route("/edit-quantity-of-shopping-item", methods=["POST"])
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
        url_for("shopping_list.show_my_shopping_lists"),
    )
    return redirect(redirect_url)


@blueprint.route("/add_recipe_to_shopping_list", methods=["POST"])
def add_recipe_to_shopping_list():
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
        recipe_info = json.loads(
            form.recipe_info.data.replace('"', '\\"').replace("'", '"')
        )
        recipe_id = recipe_info["id"]
        recipe = Recipe.query.get(recipe_id)
        portions = form.portions.data
        update_recipe_to_shopping_list(
            shopping_list=chosen_shopping_list, recipe=recipe, portions=portions
        )
        flash(
            f"Ингредиенты рецепта добавлены в список {chosen_shopping_list.name}",
            category="success",
        )
        return redirect(
            url_for(
                "recipe.recipe",
                recipe_id=recipe_id,
            )
        )

    else:
        flash_errors_from_form(form)
        return "failed"


@blueprint.route(
    "/choose_recipe_to_add/<shopping_list_public_id>", methods=["GET", "POST"]
)
def choose_recipe_to_add(shopping_list_public_id):
    user_recipes = Recipe.query.filter(Recipe.user_id == current_user.id).all()

    recipe_id = request.form.get("recipe_id")
    portions = request.form.get("portions")

    if recipe_id and portions:
        portions = int(portions)
        chosen_shopping_list = ShoppingList.query.filter(
            ShoppingList.public_id == shopping_list_public_id
        ).one()
        recipe = Recipe.query.get(recipe_id)
        update_recipe_to_shopping_list(
            shopping_list=chosen_shopping_list, recipe=recipe, portions=portions
        )

    return render_template(
        "shopping_list/choose_recipe_to_add.html",
        user_recipes=user_recipes,
        shopping_list_public_id=shopping_list_public_id,
    )
