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
    return User("tests user", "password123", 1)


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

def test_get_recipe_by_id_not_found(memory_repository):
    assert memory_repository.get_recipe_by_id(9999) is None

def test_add_multiple_recipes(memory_repository, sample_recipe):
    memory_repository.add_recipe(sample_recipe)
    r2 = Recipe(
        recipe_id=2,
        name="Pesto",
        author=sample_recipe.author,
        cook_time=10,
        preparation_time=5,
        created_date=sample_recipe.date,
        description="Basil pesto",
        images=[],
        category=sample_recipe.category,
        ingredient_quantities=[],
        ingredients=[],
        rating=None,
        nutrition=None,
        servings="2",
        recipe_yield="2 portions",
        instructions=[]
    )
    memory_repository.add_recipe(r2)

    assert memory_repository.get_number_of_recipe() == 2
    assert memory_repository.get_recipe_by_id(1) is sample_recipe
    assert memory_repository.get_recipe_by_id(2) is r2

def test_recipes_are_kept_sorted(memory_repository, sample_recipe):
    r_high = Recipe(
        recipe_id=10, name="Z", author=sample_recipe.author,
        cook_time=0, preparation_time=0, created_date=sample_recipe.date,
        description="", images=[], category=sample_recipe.category,
        ingredient_quantities=[], ingredients=[], rating=None,
        nutrition=None, servings="", recipe_yield="", instructions=[]
    )
    memory_repository.add_recipe(r_high)
    memory_repository.add_recipe(sample_recipe)

    recipes = memory_repository.get_all_recipes()
    assert recipes[0].id < recipes[1].id

def test_add_and_get_user(memory_repository, my_user):
    memory_repository.add_user(my_user)
    found = memory_repository.get_user("tests user")
    assert found is my_user

def test_get_user_not_found(memory_repository):
    assert memory_repository.get_user("no such user") is None

def test_add_invalid_then_valid_keeps_repo_consistent(memory_repository, sample_recipe):
    memory_repository.add_recipe("not a recipe")
    memory_repository.add_recipe(sample_recipe)
    assert memory_repository.get_number_of_recipe() == 1
    assert memory_repository.get_all_recipes()[0] is sample_recipe