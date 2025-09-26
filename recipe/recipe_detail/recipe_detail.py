from flask import render_template, Blueprint, request, url_for
import recipe.recipe_detail.services as services
import recipe.adapters.repository as repo

recipe_detail_blueprint = Blueprint('recipe_detail_bp', __name__)

@recipe_detail_blueprint.route('/browse/<int:recipe_id>', methods=['GET'])
def recipe_detail(recipe_id):
    recipe_object = services.get_recipe_by_id(repo.repo_instance, recipe_id)
    return_to = request.args.get("return_to")

    return render_template('recipe_detail.html', recipe=recipe_object,
                           return_to=return_to)







