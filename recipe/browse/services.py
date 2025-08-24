from recipe.adapters.repository import AbstractRepository



def get_number_of_recipes(repo: AbstractRepository):
    return repo.get_number_of_recipe()

def get_recipe(repo: AbstractRepository):
    recipes = repo.get_recipe()
    recipe_dicts = []

    for recipe in recipes:
        recipe_dict = {
            'id': recipe.id,
            'name': recipe.name,
            'author': recipe.author.name,
            'images': recipe.images
        }
        recipe_dicts.append(recipe_dict)
    return recipe_dicts