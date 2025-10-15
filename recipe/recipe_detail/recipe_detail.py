from flask import Blueprint, render_template, request, session
from flask_wtf import FlaskForm

import recipe.adapters.repository as repo
import recipe.recipe_detail.services as services
from recipe.authentication.authentication import login_required

recipe_detail_blueprint = Blueprint('recipe_detail_bp', __name__)

@recipe_detail_blueprint.route('/browse/<int:recipe_id>', methods=['GET'])
def recipe_detail(recipe_id):
    recipe = services.get_recipe_by_id(repo.repo_instance, recipe_id)

    return_to = request.args.get("return_to")

    # comments = services.get_comments(repo.repo_instance, recipe_id)
    # avg_rating = ratings.get_average_rating(repo.repo_instance, recipe_id)

    recipe_ids = []
    if 'user_name' in session:
        user_id = session['user_id']
        favourites = services.get_user_favourites(repo.repo_instance, user_id)
        recipe_ids = [fav.recipe_id for fav in favourites]

    return render_template(
        'recipe_detail.html',
        recipe=recipe,
        # comments=comments,
        # avg_rating=avg_rating,
        return_to=return_to,
        recipe_ids=recipe_ids
    )




