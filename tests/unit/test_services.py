import pytest
from datetime import datetime

from recipe.domainmodel.comment import Comment
from recipe.domainmodel.rating import Rating
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.user import User
from recipe.recipe_detail.services import get_recipe_by_id as get_recipe_id


from recipe.adapters.memory_repository import MemoryRepository
from recipe.authentication import services as auth_services
from recipe.browse import services as browse_services
from recipe.recipe_detail import services as recipe_detail_services
from recipe.comments import services as comments_services
from recipe.ratings import services as ratings_services
from recipe.user_profile import services as fav_services

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
def my_recipe(my_author, my_category):
    return Recipe(recipe_id=2,
                  name="Lemon Herb Chicken",
                  author=my_author,
                  cook_time=35,
                  preparation_time=10,
                  created_date=datetime(2024, 2, 14),
                  description="Roast chicken thighs with lemon and herbs.",
                  images=["lemon_chicken.jpg", "plated.jpg"],
                  category=my_category,
                  ingredient_quantities=["4 thighs", "2 lemons", "1 tbsp rosemary", "3 cloves garlic"],
                  ingredients=["chicken", "lemon", "rosemary", "garlic", "olive oil", "salt", "pepper"],
                  nutrition=None,
                  servings="2",
                  recipe_yield="2 portions",
                  instructions=[]
        )

