from flask import Blueprint, render_template, request, redirect, url_for, session

user_profile_blueprint = Blueprint('user_profile_bp', __name__)

@user_profile_blueprint.route('/user_profile', methods=['GET'])
def profile():
    section = request.args.get('section', 'profile')

    # Example data (in practice: pull from your repo/service layer)
    favourites = []
    if 'user_id' in session:
        # get favourites from database/repository for this user
        pass

    return render_template(
        'user_profile.html',
        section=section,
        favourites=favourites
    )

@user_profile_blueprint.route('/user_profile/remove_favourite/<int:recipe_id>', methods=['POST'])
def remove_favourite(recipe_id):
    # TODO: actually remove from user’s favourites
    return redirect(url_for('user_profile_bp.profile', section='favourites'))

@user_profile_blueprint.route('/user_profile/edit_profile', methods=['POST'])
def edit_profile():
    # TODO: check password, validate new username, update DB
    return redirect(url_for('user_profile_bp.profile', section='profile'))

@user_profile_blueprint.route('/user_profile/change_password', methods=['POST'])
def change_password():
    # TODO: validate old password, set new one
    return redirect(url_for('user_profile_bp.profile', section='profile'))
