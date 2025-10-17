from sqlalchemy import select, inspect
from datetime import datetime
from tests_db.conftest import *

from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe import RecipeIngredient
from recipe.domainmodel.recipe import RecipeInstruction
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User

# Test inspecting table names after population
def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert (inspector.get_table_names() ==
            ['authors', 'categories', 'favourites', 'nutrition',
             'recipe_images', 'recipe_ingredients', 'recipe_instructions', 'recipes', 'reviews', 'users'])

# Test selecting all authors after population
def test_database_populate_select_all_authors(database_engine):
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]
    authors_table = mapper_registry.metadata.tables.get(name_of_authors_table)

    if authors_table is None:
        raise KeyError(f"Table '{name_of_authors_table}' not found in metadata.")

    with database_engine.connect() as connection:
        select_statement = select(authors_table)
        result = connection.execute(select_statement)
        authors = result.fetchall()

        assert authors is not None
        assert len(authors) > 0
        print(authors)

# Test selecting all categories after population
def test_database_populate_select_all_categories(database_engine):
    inspector = inspect(database_engine)
    name_of_categories_table = inspector.get_table_names()[1]
    categories_table = mapper_registry.metadata.tables.get(name_of_categories_table)

    if categories_table is None:
        raise KeyError(f"Table '{name_of_categories_table}' not found in metadata.")

    with database_engine.connect() as connection:
        select_statement = select(categories_table)
        result = connection.execute(select_statement)
        categories = result.fetchall()

        assert categories is not None
        assert len(categories) > 0
        print(categories)

# Test selecting all favourites after population
def test_database_populate_select_all_favourites(database_engine):
    inspector = inspect(database_engine)
    name_of_favourites_table = inspector.get_table_names()[2]
    favourites_table = mapper_registry.metadata.tables.get(name_of_favourites_table)

    if favourites_table is None:
        raise KeyError(f"Table '{name_of_favourites_table}' not found in metadata.")

    new_favourite = {
        'id': 1,
        'user_id': 1,
        'recipe_id': 1,
        'date_added': datetime.now()
    }

    with database_engine.connect() as connection:
        connection.execute(favourites_table.insert().values(new_favourite))

        select_statement = select(favourites_table)
        result = connection.execute(select_statement)
        favourites = result.fetchall()

        favourites_dict = {
            'id': favourites[0][0],
            'user_id': favourites[0][1],
            'recipe_id': favourites[0][2],
            'date_added': favourites[0][3]
        }

        assert favourites is not None
        assert len(favourites) == 1
        assert favourites_dict == new_favourite

# Test selecting all nutrition after population
def test_database_populate_select_all_nutrition(database_engine):
    inspector = inspect(database_engine)
    name_of_nutrition_table = inspector.get_table_names()[3]
    nutrition_table = mapper_registry.metadata.tables.get(name_of_nutrition_table)

    if nutrition_table is None:
        raise KeyError(f"Table '{name_of_nutrition_table}' not found in metadata.")

    with database_engine.connect() as connection:
        select_statement = select(nutrition_table)
        result = connection.execute(select_statement)
        nutritions = result.fetchall()

        assert nutritions is not None
        assert len(nutritions) > 0
        print(nutritions)


# Test selecting all recipe images after population
def test_database_populate_select_all_recipe_images(database_engine):
    inspector = inspect(database_engine)
    name_of_recipe_images_table = inspector.get_table_names()[4]
    recipe_images_table = mapper_registry.metadata.tables.get(name_of_recipe_images_table)

    if recipe_images_table is None:
        raise KeyError(f"Table '{name_of_recipe_images_table}' not found in metadata.")

    with database_engine.connect() as connection:
        select_statement = select(recipe_images_table)
        result = connection.execute(select_statement)
        recipe_images = result.fetchall()

        assert recipe_images is not None
        assert len(recipe_images) > 0
        print(recipe_images)


# Test selecting all recipe ingredients after population
def test_database_populate_select_all_recipe_ingredients(database_engine):
    inspector = inspect(database_engine)
    name_of_recipe_ingredients_table = inspector.get_table_names()[5]
    recipe_ingredients_table = mapper_registry.metadata.tables.get(name_of_recipe_ingredients_table)

    if recipe_ingredients_table is None:
        raise KeyError(f"Table '{name_of_recipe_ingredients_table}' not found in metadata.")

    with database_engine.connect() as connection:
        select_statement = select(recipe_ingredients_table)
        result = connection.execute(select_statement)
        recipe_ingredients = result.fetchall()

        assert recipe_ingredients is not None
        assert len(recipe_ingredients) > 0
        print(recipe_ingredients)


# Test selecting all recipe instructions after population
def test_database_populate_select_all_recipe_instructions(database_engine):
    inspector = inspect(database_engine)
    name_of_recipe_instructions_table = inspector.get_table_names()[6]
    recipe_instructions_table = mapper_registry.metadata.tables.get(name_of_recipe_instructions_table)

    if recipe_instructions_table is None:
        raise KeyError(f"Table '{name_of_recipe_instructions_table}' not found in metadata.")

    with database_engine.connect() as connection:
        select_statement = select(recipe_instructions_table)
        result = connection.execute(select_statement)
        recipe_instructions = result.fetchall()

        assert recipe_instructions is not None
        assert len(recipe_instructions) > 0
        print(recipe_instructions)


# Test selecting all recipes after population
def test_database_populate_select_all_recipes(database_engine):
    inspector = inspect(database_engine)
    name_of_recipes_table = inspector.get_table_names()[7]
    recipes_table = mapper_registry.metadata.tables.get(name_of_recipes_table)

    if recipes_table is None:
        raise KeyError(f"Table '{name_of_recipes_table}' not found in metadata.")

    with database_engine.connect() as connection:
        select_statement = select(recipes_table)
        result = connection.execute(select_statement)
        recipes = result.fetchall()

        assert recipes is not None
        assert len(recipes) > 0
        print(recipes)

# Test selecting all reviews after population
def test_database_populate_select_all_reviews(database_engine):
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[8]
    reviews_table = mapper_registry.metadata.tables.get(name_of_reviews_table)

    if reviews_table is None:
        raise KeyError(f"Table '{name_of_reviews_table}' not found in metadata.")

    new_review = {
        'id': 1,
        'recipe_id': 1,
        'user_id': 1,
        'rating': 5,
        'comment': 'Great recipe!',
        'date': datetime.now()
    }

    with database_engine.connect() as connection:
        connection.execute(reviews_table.insert().values(new_review))

        select_statement = select(reviews_table)
        result = connection.execute(select_statement)
        reviews = result.fetchall()

        # Convert the result tuple to a dictionary for comparison
        review_dict = {
            'id': reviews[0][0],
            'recipe_id': reviews[0][1],
            'user_id': reviews[0][2],
            'rating': reviews[0][3],
            'comment': reviews[0][4],
            'date': reviews[0][5]
        }

        assert reviews is not None
        assert len(reviews) == 1
        assert review_dict == new_review

# Test selecting all users after population
def test_database_populate_select_all_users(database_engine):
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[9]
    users_table = mapper_registry.metadata.tables.get(name_of_users_table)

    if users_table is None:
        raise KeyError(f"Table '{name_of_users_table}' not found in metadata.")

    with database_engine.connect() as connection:
        select_statement = select(users_table)
        result = connection.execute(select_statement)
        users = result.fetchall()

        assert users is not None
        assert len(users) == 0
        print(users)