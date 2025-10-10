from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import recipe.adapters.repository as repo
import recipe.browse.services as services

browse_blueprint = Blueprint('browse_bp', __name__)


@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    # All recipes
    recipes = services.get_recipes(repo.repo_instance)
    number_of_recipes = len(recipes)

    # Get search query
    search_query = request.args.get('q', '')
    filter_by = request.args.get('filter_by', 'name')

    if search_query:
        search_query_lower = search_query.lower()

        if filter_by == 'name':
            recipes = services.get_recipes_by_name(repo.repo_instance, search_query_lower)

        elif filter_by == 'author':
            recipes = services.get_recipes_by_author(repo.repo_instance, search_query_lower)

        elif filter_by == 'category':
            recipes = services.get_recipes_by_category(repo.repo_instance, search_query_lower)

    # Pagination logic
    page = request.args.get('page', 1, type=int)
    per_page = 24
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(recipes) + per_page - 1) // per_page
    recipes_on_page = recipes[start:end]

    return render_template('browse.html',
                           total_pages=total_pages,
                           page=page,
                           search_query=search_query,
                           recipes_on_page=recipes_on_page,
                           number_of_recipes=number_of_recipes)
