
from recipe.home import services as home_services
from recipe.authentication import services as auth_services
from recipe.browse import services as browse_services
from recipe.recipe_detail import services as recipe_detail_services
from recipe.user_profile import services as fav_services

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


# Authentication services tests


# UserProfile services tests
