from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.user import User
from recipe.domainmodel.review import Review


def get_recipe_by_id(repo: AbstractRepository, recipe_id: int) :
    return repo.get_recipe_by_id(recipe_id)


