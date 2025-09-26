from flask import Blueprint, render_template, request
import recipe.adapters.repository as repo
import recipe.recipe_detail.services as services

recipe_detail_blueprint = Blueprint('recipe_detail_bp', __name__)

@recipe_detail_blueprint.route('/browse/<int:recipe_id>', methods=['GET'])
def recipe_detail(recipe_id):
    return_to = request.args.get("return_to")
    recipe_object = services.get_recipe(repo.repo_instance, recipe_id)
    comments = services.get_comments(repo.repo_instance, recipe_id)
    return render_template('recipe_detail.html',
                           recipe=recipe_object,
                           comments=comments,
                           return_to=return_to)



# @recipe_detail_blueprint.route('/browse/<int:recipe_id>', methods=['GET', 'POST'])
# def recipe_detail(recipe_id):
#     return_to = request.args.get("return_to")
#     recipe_object = services.get_recipe(repo.repo_instance, recipe_id)
#     comments = services.get_comments(repo.repo_instance, recipe_id)
#
#     if request.method == "POST":
#         user_name = session['user_name']
#         comment_text = request.form.get("comment")
#         if comment_text:
#             # Safe to call service: user_name guaranteed to exist
#             services.add_comment(repo.repo_instance, recipe_id, user_name, comment_text)
#
#         return redirect(url_for('recipe_detail_bp.recipe_detail', recipe_id=recipe_id))
#
#     return render_template('recipe_detail.html',
#                            recipe=recipe_object,
#                            comments=comments,
#                            return_to=return_to)

