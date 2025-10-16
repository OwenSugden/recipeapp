from pathlib import Path
from flask import Flask

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from recipe.adapters.memory_repository import MemoryRepository
from recipe.domainmodel.recipe import Recipe
from recipe.browse import browse

# local imports
import recipe.adapters.repository as repo
from recipe.adapters.database_repository import SqlAlchemyRepository
from recipe.adapters.populate_repository import populate
from recipe.adapters.orm import mapper_registry, map_model_to_tables

def create_app(test_config = None):
    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('recipe') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        #color
        print("\x1b[42m", f"Running in: {app.config['REPOSITORY'].upper()}", "\x1b[0m")

        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = MemoryRepository()
        database_mode = False
        # fill the content of the repository from the provided csv files, false because its not debuging
        populate(data_path, repo.repo_instance, False)

    elif app.config['REPOSITORY'] == 'database':
        #color
        print("\x1b[45m", f"Running in: {app.config['REPOSITORY'].upper()}", "\x1b[0m")

        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']

        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool, echo=database_echo)

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(inspect(database_engine).get_table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            mapper_registry.metadata.create_all(database_engine)
            for table in reversed(mapper_registry.metadata.sorted_tables):
                with database_engine.connect() as conn:
                    conn.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = True
            populate(data_path, repo.repo_instance, False)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)
        
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)
        
        from .recipe_detail import recipe_detail
        app.register_blueprint(recipe_detail.recipe_detail_blueprint)
        
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)
        
        from .user_profile import user_profile
        app.register_blueprint(user_profile.user_profile_blueprint)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, SqlAlchemyRepository):
                repo.repo_instance.close_session()


    return app
