from flask import render_template, Blueprint

import recipe.adapters.repository as repo
import recipe.browse.services as services

browse_blueprint = Blueprint('recipe_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse_recipe():
    num_recipe = services.get_number_of_recipes(repo.repo_instance)
    all_recipe = services.get_recipe(repo.repo_instance)
    return render_template(
        'browse.html',
        title='Browse recipe',
        heading="Browse recipe",
        recipes=all_recipe,
        num_recipe=num_recipe,
    )
