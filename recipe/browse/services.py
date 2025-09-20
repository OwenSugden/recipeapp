from recipe.adapters.repository import AbstractRepository

def get_number_of_recipes(repo: AbstractRepository):
    return repo.get_number_of_recipe()

def get_recipe(repo: AbstractRepository):
    recipes = repo.get_all_recipes()
    recipe_dicts = []

    for recipe in recipes:
        recipe_dict = {
            'id': recipe.id,
            'name': recipe.name,
            'author': recipe.author.name,
            'images': recipe.images,
            'category': recipe.category.name,
            'time': recipe.cook_time + recipe.preparation_time,
            'calories': recipe.nutrition.calories,
            'protein': recipe.nutrition.protein,
            'fat': recipe.nutrition.fat,
            'carbohydrates': recipe.nutrition.carbohydrates
        }
        recipe_dicts.append(recipe_dict)
    return recipe_dicts