from data.recipes import recipes


def populate_db(
    app,
    admin_email,
    admin_password,
    db,
    models,
):
    ingredient_model, product_model, projectsettings_model, user_model, recipe_model = (
        models["Ingredient"],
        models["Product"],
        models["ProjectSettings"],
        models["User"],
        models["Recipe"],
    )

    db_populated = projectsettings_model.query.filter(
        projectsettings_model.name == "db_populated"
    ).one_or_none()

    if not db_populated:
        with app.app_context():
            db.create_all()

            admin = user_model(name="admin", email=admin_email)
            admin.set_password(admin_password)
            db.session.add(admin)
            admin_obj = user_model.query.filter(
                user_model.email == admin_email
            ).one_or_none()

            if not admin_obj:
                print(f"Отсутствует пользователь с почтой {admin_email}")
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

                recipe_id = (
                    recipe_model.query.filter(
                        recipe_model.user_id == admin_id,
                        recipe_model.name == recipe["name"],
                    )
                    .one()
                    .id
                )

                for ingredient in recipe["ingredients"]:
                    product_obj = product_model.query.filter(
                        product_model.name == ingredient["product"]["name"]
                    ).one_or_none()

                    if not product_obj:
                        product_obj = product_model(
                            name=ingredient["product"]["name"],
                            category=ingredient["product"]["category"],
                        )
                        db.session.add(product_obj)

                        product_obj = product_model.query.filter(
                            product_model.name == ingredient["product"]["name"]
                        ).one()

                    product_id = product_obj.id
                    ingredient_obj = ingredient_model(
                        product_id=product_id,
                        quantity=ingredient["quantity"],
                        unit=ingredient["unit"],
                        recipe_id=recipe_id,
                    )
                    db.session.add(ingredient_obj)

            db_populated = projectsettings_model(name="db_populated", value="True")
            db.session.add(db_populated)
            db.session.commit()

        return True
