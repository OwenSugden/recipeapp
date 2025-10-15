from flask import Blueprint, render_template, request, redirect, url_for, session
import recipe.adapters.repository as repo
import recipe.user_profile.services as services
from recipe.authentication.authentication import login_required

user_profile_blueprint = Blueprint('user_profile_bp', __name__)

@user_profile_blueprint.route('/user_profile', methods=['GET'])
def profile():
    section = request.args.get('section', 'profile')

    favourite_recipes = []
    reviews = []
    if 'user_id' in session:
        user_id = session['user_id']
        favourites = services.get_user_favourites(repo.repo_instance, user_id)
        favourite_recipes = [services.get_recipe_by_id(repo.repo_instance, fav.recipe_id) for fav in favourites]
        reviews = services.get_reviews_for_user(repo.repo_instance, user_id)


    return render_template(
        'user_profile.html',
        section=section,
        favourite_recipes=favourite_recipes,
        reviews=reviews
    )

@user_profile_blueprint.route('/user_profile/remove_favourite/<int:recipe_id>', methods=['POST'])
@login_required
def remove_favourite(recipe_id):
    user_id = session['user_id']
    services.remove_favourite(repo.repo_instance, user_id, recipe_id)

    return_to = request.args.get("return_to")

    return redirect(url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id, return_to=return_to))

@user_profile_blueprint.route('/user_profile/remove_review/<int:recipe_id>', methods=['POST'])
@login_required
def remove_review(recipe_id):
    user_id = session['user_id']
    services.remove_review(repo.repo_instance, user_id, recipe_id)
    review_id = request.form.get('review_id', type=int)

    if review_id is None:
        return redirect(url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id))

    services.remove_review(repo.repo_instance, user_id, review_id)
    return_to = request.form.get('return_to')

    if not return_to:
        return_to = url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id)

    return redirect(return_to)


@user_profile_blueprint.route('/user_profile/edit_profile', methods=['POST'])
def edit_profile():
    # TODO: check password, validate new username, update DB
    return redirect(url_for('user_profile_bp.profile', section='profile'))

@user_profile_blueprint.route('/user_profile/change_password', methods=['POST'])
def change_password():
    # TODO: validate old password, set new one
    return redirect(url_for('user_profile_bp.profile', section='profile'))
