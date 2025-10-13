from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import recipe.adapters.repository as repo
import recipe.browse.services as services

browse_blueprint = Blueprint('browse_bp', __name__)


@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    search_query = (request.args.get('q') or '').strip()
    filter_by = request.args.get('filter_by', 'name')
    page = request.args.get('page', 1, type=int)
    per_page = 24

    # All recipes
    recipes = services.get_recipes(repo.repo_instance)

    if search_query:
        search_query_lower = search_query.lower()

        if filter_by == 'name':
            recipes = services.get_recipes_by_name(repo.repo_instance, search_query_lower)

        elif filter_by == 'author':
            recipes = services.get_recipes_by_author(repo.repo_instance, search_query_lower)

        elif filter_by == 'category':
            recipes = services.get_recipes_by_category(repo.repo_instance, search_query_lower)

    number_of_recipes = len(recipes)

    # Pagination
    total_pages = max(1, (number_of_recipes + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    recipes_on_page = recipes[start:end]

    args = request.args.to_dict(flat=True)
    prev_url = None
    next_url = None
    if page > 1:
        prev_args = {**args, "page": page - 1}
        prev_url = url_for('browse_bp.browse', **prev_args)
    if page < total_pages:
        next_args = {**args, "page": page + 1}
        next_url = url_for('browse_bp.browse', **next_args)

    return render_template(
        'browse.html',
        recipes_on_page=recipes_on_page,
        number_of_recipes=number_of_recipes,
        search_query=search_query,
        filter_by=filter_by,
        page=page,
        total_pages=total_pages,
        prev_url=prev_url,
        next_url=next_url,
    )
