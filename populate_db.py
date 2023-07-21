from data.recipes import recipes


def populate_db(
    app,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    db,
    Ingredient,
    Product,
    ProjectSettings,
    User,
    Recipe,
):
    db_populated = ProjectSettings.query.filter(
        ProjectSettings.name == "db_populated"
    ).one_or_none()

    if not db_populated:
        with app.app_context():
            admin = User(name="admin", email=ADMIN_EMAIL)
            admin.set_password(ADMIN_PASSWORD)
            db.session.add(admin)
            db.session.commit()
            admin_obj = User.query.filter(User.email == ADMIN_EMAIL).one_or_none()

            if not admin_obj:
                print(f"Отсутствует пользователь с почтой {ADMIN_EMAIL}")
                exit()

            admin_id = admin_obj.id

            for recipe in recipes:
                recipe_obj = Recipe(
                    user_id=admin_id,
                    name=recipe["name"],
                    category=recipe["category"],
                    description=recipe["description"],
                    preparation_time=recipe["preparation_time"],
                    cooking_time=recipe["cooking_time"],
                )
                db.session.add(recipe_obj)
                db.session.commit()

                recipe_id = (
                    Recipe.query.filter(
                        Recipe.user_id == admin_id, Recipe.name == recipe["name"]
                    )
                    .one()
                    .id
                )

                for ingredient in recipe["ingredients"]:
                    product_obj = Product.query.filter(
                        Product.name == ingredient["product"]["name"]
                    ).one_or_none()

                    if not product_obj:
                        product_obj = Product(
                            name=ingredient["product"]["name"],
                            category=ingredient["product"]["category"],
                        )
                        db.session.add(product_obj)
                        db.session.commit()

                        product_obj = Product.query.filter(
                            Product.name == ingredient["product"]["name"]
                        ).one()

                    product_id = product_obj.id
                    ingredient_obj = Ingredient(
                        product_id=product_id,
                        quantity=ingredient["quantity"],
                        unit=ingredient["unit"],
                        recipe_id=recipe_id,
                    )
                    db.session.add(ingredient_obj)

            db_populated = ProjectSettings(name="db_populated", value="True")
            db.session.add(db_populated)
            db.session.commit()

        return True
