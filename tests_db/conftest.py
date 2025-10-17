from datetime import datetime

import pytest
from werkzeug.security import generate_password_hash

# imports from SQLAlchemy
import recipe.adapters.repository as repo
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from recipe.adapters.database_repository import SqlAlchemyRepository
from recipe.adapters import database_repository, populate_repository
from recipe.adapters.orm import map_model_to_tables, mapper_registry
from utils import get_project_root

from recipe.domainmodel.recipe import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.recipe import RecipeImage
from recipe.domainmodel.recipe import RecipeIngredient
from recipe.domainmodel.recipe import RecipeInstruction
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User


TEST_DATA_PATH_DATABASE_FULL = get_project_root() / "recipe" / "adapters" / "data"
TEST_DATA_PATH_DATABASE_LIMITED = get_project_root() / "tests" / "data"

# Database URIs
TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///recipe-test.db'

@pytest.fixture
def database_engine():
    database_engine = create_engine(TEST_DATABASE_URI_FILE, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                    echo=False)

    # Set up session factory and repo instance
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
    repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

    print("REPOPULATING DATABASE...")
    clear_mappers()
    mapper_registry.metadata.create_all(database_engine)  # Create tables
    for table in reversed(mapper_registry.metadata.sorted_tables): # Clear any pre-existing data
        with database_engine.connect() as conn:
            conn.execute(table.delete())

    map_model_to_tables()
    # Populate repository with limited test data
    database_mode = True
    populate_repository.populate(TEST_DATA_PATH_DATABASE_LIMITED, repo.repo_instance, True)
    print("REPOPULATING DATABASE... FINISHED")

    yield database_engine  # Yield the database engine for use in tests
    mapper_registry.metadata.drop_all(database_engine)


@pytest.fixture
def session_factory():
    clear_mappers()
    database_engine = create_engine(TEST_DATABASE_URI_FILE, connect_args={"check_same_thread": False},
                                    poolclass=NullPool, echo=False)

    # Create tables
    mapper_registry.metadata.create_all(database_engine)

    # Clear existing data
    for table in reversed(mapper_registry.metadata.sorted_tables):
        with database_engine.connect() as conn:
            conn.execute(table.delete())

    map_model_to_tables()

    # Create session factory
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

    # Populate repository with test data
    repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    populate_repository.populate(TEST_DATA_PATH_DATABASE_LIMITED, repo.repo_instance, True)

    yield session_factory  # Yield the session factory for use in tests

    # Drop tables after test
    mapper_registry.metadata.drop_all(database_engine)

@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    mapper_registry.metadata.create_all(engine)
    for table in reversed(mapper_registry.metadata.sorted_tables):  # Remove any data from the tables.
        with engine.connect() as conn:
            conn.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    mapper_registry.metadata.drop_all(engine)

@pytest.fixture
def my_author():
    return Author(1533, "Dancer")

@pytest.fixture
def my_category():
    return Category(1, "Frozen Desserts")

@pytest.fixture
def my_favourite(my_user, my_recipe):
    return Favourite(1, my_user.id, my_recipe.id, datetime(2024, 1, 1))

@pytest.fixture
def my_nutrition():
    return Nutrition(1, 170.9,2.5,1.3,8,29.8,
                     37.1, 3.6, 30.2, 3.2)

@pytest.fixture
def my_recipe(my_author, my_category, my_nutrition, my_recipe_images, my_recipe_ingredients, my_recipe_instructions):
    return Recipe(38, "Low-Fat Berry Blue Frozen Dessert", my_author, 1440,
                  45, 1485, datetime(2009, 8, 9),
                  "Make and share this Low-Fat Berry Blue Frozen Dessert recipe from Food.com.",
                  my_recipe_images, my_category, my_recipe_ingredients, my_nutrition, 4, "NA",
                  my_recipe_instructions)

@pytest.fixture
def my_recipe_image():
    return RecipeImage(38,'https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/38/YUeirxMLQaeE1h3v3qnM_229%20berry%20blue%20frzn%20dess.jpg',
                1)

@pytest.fixture
def my_recipe_ingredient():
    return RecipeIngredient(38, "4", "blueberries", 1)

@pytest.fixture
def my_recipe_instruction():
    return RecipeInstruction(38, 'Toss 2 cups berries with sugar.',
                             1)

@pytest.fixture
def my_recipe_images():
    return [RecipeImage(38, 'https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/38/YUeirxMLQaeE1h3v3qnM_229%20berry%20blue%20frzn%20dess.jpg',
                               1)]

@pytest.fixture
def my_recipe_ingredients():
    quantities = ['4', '1/4', '1', '1']
    parts      = ['blueberries', 'granulated sugar', 'vanilla yogurt', 'lemon juice']
    return [
        RecipeIngredient(38, q.strip(), p.strip(), idx)
        for idx, (q, p) in enumerate(zip(quantities, parts), start=1)
    ]

@pytest.fixture
def my_recipe_instructions():
    steps = [
        'Toss 2 cups berries with sugar.',
        'Let stand for 45 minutes, stirring occasionally.',
        'Transfer berry-sugar mixture to food processor.',
        'Add yogurt and process until smooth.',
        "Strain through fine sieve. Pour into baking pan (or transfer to ice cream maker and process according to manufacturers' directions). Freeze uncovered until edges are solid but centre is soft.  Transfer to processor and blend until smooth again.",
        'Return to pan and freeze until edges are solid.',
        'Transfer to processor and blend until smooth again.',
        'Fold in remaining 2 cups of blueberries.',
        'Pour into plastic mold and freeze overnight. Let soften slightly to serve.'
    ]
    return [
        RecipeInstruction(38, step.strip(), idx)
        for idx, step in enumerate(steps, start=1)
    ]

@pytest.fixture
def my_user():
    return User(1, "tests user", generate_password_hash("password123"))


@pytest.fixture
def my_review(my_user, my_recipe):
    return Review(1, my_user.id, datetime(2024, 1, 1), my_recipe.id, 5, "Food is good")