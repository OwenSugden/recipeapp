import pytest
from datetime import datetime

from recipe.domainmodel.user import User
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.review import Review

# Fixtures
@pytest.fixture
def my_user():
    return User("test user", "password123", 1)


@pytest.fixture
def my_author():
    return Author(1, "Gordon Ramsay")


@pytest.fixture
def my_category():
    return Category("Italian", [], 1)


@pytest.fixture
def my_recipe(my_author, my_category):
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

@pytest.fixture
def my_nutrition():
    return Nutrition(100.1, 10.1, 20.1, 30.2, 40.3,
                     50.4, 60.5, 70.6, 80.7)

@pytest.fixture
def my_favourite():
    return Favourite(1, 1)

@pytest.fixture
def my_review():
    return Review(1, 1, 1, 1, "Food is good")

# User tests
def test_user_construction():
    user = User("john_doe", "secret123", 1)
    assert user.id == 1
    assert user.username == "john_doe"
    assert user.password == "secret123"
    assert user.favourite_recipes == []
    assert user.reviews == []


def test_user_construction_without_id():
    user = User("jane_doe", "password456")
    assert user.id is None
    assert user.username == "jane_doe"


def test_user_equality():
    user1 = User("test", "pass", 1)
    user2 = User("test", "pass", 1)
    user3 = User("test", "pass", 2)
    assert user1 == user2
    assert user1 != user3


def test_user_less_than():
    user1 = User("test", "pass", 1)
    user2 = User("test", "pass", 2)
    assert user1 < user2


def test_user_hash():
    user1 = User("test", "pass", 1)
    user2 = User("test", "pass", 1)
    user_set = {user1, user2}
    assert len(user_set) == 1


# Author tests
def test_author_construction():
    author = Author(1, "Jamie Oliver")
    assert author.id == 1
    assert author.name == "Jamie Oliver"
    assert author.recipes == []


def test_author_equality():
    author1 = Author(1, "Chef A")
    author2 = Author(1, "Chef B")
    author3 = Author(2, "Chef A")
    assert author1 == author2
    assert author1 != author3


def test_author_less_than():
    author1 = Author(1, "Chef A")
    author2 = Author(2, "Chef B")
    assert author1 < author2


def test_author_hash():
    author1 = Author(1, "Chef A")
    author2 = Author(1, "Chef B")
    author_set = {author1, author2}
    assert len(author_set) == 1


def test_author_add_recipe(my_author, my_recipe):
    my_author.add_recipe(my_recipe)
    assert my_recipe in my_author.recipes


def test_author_add_duplicate_recipe(my_author, my_recipe):
    my_author.add_recipe(my_recipe)
    with pytest.raises(ValueError):
        my_author.add_recipe(my_recipe)


# Category tests
def test_category_construction():
    category = Category("Desserts", [], 1)
    assert category.id == 1
    assert category.name == "Desserts"
    assert category.recipes == []


def test_category_construction_without_id():
    category = Category("Main Course")
    assert category.id is None
    assert category.name == "Main Course"


def test_category_equality():
    category1 = Category("Italian", [], 1)
    category2 = Category("French", [], 1)
    category3 = Category("Italian", [], 2)
    assert category1 == category2
    assert category1 != category3


def test_category_less_than():
    category1 = Category("A", [], 1)
    category2 = Category("B", [], 2)
    assert category1 < category2


def test_category_hash():
    category1 = Category("Italian", [], 1)
    category2 = Category("French", [], 1)
    category_set = {category1, category2}
    assert len(category_set) == 1


def test_category_add_recipe(my_category, my_recipe):
    my_category.add_recipe(my_recipe)
    assert my_recipe in my_category.recipes


def test_category_add_invalid_recipe(my_category):
    with pytest.raises(TypeError):
        my_category.add_recipe("not a recipe")


# Recipe tests
def test_recipe_construction(my_author, my_category):
    recipe = Recipe(
        recipe_id=1,
        name="Test Recipe",
        author=my_author,
        cook_time=30,
        preparation_time=15,
        created_date=datetime(2024, 1, 1),
        description="Test description",
        images=["test.jpg"],
        category=my_category,
        ingredient_quantities=["1 cup flour"],
        ingredients=["flour"],
        rating=4.0,
        nutrition=None,
        servings="2",
        recipe_yield="2 portions",
        instructions=["Mix ingredients"]
    )
    assert recipe.id == 1
    assert recipe.name == "Test Recipe"
    assert recipe.author == my_author


