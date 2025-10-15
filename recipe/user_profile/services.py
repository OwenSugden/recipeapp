from datetime import datetime
from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.favourite import Favourite

def add_favourite(repo: AbstractRepository, user_id: int, recipe_id: int):
    fav = Favourite(repo.get_new_favourite_id(), user_id, recipe_id, datetime.now())
    repo.add_favourite(fav)

def remove_favourite(repo: AbstractRepository, user_id: int, recipe_id: int):
    repo.remove_favourite(user_id, recipe_id)

def get_user_favourites(repo: AbstractRepository, user_id: int):
    return repo.get_favourites_for_user(user_id)

def get_recipe_by_id(repo: AbstractRepository, recipe_id: int) :
    return repo.get_recipe_by_id(recipe_id)

def get_reviews_for_user(repo: AbstractRepository, user_id: int):
    return repo.get_reviews_and_recipes_for_user(user_id)

def remove_review(repo: AbstractRepository, user_id: int, recipe_id: int):
    repo.remove_review(user_id, recipe_id)