@pytest.fixture
def my_comment(my_recipe, my_user):
    user_name = getattr(my_user, "user_name", getattr(my_user, "username", "tester"))
    return Comment(user_name=user_name,
        comment_id=2,
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


#tests for get_number_of_recipes
def test_get_number_of_recipes_empty(memory_repository):
    result = browse_services.get_number_of_recipes(memory_repository)
    assert result == 0


def test_get_number_of_recipes_with_recipes(memory_repository, my_recipe):
    memory_repository.add_recipe(my_recipe)
    result = browse_services.get_number_of_recipes(memory_repository)
    assert result == 1


#tests for get_recipe
def test_get_recipe_empty_repository(memory_repository):
    result = browse_services.get_recipe(memory_repository)
    assert result == []


def test_get_recipe_with_single_recipe(memory_repository, my_recipe):
    memory_repository.add_recipe(my_recipe)
    result = browse_services.get_recipe(memory_repository)

    expected = [{
        'id': my_recipe.id,
        'name': my_recipe.name,
        'author': my_recipe.author.name,
        'images': my_recipe.images,
        'category': my_recipe.category.name if my_recipe.category else None,
        'time': (my_recipe.cook_time or 0) + (my_recipe.preparation_time or 0),
        'nutrition': my_recipe.nutrition,
        'calories': getattr(my_recipe.nutrition, 'calories', None),
        'protein': getattr(my_recipe.nutrition, 'protein', None),
        'fat': getattr(my_recipe.nutrition, 'fat', None),
        'carbohydrates': getattr(my_recipe.nutrition, 'carbohydrates', None),
    }]

    assert result == expected

def test_get_recipe_with_multiple_recipes(memory_repository, my_recipe, my_author, my_category):
    # Second recipe with different values
    r2 = Recipe(
        recipe_id=99,
        name="Pumpkin Risotto",
        author=my_author,
        cook_time=28,
        preparation_time=12,
        created_date=datetime(2024, 3, 3),
        description="Creamy risotto",
        images=["r2.jpg"],
        category=my_category,
        ingredient_quantities=[],
        ingredients=[],
        nutrition=None,           # keep None to avoid attr-name mismatches
        servings="3",
        recipe_yield="3 bowls",
        instructions=[]
    )

    memory_repository.add_recipe(my_recipe)
    memory_repository.add_recipe(r2)

    result = browse_services.get_recipe(memory_repository)

    # Build expecteds for both
    expected1 = {
        "id": my_recipe.id,
        "name": my_recipe.name,
        "author": my_recipe.author.name,
        "images": my_recipe.images,
        "category": my_recipe.category.name if my_recipe.category else None,
        "time": (my_recipe.cook_time or 0) + (my_recipe.preparation_time or 0),
        "nutrition": my_recipe.nutrition,
        "calories": getattr(my_recipe.nutrition, "calories", None),
        "protein": getattr(my_recipe.nutrition, "protein", None),
        "fat": getattr(my_recipe.nutrition, "fat", None),
        "carbohydrates": getattr(my_recipe.nutrition, "carbohydrates", None),
    }
    expected2 = {
        "id": r2.id,
        "name": r2.name,
        "author": r2.author.name,
        "images": r2.images,
        "category": r2.category.name if r2.category else None,
        "time": (r2.cook_time or 0) + (r2.preparation_time or 0),
        "nutrition": r2.nutrition,
        "calories": getattr(r2.nutrition, "calories", None),
        "protein": getattr(r2.nutrition, "protein", None),
        "fat": getattr(r2.nutrition, "fat", None),
        "carbohydrates": getattr(r2.nutrition, "carbohydrates", None),
    }

    # Assert size and per-item equality (order-agnostic)
    assert len(result) == 2
    r_by_id = {r["id"]: r for r in result}
    assert r_by_id[expected1["id"]] == expected1
    assert r_by_id[expected2["id"]] == expected2

def recipes():
    # Simple dict rows used by all tests
    return [
        {"id": 1, "name": "Chocolate Cake", "author": "Anna", "category": "Dessert",
         "time": 60, "calories": 450, "protein": 6, "fat": 20, "carbohydrates": 50},
        {"id": 2, "name": "Kimchi Stew", "author": "Bong", "category": "Korean",
         "time": 30, "calories": 300, "protein": 18, "fat": 10, "carbohydrates": 22},
        {"id": 3, "name": "Apple Pie", "author": "Cara", "category": "Dessert",
         "time": 45, "calories": 380, "protein": 4, "fat": 12, "carbohydrates": 55},
        {"id": 4, "name": "Greek Salad", "author": "Dora", "category": "Salad",
         "time": 10, "calories": 120, "protein": 3, "fat": 7, "carbohydrates": 12},
        {"id": 5, "name": "Pasta", "author": "Evan", "category": "Italian",
         "time": 25, "calories": 520, "protein": 15, "fat": 14, "carbohydrates": 60},
        {"id": 6, "name": "Tacos", "author": "Luis", "category": "Mexican",
         "time": 20, "calories": 430, "protein": 15, "fat": 18, "carbohydrates": 45},
    ]

def test_get_categories_empty_repository():
    # No rows → no categories (after skip)
    assert browse_services.get_categories([], skip_n=4) == []

def test_get_categories_with_single_recipe_no_skip(my_category):
    # One category present
    rows = [{"category": my_category.name}]
    assert browse_services.get_categories(rows, skip_n=0) == [my_category.name]

def test_get_categories_with_single_recipe_default_skip(my_category):
    # Default skip_n=4 will cut it out → empty
    rows = [{"category": my_category.name}]
    assert browse_services.get_categories(rows) == []

def test_filter_text_and_category_by_text():
    rows = recipes()
    out = browse_services.filter_text_and_category(rows, q="cake", filter_by="all")
    assert [r["name"] for r in out] == ["Chocolate Cake"]

def test_filter_text_and_category_by_category():
    rows = recipes()
    out = browse_services.filter_text_and_category(rows, q="", filter_by="Korean")
    assert [r["name"] for r in out] == ["Kimchi Stew"]

def test_apply_numeric_filter_lt():
    rows = recipes()
    out = browse_services.apply_numeric_filter(rows, key="calories", op="lt", val=400)
    assert {r["id"] for r in out} == {2, 3, 4}

def test_apply_numeric_filter_invalid_op_returns_same_list():
    rows = recipes()
    out = browse_services.apply_numeric_filter(rows, key="calories", op="eq", val=400)
    # Function returns the original list when op invalid → identity match
    assert out is rows

def test_sort_recipes_by_name_case_insensitive():
    rows = recipes()
    out = browse_services.sort_recipes(rows, sort_option="name")
    assert [r["name"] for r in out][:3] == ["Apple Pie", "Chocolate Cake", "Greek Salad"]

def test_sort_recipes_by_author():
    rows = recipes()
    out = browse_services.sort_recipes(rows, sort_option="author")
    assert [r["author"] for r in out][:3] == ["Anna", "Bong", "Cara"]

def test_pagination_middle_page():
    rows = recipes()
    page_items, total_pages, page, total_items = browse_services.pagination(rows, page=2, per_page=2)
    assert [r["id"] for r in page_items] == [3, 4]
    assert total_pages == 3 and page == 2 and total_items == 6

def test_pagination_clamps_to_last_page():
    rows = recipes()
    page_items, total_pages, page, _ = browse_services.pagination(rows, page=999, per_page=2)
    assert page == 3
    assert [r["id"] for r in page_items] == [5, 6]

#tests for get_recipe by ID
def test_get_recipe_by_id_empty_repository(memory_repository):
    result = recipe_detail_services.get_recipe_by_id(memory_repository, 1)
    assert result is None

def test_get_recipe_by_id_single_recipe(memory_repository, my_recipe):
    memory_repository.add_recipe(my_recipe)
    result = recipe_detail_services.get_recipe_by_id(memory_repository, my_recipe.id)
    assert result is my_recipe

def test_get_recipe_by_id_multiple_recipes(memory_repository, my_recipe, my_author, my_category):
    r2 = Recipe(
        recipe_id=99,
        name="Pumpkin Risotto",
        author=my_author,
        cook_time=28,
        preparation_time=12,
        created_date=datetime(2024, 3, 3),
        description="Creamy risotto",
        images=[],
        category=my_category,
        ingredient_quantities=[],
        ingredients=[],
        nutrition=None,
        servings="3",
        recipe_yield="3 bowls",
        instructions=[]
    )

    memory_repository.add_recipe(r2)
    memory_repository.add_recipe(my_recipe)

    assert recipe_detail_services.get_recipe_by_id(memory_repository, my_recipe.id) is my_recipe
    assert recipe_detail_services.get_recipe_by_id(memory_repository, r2.id) is r2

def test_can_add_user(memory_repository):
    new_user_name = 'coolcooker'
    new_password = 'Abcd1A23'

    # Create the user
    auth_services.add_user(new_user_name, new_password, memory_repository)

    user_as_dict = auth_services.get_user(new_user_name, memory_repository)
    assert user_as_dict is not None
    assert user_as_dict['user_name'] == new_user_name

    auth_services.authenticate_user(new_user_name, new_password, memory_repository)

    user_obj = memory_repository.get_user(new_user_name)
    assert user_obj is not None
    assert user_obj.check_password(new_password) is True

def test_cannot_add_user_with_existing_name(memory_repository):
    user_name = 'radcooker'
    password = 'abcd1A23'

    auth_services.add_user(user_name, password, memory_repository)

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, memory_repository)


