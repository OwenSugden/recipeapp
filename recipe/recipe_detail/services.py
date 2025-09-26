from recipe.domainmodel.comment import Comment

def get_recipe(repo, recipe_id):
    return repo.get_recipe_by_id(recipe_id)

def get_comments(repo, recipe_id):
    return repo.get_comments_for_recipe(recipe_id)

def add_comment(repo, recipe_id, user_name, text):
    recipe = repo.get_recipe_by_id(recipe_id)
    user = repo.get_user(user_name)
    if not recipe:
        raise ValueError("Recipe not found")
    if not user:
        raise ValueError("User not found")

    next_id = len(repo.get_comments_for_recipe(recipe_id)) + 1
    comment = Comment(user_name, next_id, recipe_id, user.id, text)
    repo.add_comment(comment)
    return comment
