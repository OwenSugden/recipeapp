from bisect import insort_left
from typing import List
import os

from recipe.domainmodel.comment import Comment
from recipe.domainmodel.rating import Rating
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.user import User
from recipe.adapters.repository import AbstractRepository
from recipe.adapters.datareader.csvdatareader import CSVDataReader

### just added
import csv
from pathlib import Path
from datetime import date, datetime
from werkzeug.security import generate_password_hash
###

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__recipe = list()
        self.__users = list()
        self.__comments = list()
        self.__ratings = list()

    def add_recipe(self, recipe: Recipe):
        if isinstance(recipe, Recipe):
            insort_left(self.__recipe, recipe)

    def get_all_recipes(self) -> List[Recipe]:
        return self.__recipe

    def get_number_of_recipe(self):
        return len(self.__recipe)

    def get_recipe_by_id(self, recipe_id):
        for recipe in self.__recipe:
            if recipe.id == recipe_id:
                return recipe
        return None

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def add_comment(self, comment: Comment):
        if isinstance(comment, Comment):
            self.__comments.append(comment)
        else:
            raise TypeError("Expected a Comment instance")

    def get_comments(self) -> List[Comment]:
        return list(self.__comments)

    def get_comments_for_recipe(self, recipe_id: int) -> List[Comment]:
        return [c for c in self.__comments if c.recipe_id == recipe_id]

    # In MemoryRepository
    def add_rating(self, rating: Rating):
        # Remove previous rating from same user for this recipe
        self.__ratings = [r for r in self.__ratings
                         if not (r.user_name == rating.user_name and r.recipe_id == rating.recipe_id)]
        self.__ratings.append(rating)

    def get_ratings_for_recipe(self, recipe_id: int):
        return [r for r in self.__ratings if r.recipe_id == recipe_id]

def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    recipe_file_name = os.path.join(dir_name, "data/recipes.csv")
    reader = CSVDataReader(recipe_file_name)
    reader.read_csv_file()

    recipes = reader.get_recipes()

    for recipe in recipes:
        repo.add_recipe(recipe)

