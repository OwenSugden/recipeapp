from flask import Blueprint, render_template, request, session
import recipe.adapters.repository as repo
import recipe.recipe_detail.services as services
import recipe.ratings.services as ratings
import recipe.user_profile.services as fav_services


recipe_detail_blueprint = Blueprint('recipe_detail_bp', __name__)

@recipe_detail_blueprint.route('/browse/<int:recipe_id>', methods=['GET'])
def recipe_detail(recipe_id):
    recipe_object = services.get_recipe_by_id(repo.repo_instance, recipe_id)
    return_to = request.args.get("return_to")
    comments = services.get_comments(repo.repo_instance, recipe_id)
    avg_rating = ratings.get_average_rating(repo.repo_instance, recipe_id)
  
    favourites = []
    if 'user_name' in session:
        user_name = session['user_name']
        favourites = fav_services.get_user_favourites(repo.repo_instance, user_name)  # list of recipe_ids

    return render_template(
        'recipe_detail.html',
        recipe=recipe_object,
        comments=comments,
        avg_rating=avg_rating,
        return_to=return_to,
        favourites=favourites
    )







