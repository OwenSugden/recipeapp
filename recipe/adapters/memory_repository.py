from bisect import insort_left
from typing import List
import os

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


def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    recipe_file_name = os.path.join(dir_name, "data/recipes.csv")
    reader = CSVDataReader(recipe_file_name)
    reader.read_csv_file()

    recipes = reader.get_recipes()

    for recipe in recipes:
        repo.add_recipe(recipe)

