import pytest
from datetime import datetime
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.adapters.memory_repository import MemoryRepository
from recipe.domainmodel.user import User


# Fixtures
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
def sample_recipe():
    author = Author(1, "Gordon Ramsay")
    category = Category("Italian", [], 1)
    return Recipe(
        recipe_id=1,
        name="Spaghetti Carbonara",
        author=author,
        cook_time=20,
        preparation_time=15,
        created_date=datetime(2024, 1, 1),
        description="Classic Italian pasta dish",
        images=["image1.jpg"],
        category=category,
        ingredient_quantities=["200g pasta", "100g bacon"],
        ingredients=["pasta", "bacon", "eggs", "cheese"],
        rating=4.5,
        nutrition=None,
        servings="4",
        recipe_yield="4 portions",
        instructions=["Boil pasta", "Cook bacon", "Mix with eggs"]
    )


# MemoryRepository tests
def test_add_recipe(memory_repository, sample_recipe):
    memory_repository.add_recipe(sample_recipe)
    assert len(memory_repository.get_all_recipes()) == 1
    assert memory_repository.get_recipe_by_id(1) == sample_recipe

def test_add_recipe_invalid_type(memory_repository):
    memory_repository.add_recipe("not a recipe")
    assert len(memory_repository.get_all_recipes()) == 0

def test_add_recipe_none(memory_repository):
    memory_repository.add_recipe(None)
    assert len(memory_repository.get_all_recipes()) == 0

def test_get_all_recipes_empty(memory_repository):
    assert memory_repository.get_all_recipes() == []

def test_get_number_of_recipe_empty(memory_repository):
    assert memory_repository.get_number_of_recipe() == 0

def test_get_recipe_by_id_found(memory_repository, sample_recipe):
    memory_repository.add_recipe(sample_recipe)
    result = memory_repository.get_recipe_by_id(1)
    assert result == sample_recipe
    assert result.name == "Spaghetti Carbonara"
    assert result.author.name == "Gordon Ramsay"