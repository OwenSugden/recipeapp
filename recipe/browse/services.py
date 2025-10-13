from typing import Dict, List

from recipe import Recipe
from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.category import Category


def get_recipes(repo: AbstractRepository) -> List[Recipe]:
    recipes = repo.get_recipes()
    return recipes

def get_number_of_recipes(repo: AbstractRepository) -> int:
    number_of_recipes = repo.get_number_of_recipes()
    return number_of_recipes

def get_recipes_by_name(repo: AbstractRepository, name: str) -> List[Recipe]:
    recipes = repo.get_recipes_by_name(name)
    return recipes

def get_recipes_by_author(repo: AbstractRepository, author: str) -> List[Recipe]:
    recipes = repo.get_recipes_by_author(author)
    return recipes

def get_recipes_by_category(repo: AbstractRepository, category: str) -> List[Recipe]:
    recipes = repo.get_recipes_by_category(category)
    return recipes

