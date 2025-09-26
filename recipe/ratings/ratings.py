from flask import Blueprint, request, redirect, url_for, session
import recipe.adapters.repository as repo
import recipe.ratings.services as services

ratings_blueprint = Blueprint('ratings_bp', __name__)

@ratings_blueprint.route('/rate/<int:recipe_id>', methods=['POST'])
def rate_recipe(recipe_id):
    if 'user_name' not in session or not session['user_name'] or session is None:
        return redirect(url_for('authentication_bp.login', next=request.path))

    user_name = session['user_name']
    value = request.form.get('rating')



    if value:
        services.add_rating(repo.repo_instance, recipe_id, user_name, int(value))

    return redirect(url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id))
