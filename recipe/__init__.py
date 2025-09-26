from datetime import datetime
from flask import Flask, render_template
import recipe.adapters.repository as repo
from recipe.adapters.memory_repository import populate
from recipe.adapters.memory_repository import MemoryRepository
from pathlib import Path

from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author


def create_app(test_config = None):
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('recipes') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)
        from .recipe_detail import recipe_detail
        app.register_blueprint(recipe_detail.recipe_detail_blueprint)
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)
        from .search import search
        app.register_blueprint(search.search_blueprint)
        from .user_profile import user_profile
        app.register_blueprint(user_profile.user_profile_blueprint)

    repo.repo_instance = MemoryRepository()

    populate(repo.repo_instance)
    return app
