from pathlib import Path
from flask import Flask

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from recipe.domainmodel.recipe import Recipe
from recipe.browse import browse

# local imports
import recipe.adapters.repository as repo
from recipe.adapters.database_repository import SqlAlchemyRepository
from recipe.adapters.populate_repository import populate
from recipe.adapters.orm import mapper_registry, map_model_to_tables

# TODO add memory repository

def create_app(test_config = None):
    app = Flask(__name__)

    database_uri = 'sqlite:///recipes.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_ECHO'] = True  # echo SQL statements - useful for debugging

    database_engine = create_engine(database_uri, connect_args={"check_same_thread": False},
                                    poolclass=NullPool,
                                    echo=False)

    app.config.from_object('config.Config')
    data_path = Path('recipe') / 'adapters' / 'data'

    # STEP 3: Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True,
                                   bind=database_engine)

    # STEP 4: Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo.repo_instance = SqlAlchemyRepository(session_factory)
    data_path = Path('recipe') / 'adapters' / 'data'
    testing = test_config is not None

    # STEP 4: Repopulate the DB.
    if len(inspect(database_engine).get_table_names()) == 0:
        print("REPOPULATING DATABASE...")
        # For testing, or first-time use of the web application, reinitialise the database.
        clear_mappers()
        # Conditionally create database tables.
        mapper_registry.metadata.create_all(database_engine)
        # Remove any data from the tables.
        for table in reversed(mapper_registry.metadata.sorted_tables):
            with database_engine.connect() as conn:
                conn.execute(table.delete())

        # Generate mappings that map domain model classes to the database tables.
        map_model_to_tables()

        populate(data_path, repo.repo_instance, testing=testing)
        print("REPOPULATING DATABASE... FINISHED")

    else:
        # Solely generate mappings that map domain model classes to the database tables.
        map_model_to_tables()

    # if test_config is not None:
    #     app.config.from_mapping(test_config)
    #     data_path = app.config['TEST_DATA_PATH']

    # repo.repo_instance = MemoryRepository()
    # populate(data_path, repo.repo_instance)

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
