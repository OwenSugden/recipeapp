from flask import Blueprint, request, redirect, url_for, session
import recipe.adapters.repository as repo
import recipe.ratings.services as services
from recipe.authentication.authentication import login_required

ratings_blueprint = Blueprint('ratings_bp', __name__)

@ratings_blueprint.route('/rate/<int:recipe_id>', methods=['POST'])
@login_required
def rate_recipe(recipe_id):
    user_name = session['user_name']
    value = request.form.get('rating')

    if value:
        services.add_rating(repo.repo_instance, recipe_id, user_name, int(value))

    return redirect(url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id))
