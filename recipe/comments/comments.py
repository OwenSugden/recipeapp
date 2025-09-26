from flask import Blueprint, request, redirect, url_for, session
import recipe.adapters.repository as repo
import recipe.comments.services as services
from recipe.authentication.authentication import login_required

comments_blueprint = Blueprint('comments_bp', __name__)


@comments_blueprint.route('/browse/<int:recipe_id>/comment', methods=['POST'])
@login_required
def add_comment(recipe_id):
    # Redirect to login if not logged in
    # if 'user_name' not in session or not session['user_name'] or session is None:
    #     return redirect(url_for('authentication_bp.login', next=request.referrer or '/'))

    user_name = session['user_name']
    comment_text = request.form.get('comment')
    if comment_text:
        services.add_comment(repo.repo_instance, recipe_id, user_name, comment_text)

    # Redirect back to the recipe page
    return redirect(url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id))
