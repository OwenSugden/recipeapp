from flask import Blueprint, render_template, request, redirect, url_for, session
import recipe.adapters.repository as repo
import recipe.favourites.services as services

user_profile_blueprint = Blueprint('user_profile_bp', __name__)

@user_profile_blueprint.route('/user_profile', methods=['GET'])
def profile():
    section = request.args.get('section', 'profile')

    favourites = []
    if 'user_name' in session:
        user_name= session['user_name']
        fav_ids = services.get_user_favourites(repo.repo_instance, user_name)  # returns list of recipe_ids
        favourites = [services.get_recipe_by_id(repo.repo_instance, rid) for rid in fav_ids]  # now list of recipe objects


        pass

    return render_template(
        'user_profile.html',
        section=section,
        favourites=favourites
    )

@user_profile_blueprint.route('/user_profile/add_favourite/<int:recipe_id>', methods=['POST'])
def add_favourite(recipe_id):
    if 'user_name' not in session:
        return redirect(url_for('authentication_bp.login'))

    user_name = session['user_name']
    services.add_favourite(repo.repo_instance, user_name, recipe_id)
    return redirect(url_for('user_profile_bp.profile', section='favourites'))


@user_profile_blueprint.route('/user_profile/remove_favourite/<int:recipe_id>', methods=['POST'])
def remove_favourite(recipe_id):
    if 'user_name' not in session:
        return redirect(url_for('authentication_bp.login'))

    user_name = session['user_name']
    services.remove_favourite(repo.repo_instance, user_name, recipe_id)
    return redirect(url_for('user_profile_bp.profile', section='favourites'))


@user_profile_blueprint.route('/user_profile/edit_profile', methods=['POST'])
def edit_profile():
    # TODO: check password, validate new username, update DB
    return redirect(url_for('user_profile_bp.profile', section='profile'))

@user_profile_blueprint.route('/user_profile/change_password', methods=['POST'])
def change_password():
    # TODO: validate old password, set new one
    return redirect(url_for('user_profile_bp.profile', section='profile'))