def test_recipe_equality():
    author = Author(1, "Chef")

    recipe1 = Recipe(1, "Recipe A", author)
    recipe2 = Recipe(1, "Recipe B", author)
    recipe3 = Recipe(2, "Recipe A", author)

    assert recipe1 == recipe2
    assert recipe1 != recipe3


def test_recipe_less_than():
    author = Author(1, "Chef")

    recipe1 = Recipe(1, "Recipe A", author)
    recipe2 = Recipe(2, "Recipe B", author)

    assert recipe1 < recipe2


def test_recipe_hash():
    author = Author(1, "Chef")

    recipe1 = Recipe(1, "Recipe A", author)
    recipe2 = Recipe(1, "Recipe B", author)

    recipe_set = {recipe1, recipe2}
    assert len(recipe_set) == 1


def test_author_set_recipe(my_author):
    new_recipe = Recipe(200, "New Recipe", my_author)

    my_author.add_recipe(new_recipe)
    assert new_recipe in my_author.recipes


def test_author_set_recipe_invalid_type(my_author):
    with pytest.raises(TypeError):
        my_author.add_recipe("not a recipe")

# Nutrition tests
def test_nutrition_construction():
    nutrition = Nutrition(100.0, 10.0, 3.0, 20.0,
                          200.0,15.0, 5.0, 7.0,
                          8.0)
    assert nutrition.calories == 100.0
    assert nutrition.fat == 10.0
    assert nutrition.carbohydrates == 3.0
    assert nutrition.protein == 20.0


def test_nutrition_equality():
    n1 = Nutrition(100.0, 10.0, 3.0, 20.0, 200.0,
                   15.0, 5.0, 7.0, 8.0)
    n2 = Nutrition(100.0, 10.0, 3.0, 20.0, 200.0,
                   15.0, 5.0, 7.0, 8.0)
    n3 = Nutrition(120.0, 10.0, 3.0, 20.0, 200.0,
                   15.0, 5.0, 7.0, 8.0)
    assert n1 == n2
    assert n1 != n3

def test_nutrition_less_than():
    n1 = Nutrition(100.0, 10.0, 3.0, 20.0, 200.0,
                   15.0, 5.0, 7.0, 8.0)
    n2 = Nutrition(150.0, 10.0, 3.0, 20.0, 200.0,
                   15.0, 5.0, 7.0, 8.0)
    assert n1 < n2

def test_nutrition_hash():
    n1 = Nutrition(100.0, 10.0, 3.0, 20.0, 200.0,
                   15.0, 5.0, 7.0, 8.0)
    n2 = Nutrition(100.0, 10.0, 3.0, 20.0, 200.0,
                   15.0, 5.0, 7.0, 8.0)
    nutrition_set = {n1, n2}
    assert len(nutrition_set) == 1


# Favourite test
def test_favourite_construction(my_user, my_recipe):
    fav = Favourite(my_user.id, my_recipe.id)
    assert fav.user_id == my_user.id
    assert fav.recipe_id == my_recipe.id

def test_favourite_equality():
    fav1 = Favourite(1, 2)
    fav2 = Favourite(1, 2)
    fav3 = Favourite(1, 3)
    assert fav1 == fav2
    assert fav1 != fav3

def test_favourite_less_than():
    fav1 = Favourite(1, 2)
    fav2 = Favourite(2, 1)
    assert fav1 < fav2

def test_favourite_hash():
    fav1 = Favourite(1, 2)
    fav2 = Favourite(1, 2)
    fav_set = {fav1, fav2}
    assert len(fav_set) == 1

# Review test
def test_review_construction(my_recipe, my_user):
    review = Review(1, my_recipe.id, my_user.id, 5, "Excellent!")
    assert review.id == 1
    assert review.recipe_id == my_recipe.id
    assert review.user_id == my_user.id


def test_review_equality():
    r1 = Review(1, 7, 3, 5, "A")
    r2 = Review(1, 8, 4, 3, "B")
    r3 = Review(2, 7, 3, 5, "A")
    assert r1 == r2
    assert r1 != r3

def test_review_less_than():
    r1 = Review(1, 7, 3, 2, "apple")
    r2 = Review(2, 7, 3, 3, "banana")
    r3 = Review(3, 7, 3, 3, "zebra")
    assert r1 < r2        # lower rating
    assert r2 < r3        # same rating, compare comment

def test_review_hash():
    r1 = Review(1, 7, 3, 5, "nice")
    r2 = Review(1, 8, 4, 2, "different")
    review_set = {r1, r2}
    assert len(review_set) == 1

