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

def search_recipes(repo: AbstractRepository, search_query: str) -> List[Recipe]:
    searched_recipes = repo.search_recipes(search_query)
    return searched_recipes

def pagination(items, page, per_page):
    total_items = len(items)
    total_pages = max((total_items + per_page - 1) // per_page, 1)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], total_pages, page, total_items

def get_recipes_by_name(repo: AbstractRepository, name: str) -> List[Recipe]:
    recipes = repo.get_recipes_by_name(name)
    return recipes

def get_recipes_by_author(repo: AbstractRepository, author: str) -> List[Recipe]:
    recipes = repo.get_recipes_by_author(author)
    return recipes

def get_recipes_by_category(repo: AbstractRepository, category: str) -> List[Recipe]:
    recipes = repo.get_recipes_by_category(category)
    return recipes

