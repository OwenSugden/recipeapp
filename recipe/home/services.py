from typing import List

from recipe import Recipe
from recipe.adapters.repository import AbstractRepository

def get_recipes(repo: AbstractRepository) -> List[Recipe]:
    recipes = repo.get_recipes()
    return recipes