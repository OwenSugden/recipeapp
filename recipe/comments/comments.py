from flask import Blueprint, request, redirect, url_for, session
import recipe.adapters.repository as repo
import recipe.comments.services as services
from recipe.authentication.authentication import login_required

comments_blueprint = Blueprint('comments_bp', __name__)


@comments_blueprint.route('/browse/<int:recipe_id>/comment', methods=['POST'])
@login_required
def add_comment(recipe_id):
    user_name = session['user_name']
    comment_text = request.form.get('comment')
    return_to = request.args.get("return_to")
    if comment_text:
        services.add_comment(repo.repo_instance, recipe_id, user_name, comment_text)

    # Redirect back to the recipe page
    return redirect(url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id, return_to=return_to))
