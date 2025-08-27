"""Initialize Flask app."""
from datetime import datetime
from flask import Flask, render_template
import recipe.adapters.repository as repo
from recipe.adapters.memory_repository import populate
from recipe.adapters.memory_repository import MemoryRepository

# TODO: Access to the recipe should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!

from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author


def create_app():
    app = Flask(__name__)

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)
        from .recipe_detail import recipe_detail
        app.register_blueprint(recipe_detail.recipe_detail_blueprint)

    repo.repo_instance = MemoryRepository()

    populate(repo.repo_instance)
    return app