def test_authentication_with_valid_credentials(memory_repository):
    new_user_name = 'fooddestroyer'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, memory_repository)

    auth_services.authenticate_user(new_user_name, new_password, memory_repository)

def test_authentication_with_invalid_credentials(memory_repository):
    new_user_name = 'fooddestroyer'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, memory_repository)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', memory_repository)

def test_get_comments_delegates_to_repo(memory_repo, my_comment):
    # Seed one comment in the repo
    memory_repo.add_comment(my_comment)

    result = comments_services.get_comments(memory_repo, my_comment.recipe_id)
    assert isinstance(result, list)
    assert my_comment in result


def test_add_comment_returns_none_when_user_missing(memory_repo, my_recipe):
    result = comments_services.add_comment(
        memory_repo, my_recipe.id, user_name="__no_such_user__", text="won't be saved"
    )
    assert result is None
    assert memory_repo.get_comments_for_recipe(my_recipe.id) == []


def test_add_rating_returns_none_for_missing_user(memory_repo, my_recipe):
    result = ratings_services.add_rating(memory_repo, my_recipe.id, "__no_such_user__", value=4)
    assert result is None
    assert ratings_services.get_average_rating(memory_repo, my_recipe.id) == 0


def test_add_favourite_for_missing_user(memory_repository, my_user, my_recipe):
    result = fav_services.add_favourite(memory_repository, "__no_such_user__", my_recipe.id)
    assert result is None


def test_remove_favourite_for_missing_user(memory_repository, my_user, my_recipe):
    result = fav_services.remove_favourite(memory_repository, "__no_such_user__", my_recipe.id)
    assert result is None

