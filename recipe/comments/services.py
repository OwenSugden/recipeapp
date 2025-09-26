from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel import recipe
from recipe.domainmodel.comment import Comment

def get_comments(repo: AbstractRepository, recipe_id: int):
    return repo.get_comments_for_recipe(recipe_id)

def add_comment(repo: AbstractRepository, recipe_id: int, user_name: str, text: str):
    user = repo.get_user(user_name)

    if not recipe:
        raise ValueError("Recipe not found")

    if not user:
        return None

    next_id = len(repo.get_comments_for_recipe(recipe_id)) + 1
    comment = Comment(user_name, next_id, recipe_id, user.id, text)
    repo.add_comment(comment)
    return comment
