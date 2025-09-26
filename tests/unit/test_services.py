import pytest
from datetime import datetime
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.browse.services import get_number_of_recipes, get_recipe
from recipe.adapters.memory_repository import MemoryRepository
from recipe.domainmodel.user import User
from recipe.recipe_detail.services import get_recipe as get_recipe_id


@pytest.fixture
def memory_repository():
    return MemoryRepository()

@pytest.fixture
def my_user():
    return User("test user_profile", "password123", 1)


@pytest.fixture
def my_author():
    return Author(1, "Gordon Ramsay")


@pytest.fixture
def my_category():
    return Category("Italian", [], 1)


@pytest.fixture
def sample_recipe(my_author, my_category):
    return Recipe(
        recipe_id=1,
        name="Spaghetti Carbonara",
        author=my_author,
        cook_time=20,
        preparation_time=15,
        created_date=datetime(2024, 1, 1),
        description="Classic Italian pasta dish",
        images=["image1.jpg"],
        category=my_category,
        ingredient_quantities=["200g pasta", "100g bacon"],
        ingredients=["pasta", "bacon", "eggs", "cheese"],
        rating=4.5,
        nutrition=None,
        servings="4",
        recipe_yield="4 portions",
        instructions=["Boil pasta", "Cook bacon", "Mix with eggs"]
    )


#tests for get_number_of_recipes
def test_get_number_of_recipes_empty(memory_repository):
    result = get_number_of_recipes(memory_repository)
    assert result == 0


def test_get_number_of_recipes_with_recipes(memory_repository, sample_recipe):
    memory_repository.add_recipe(sample_recipe)
    result = get_number_of_recipes(memory_repository)
    assert result == 1


#tests for get_recipe
def test_get_recipe_empty_repository(memory_repository):
    result = get_recipe(memory_repository)
    assert result == []


def test_get_recipe_with_single_recipe(memory_repository, sample_recipe):
    memory_repository.add_recipe(sample_recipe)
    result = get_recipe(memory_repository)

    expected = [{
        'id': 1,
        'name': "Spaghetti Carbonara",
        'author': "Gordon Ramsay",
        'images': ["image1.jpg"]
    }]

    assert result == expected

#tests for get_recipe by ID
def test_get_recipe_by_id_empty_repository(memory_repository):
    result = get_recipe_id(memory_repository, 1)
    assert result is None


def test_get_recipe_by_id_single_recipe(memory_repository, sample_recipe):
    memory_repository.add_recipe(sample_recipe)
    result = get_recipe_id(memory_repository, 1)
    assert result is sample_recipe

