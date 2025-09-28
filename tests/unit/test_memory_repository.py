import pytest
from datetime import datetime

from recipe.domainmodel.comment import Comment
from recipe.domainmodel.rating import Rating
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.adapters.memory_repository import MemoryRepository
from recipe.domainmodel.user import User
from recipe.domainmodel.favourite import Favourite


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
def my_recipe():
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
        nutrition=None,
        servings="4",
        recipe_yield="4 portions",
        instructions=["Boil pasta", "Cook bacon", "Mix with eggs"]
    )

@pytest.fixture
def my_comment(my_recipe, my_user):
    user_name = getattr(my_user, "user_name", getattr(my_user, "username", "tester"))
    return Comment(user_name=user_name,
        comment_id=1,
        recipe_id=my_recipe.id,
        user_id=my_user.id,
        text="Great recipe!"
    )

@pytest.fixture
def my_rating(my_recipe, my_user):
    user_name = getattr(my_user, "user_name", getattr(my_user, "username", "tester"))
    return Rating(
        rating_id=1,
        recipe_id=my_recipe.id,
        user_id=my_user.id,
        value=5,
        user_name=user_name
    )

# MemoryRepository tests
def test_add_recipe(memory_repository, my_recipe):
    memory_repository.add_recipe(my_recipe)
    assert len(memory_repository.get_all_recipes()) == 1
    assert memory_repository.get_recipe_by_id(1) == my_recipe

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

def test_get_recipe_by_id_found(memory_repository, my_recipe):
    memory_repository.add_recipe(my_recipe)
    result = memory_repository.get_recipe_by_id(1)
    assert result == my_recipe
    assert result.name == "Spaghetti Carbonara"
    assert result.author.name == "Gordon Ramsay"

def test_get_recipe_by_id_not_found(memory_repository):
    assert memory_repository.get_recipe_by_id(9999) is None

def test_add_multiple_recipes(memory_repository, my_recipe):
    memory_repository.add_recipe(my_recipe)
    r2 = Recipe(
        recipe_id=2,
        name="Pesto",
        author=my_recipe.author,
        cook_time=10,
        preparation_time=5,
        created_date=my_recipe.date,
        description="Basil pesto",
        images=[],
        category=my_recipe.category,
        ingredient_quantities=[],
        ingredients=[],
        nutrition=None,
        servings="2",
        recipe_yield="2 portions",
        instructions=[]
    )
    memory_repository.add_recipe(r2)

    assert memory_repository.get_number_of_recipe() == 2
    assert memory_repository.get_recipe_by_id(1) is my_recipe
    assert memory_repository.get_recipe_by_id(2) is r2

def test_recipes_are_kept_sorted(memory_repository, my_recipe):
    r_high = Recipe(
        recipe_id=10, name="Z", author=my_recipe.author,
        cook_time=0, preparation_time=0, created_date=my_recipe.date,
        description="", images=[], category=my_recipe.category,
        ingredient_quantities=[], ingredients=[],
        nutrition=None, servings="", recipe_yield="", instructions=[]
    )
    memory_repository.add_recipe(r_high)
    memory_repository.add_recipe(my_recipe)

    recipes = memory_repository.get_all_recipes()
    assert recipes[0].id < recipes[1].id

def test_add_and_get_user(memory_repository, my_user):
    memory_repository.add_user(my_user)
    found = memory_repository.get_user("tests user")
    assert found is my_user

def test_get_user_not_found(memory_repository):
    assert memory_repository.get_user("no such user") is None

def test_add_invalid_then_valid_keeps_repo_consistent(memory_repository, my_recipe):
    memory_repository.add_recipe("not a recipe")
    memory_repository.add_recipe(my_recipe)
    assert memory_repository.get_number_of_recipe() == 1
    assert memory_repository.get_all_recipes()[0] is my_recipe

def test_add_and_get_comments(memory_repo, my_comment):
    memory_repo.add_comment(my_comment)
    assert my_comment in memory_repo.get_comments()
    assert memory_repo.get_comments_for_recipe(my_comment.recipe_id) == [my_comment]

def test_add_comment_type_error(memory_repo):
    with pytest.raises(TypeError):
        memory_repo.add_comment("not-a-comment")

def test_add_rating_replaces_previous_from_same_user(memory_repo, my_recipe, my_user):
    r1 = Rating(1, my_recipe.id, my_user.id, 2, user_name="alice")
    r2 = Rating(2, my_recipe.id, my_user.id, 5, user_name="alice")  # same user & recipe
    memory_repo.add_rating(r1)
    memory_repo.add_rating(r2)

    ratings = memory_repo.get_ratings_for_recipe(my_recipe.id)
    # Only one rating from 'alice' should remain, and it's the latest (value=5)
    user_ratings = [r for r in ratings if r.user_name == "alice"]
    assert len(user_ratings) == 1
    assert user_ratings[0].value == 5

def test_get_ratings_filters_by_recipe(memory_repo, my_recipe, my_user):
    r_ok = Rating(3, my_recipe.id, my_user.id, 4, user_name="bob")
    r_other = Rating(4, my_recipe.id + 1, my_user.id, 3, user_name="bob")
    memory_repo.add_rating(r_ok)
    memory_repo.add_rating(r_other)

    result = memory_repo.get_ratings_for_recipe(my_recipe.id)
    assert r_ok in result
    assert all(r.recipe_id == my_recipe.id for r in result)


def test_add_and_get_favourites(memory_repository, my_user, my_recipe):
    fav = Favourite(my_user.username, my_recipe.id)
    memory_repository.add_favourite(fav)

    favourites = memory_repository.get_favourites_for_user(my_user.username)
    assert favourites == [my_recipe.id]
    assert memory_repository.is_favourite(my_user.username, my_recipe.id)

def test_add_duplicate_favourite_only_once(memory_repository, my_user, my_recipe):
    fav = Favourite(my_user.username, my_recipe.id)
    memory_repository.add_favourite(fav)
    memory_repository.add_favourite(fav)  # attempt duplicate

    favourites = memory_repository.get_favourites_for_user(my_user.username)
    assert favourites == [my_recipe.id]
    assert len(favourites) == 1

def test_remove_favourite(memory_repository, my_user, my_recipe):
    fav = Favourite(my_user.username, my_recipe.id)
    memory_repository.add_favourite(fav)

    memory_repository.remove_favourite(fav)
    assert memory_repository.get_favourites_for_user(my_user.username) == []
    assert not memory_repository.is_favourite(my_user.username, my_recipe.id)

def test_get_favourites_for_user_empty(memory_repository, my_user):
    favourites = memory_repository.get_favourites_for_user(my_user.username)
    assert favourites == []

def test_is_favourite_false_for_nonexistent(memory_repository, my_user, my_recipe):
    assert not memory_repository.is_favourite(my_user.username, my_recipe.id)
