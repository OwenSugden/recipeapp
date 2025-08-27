from flask import render_template, Blueprint, request

import recipe.adapters.repository as repo
import recipe.browse.services as services

browse_blueprint = Blueprint('browse_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse_recipe():
    num_recipe = services.get_number_of_recipes(repo.repo_instance)
    all_recipe = services.get_recipe(repo.repo_instance)

    page = request.args.get('page', 1, type=int)
    per_page = 100
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (num_recipe + per_page - 1) // per_page

    recipes_on_page = all_recipe[start:end]

    return render_template(
        'browse.html',
        title='Browse recipe',
        heading="Browse recipe",
        recipes=all_recipe,
        num_recipe=num_recipe,
        recipes_on_page=recipes_on_page,
        total_pages=total_pages,
        page=page,
    )

