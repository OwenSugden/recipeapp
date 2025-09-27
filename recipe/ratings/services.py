from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel import recipe
from recipe.domainmodel.rating import Rating

def add_rating(repo: AbstractRepository, recipe_id: int, user_name: str, value: int):
    # Check if the user already has a rating
    user = repo.get_user(user_name)



    if not recipe:
        raise ValueError("Recipe not found")

    if not user:
        return None

    # Create new rating
    rating_id = len(repo.get_ratings_for_recipe(recipe_id)) + 1
    rating = Rating(rating_id, recipe_id, user.id, value, user_name)
    repo.add_rating(rating)
    return rating


def get_average_rating(repo: AbstractRepository, recipe_id: int):
    ratings = repo.get_ratings_for_recipe(recipe_id)
    if not ratings:
        return 0
    total = sum(r.value for r in ratings)
    return total / len(ratings)
