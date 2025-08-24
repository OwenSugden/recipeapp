from bisect import insort_left
from typing import List
import os

from recipe.domainmodel.recipe import Recipe
from recipe.adapters.repository import AbstractRepository
from recipe.adapters.datareader.csvdatareader import CSVDataReader

class MemoryRepository(AbstractRepository):
    def __init__(self, path: str):
        self.__recipe = list()

    def add_recipe(self, recipe: Recipe):
        if isinstance(recipe, Recipe):
            insort_left(self.__recipe, recipe)

    def get_recipe(self) -> List[Recipe]:
        return self.__recipe

    def get_number_of_recipe(self):
        return len(self.__recipe)

def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    recipe_file_name = os.path.join(dir_name, "data/recipes.csv")
    reader = CSVDataReader(recipe_file_name)
    recipes = reader.get_recipes()

    for recipe in recipes:
        repo.add_recipe(recipe)