from recipe.adapters.repository import AbstractRepository

def get_recipe(repo: AbstractRepository, recipe_id: int) :
    return repo.get_recipe_by_id(recipe_id)
