from flask import Flask
from pathlib import Path
import recipe.adapters.repository as repo
from recipe.adapters.memory_repository import MemoryRepository, populate

def create_app(test_config = None):
    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('recipe') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)
        from .recipe_detail import recipe_detail
        app.register_blueprint(recipe_detail.recipe_detail_blueprint)
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    return app
