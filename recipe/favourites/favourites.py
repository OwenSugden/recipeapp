from flask import Blueprint, session, redirect, url_for, request, render_template
import recipe.favourites.services as fav_services

favourites_bp = Blueprint('favourites_bp', __name__)

@favourites_bp.route('/favourite/<int:recipe_id>', methods=['POST'])
def toggle_favourite(recipe_id):
    user_name = session.get('user_name')
    if not user_name:
        return redirect(url_for('authentication_bp.login', next=request.path))

    if fav_services.is_recipe_favourite(user_name, recipe_id):
        fav_services.remove_favourite(user_name, recipe_id)
    else:
        fav_services.add_favourite(user_name, recipe_id)

    return redirect(request.referrer or url_for('home_bp.home'))

@favourites_bp.route('/my-favourites')
def my_favourites():
    user_name = session.get('user_name')
    if not user_name:
        return redirect(url_for('authentication_bp.login'))
    fav_recipes = fav_services.get_user_favourites(user_name)
    return render_template('my_favourites.html', recipes=fav_recipes)
