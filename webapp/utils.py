from flask import flash
from webapp.db import db
from webapp.shopping_list.models import ShoppingItem


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


def flash_errors_from_form(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                'Ошибка в поле "{}": {}'.format(getattr(form, field).label.text, error),
                category="danger",
            )
