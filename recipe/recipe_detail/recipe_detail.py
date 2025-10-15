from flask import Blueprint, render_template, request, session, redirect, url_for

import recipe.adapters.repository as repo
import recipe.recipe_detail.services as services
from recipe.authentication.authentication import login_required

recipe_detail_blueprint = Blueprint('recipe_detail_bp', __name__)

@recipe_detail_blueprint.route('/browse/<int:recipe_id>', methods=['GET'])
def recipe_detail(recipe_id):
    recipe = services.get_recipe_by_id(repo.repo_instance, recipe_id)

    return_to = request.args.get("return_to")

    avg_rating = services.get_average_rating(repo.repo_instance, recipe_id)

    recipe_ids = []
    username = ''
    reviews_with_names = services.get_reviews_with_usernames_for_recipe(repo.repo_instance, recipe_id)
    reviews_with_names.reverse()
    if 'user_id' in session:
        user_id = session['user_id']
        favourites = services.get_user_favourites(repo.repo_instance, user_id)
        recipe_ids = [fav.recipe_id for fav in favourites]

    return render_template(
        'recipe_detail.html',
        recipe=recipe,
        avg_rating=avg_rating,
        return_to=return_to,
        recipe_ids=recipe_ids,
        reviews_with_names=reviews_with_names,
        username = username
    )

@recipe_detail_blueprint.route('/browse/add_favourite/<int:recipe_id>', methods=['POST'])
@login_required
def add_favourite(recipe_id):
    user_id = session['user_id']
    services.add_favourite(repo.repo_instance, user_id, recipe_id)
    return_to = request.form.get('return_to')
    if not return_to:
        return_to = url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id)

    return redirect(return_to)

@recipe_detail_blueprint.route('/browse/remove_favourite/<int:recipe_id>', methods=['POST'])
@login_required
def remove_favourite(recipe_id):
    user_id = session['user_id']
    services.remove_favourite(repo.repo_instance, user_id, recipe_id)

    return_to = request.form.get('return_to')
    if not return_to:
        return_to = url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id)

    return redirect(return_to)

@recipe_detail_blueprint.route('/browse/add_review/<int:recipe_id>', methods=['POST'])
@login_required
def add_review(recipe_id):
    user_id = session['user_id']
    rating = request.form.get('rating')

    if not rating:
        print("This is run")
        return redirect(url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id))

    rating = float(rating)
    comment = request.form.get('comment')

    services.add_review(repo.repo_instance, user_id, recipe_id, rating, comment)
    return_to = request.form.get('return_to')

    if not return_to:
        return_to = url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id)

    return redirect(return_to)

@recipe_detail_blueprint.route('/browse/remove_review/<int:recipe_id>', methods=['POST'])
@login_required
def remove_review(recipe_id):
    user_id = session['user_id']
    review_id = request.form.get('review_id', type=int)

    if review_id is None:
        return redirect(url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id))

    services.remove_review(repo.repo_instance, user_id, review_id)
    return_to = request.form.get('return_to')

    if not return_to:
        return_to = url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id)

    return redirect(return_to)