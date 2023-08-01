import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, redirect, render_template, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from populate_db import populate_db
from webapp.shopping_list.models import ShoppingList
from webapp.db import db
from webapp.user.models import User
from webapp.recipe.views import blueprint as recipe_blueprint
from webapp.user.views import blueprint as user_blueprint
from webapp.shopping_list.views import blueprint as shopping_list_blueprint

database_uri = os.environ.get("DATABASE_URL")
secret_key = os.environ.get("FLASK_SECRET_KEY")


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
    login_manager.login_view = "user.login"
    app.register_blueprint(user_blueprint)
    app.register_blueprint(recipe_blueprint)
    app.register_blueprint(shopping_list_blueprint)

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
                    url_for(
                        "shopping_list.show_shopping_list",
                        public_id=shopping_list_public_id,
                    )
                )
            else:
                return redirect(url_for("shopping_list.show_my_shopping_lists"))

        return render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
