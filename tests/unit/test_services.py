import pytest

from recipe.authentication.services import NameNotUniqueException, AuthenticationException, UnknownUserException
from recipe.home import services as home_services
from recipe.authentication import services as auth_services
from recipe.browse import services as browse_services
from recipe.recipe_detail import services as recipe_detail_services
from recipe.user_profile import services as profile_services

# Home services tests
def test_get_recipes_home(in_memory_repo, sample_recipes):
    recipes_from_service = home_services.get_recipes(in_memory_repo)
    assert recipes_from_service[0] == sample_recipes[0]

# Browse services tests
def test_get_recipes_browse(in_memory_repo, sample_recipes):
    recipes_from_service = browse_services.get_recipes(in_memory_repo)
    assert recipes_from_service[0] == sample_recipes[0]

def test_get_number_of_recipes_browse(in_memory_repo, sample_recipes):
    number_of_recipes_from_service = browse_services.get_number_of_recipes(in_memory_repo)
    assert number_of_recipes_from_service == len(sample_recipes)

# RecipeDetail services tests
# TODO finish this
def test_add_and_get_favourite_recipe_detail(in_memory_repo, my_user, my_recipe):
    recipe_detail_services.add_favourite(in_memory_repo, my_user.id, my_recipe.id)
    favourites = recipe_detail_services.get_user_favourites(in_memory_repo, my_user.id)

    assert len(favourites) == 1
    assert favourites[0].recipe_id == my_recipe.id

def test_remove_favourite_recipe_detail(in_memory_repo, my_user, my_recipe):
    recipe_detail_services.add_favourite(in_memory_repo, my_user.id, my_recipe.id)
    recipe_detail_services.remove_favourite(in_memory_repo, my_user.id, my_recipe.id)

    favourites = recipe_detail_services.get_user_favourites(in_memory_repo, my_user.id)
    assert favourites == []

def test_add_and_get_review_recipe_detail(in_memory_repo, my_user, my_recipe):
    recipe_detail_services.add_review(in_memory_repo, my_user.id, my_recipe.id, 5, "yummy")
    reviews = recipe_detail_services.get_reviews_for_recipe(in_memory_repo, my_recipe.id)

    assert len(reviews) == 1
    assert reviews[0].comment == "yummy"

def test_average_rating_recipe_detail_same_user(in_memory_repo, my_user, my_recipe):
    recipe_detail_services.add_review(in_memory_repo, my_user.id, my_recipe.id, 3, "trash")
    recipe_detail_services.add_review(in_memory_repo, my_user.id, my_recipe.id, 1, "mid")

    avg = recipe_detail_services.get_average_rating(in_memory_repo, my_recipe.id)
    assert avg == 3.0

# Authentication services tests
# TODO finish this
def test_can_add_user(in_memory_repo):
    new_user_name = "bob"
    new_password = "clownfish"

    auth_services.add_user(new_user_name, new_password, in_memory_repo)
    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)

    assert user_as_dict["user_name"] == new_user_name
    assert user_as_dict["password"].startswith("scrypt:32768")

def test_cannot_add_user_with_existing_name(in_memory_repo):
    auth_services.add_user("bob", "abc123", in_memory_repo)
    with pytest.raises(NameNotUniqueException):
        auth_services.add_user("bob", "abc1234", in_memory_repo)

def test_authentication_with_valid_credentials(in_memory_repo):
    auth_services.add_user("charlie", "abc123", in_memory_repo)
    auth_services.authenticate_user("charlie", "abc123", in_memory_repo)

def test_authentication_with_invalid_password(in_memory_repo):
    auth_services.add_user("dave", "abc123", in_memory_repo)
    with pytest.raises(AuthenticationException):
        auth_services.authenticate_user("dave", "abc1234", in_memory_repo)

def test_get_unknown_user_raises(in_memory_repo):
    with pytest.raises(UnknownUserException):
        auth_services.get_user("ghost", in_memory_repo)



# UserProfile services tests
# TODO finish this

def test_can_add_and_get_user_favourites(in_memory_repo, my_user, my_recipe):
    profile_services.add_favourite(in_memory_repo, my_user.id, my_recipe.id)
    favourites = profile_services.get_user_favourites(in_memory_repo, my_user.id)

    assert len(favourites) == 1

def test_can_remove_user_favourite(in_memory_repo, my_user, my_recipe):
    profile_services.add_favourite(in_memory_repo, my_user.id, my_recipe.id)
    profile_services.remove_favourite(in_memory_repo, my_user.id, my_recipe.id)
    favourites = profile_services.get_user_favourites(in_memory_repo, my_user.id)

    assert favourites == []

