from datetime import datetime

from recipe import Recipe
from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User

def add_favourite(repo: AbstractRepository, user_id: int, recipe_id: int):
    fav = Favourite(repo.get_new_favourite_id(), user_id, recipe_id, datetime.now())
    repo.add_favourite(fav)

def remove_favourite(repo: AbstractRepository, user_id: int, recipe_id: int):
    repo.remove_favourite(user_id, recipe_id)

def get_recipe_by_id(repo: AbstractRepository, recipe_id: int) :
    return repo.get_recipe_by_id(recipe_id)

def get_user_favourites(repo: AbstractRepository, user_id: int):
    return repo.get_favourites_for_user(user_id)

def get_user_by_id(repo: AbstractRepository, user_id: int) :
    return repo.get_user_by_id(user_id)

def add_review(repo: AbstractRepository, user_id: int, recipe_id: int, rating: float, comment: str):
    review = Review(repo.get_new_review_id(), user_id, datetime.now(), recipe_id, rating, comment)
    repo.add_review(review)

def remove_review(repo: AbstractRepository, user_id: int, recipe_id: int):
    repo.remove_review(user_id, recipe_id)

def get_reviews_with_usernames_for_recipe(repo: AbstractRepository, recipe_id: int):
    return repo.get_reviews_with_usernames_for_recipe(recipe_id)

def get_average_rating(repo: AbstractRepository, recipe_id: int):
    return repo.get_average_rating(recipe_id)

def get_reviews_for_recipe(repo: AbstractRepository, recipe_id: int):
    return repo.get_reviews_for_recipe(recipe_id)



