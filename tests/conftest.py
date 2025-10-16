import os
import pytest

from recipe import create_app
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

from datetime import datetime
from recipe.adapters.datareader.CSVdatareader import CSVDataReader
from recipe.adapters.memory_repository import MemoryRepository
from utils import get_project_root
from werkzeug.security import generate_password_hash
from recipe.adapters.populate_repository import populate

# Path to test data
TEST_DATA_PATH = get_project_root() / "tests" / "data"

@pytest.fixture
def memory_repository():
    return MemoryRepository()

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    populate(TEST_DATA_PATH, repo, True)
    return repo

@pytest.fixture
def csv_file_paths():
    current_dir = os.path.dirname(os.path.abspath(__file__))   # .../cs235.../tests
    tests_data_dir = os.path.join(current_dir, 'data')         # .../cs235.../tests/data
    file_name = os.path.join(tests_data_dir, 'recipes-excerpt.csv')
    assert os.path.exists(file_name), f"path {file_name} does not exist!"
    return file_name

@pytest.fixture
def sample_recipes(csv_file_paths):
    filename = csv_file_paths
    csv_reader = CSVDataReader(filename)

    csv_reader.read_recipes_csv()
    recipes = csv_reader.dataset_of_recipes

    return recipes

@pytest.fixture
def my_author():
    return Author(1, "Gordon Ramsay")

@pytest.fixture
def my_category():
    return Category(1, "Italian", [])

@pytest.fixture
def my_favourite(my_user, my_recipe):
    return Favourite(1, my_user.id, my_recipe.id, datetime(2024, 1, 1))

@pytest.fixture
def my_nutrition():
    return Nutrition(1, 100.1, 20.1, 30.2, 40.3,
                     50.4, 60.5, 70.6, 80.7, 45.0)

@pytest.fixture
def my_recipe(my_author, my_category, my_nutrition, my_recipe_image, my_recipe_ingredients, my_recipe_instructions):
    return Recipe(
        recipe_id=1,
        name="Spaghetti Carbonara",
        author=my_author,
        cook_time=20,
        preparation_time=15,
        created_date=datetime(2024, 1, 1),
        description="Classic Italian pasta dish",
        images=[my_recipe_image],
        category=my_category,
        ingredients=my_recipe_ingredients,
        nutrition=my_nutrition,
        servings=4,
        recipe_yield="4 portions",
        instructions=my_recipe_instructions,
    )

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
def my_recipe_ingredients():
    rin1 = RecipeIngredient(recipe_id=1, quantity="200 g", ingredient="spaghetti", position=0)
    rin2 = RecipeIngredient(recipe_id=1, quantity="100 g", ingredient="pancetta", position=1)
    rin3 = RecipeIngredient(recipe_id=1, quantity="2", ingredient="eggs", position=2)
    return [rin1, rin2, rin3]

@pytest.fixture
def my_recipe_instructions():
    rins1 = RecipeInstruction(recipe_id=1, step="Boil water in a large pot", position=0)
    rins2 = RecipeInstruction(recipe_id=1, step="Add spaghetti and cook until al dente", position=1)
    rins3 = RecipeInstruction(recipe_id=1, step="Mix with sauce and serve hot", position=2)
    return [rins1, rins2, rins3]

@pytest.fixture
def my_user():
    return User(1, "tests user", generate_password_hash("password123"))

@pytest.fixture
def my_review(my_user, my_recipe):
    return Review(1, my_user.id, datetime(2024, 1, 1), my_recipe.id, 5, "Food is good")