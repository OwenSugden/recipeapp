from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.favourite import Favourite

def add_favourite(repo: AbstractRepository, user_name: str, recipe_id: int):
    fav = Favourite(user_name, recipe_id)
    repo.add_favourite(fav)

def remove_favourite(repo: AbstractRepository, user_name: str, recipe_id: int):
    fav = Favourite(user_name, recipe_id)
    repo.remove_favourite(fav)

def get_user_favourites(repo: AbstractRepository, user_name: str):
    return repo.get_favourites_for_user(user_name)

def is_recipe_favourite(repo: AbstractRepository, user_name: str, recipe_id: int):
    return repo.is_favourite(user_name, recipe_id)

def get_recipe_by_id(repo: AbstractRepository, recipe_id: int) :
    return repo.get_recipe_by_id(recipe_id)
