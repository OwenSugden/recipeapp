from flask import render_template, Blueprint, request

import recipe.adapters.repository as repo
import recipe.browse.services as services

browse_blueprint = Blueprint('browse_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    num_recipe = services.get_number_of_recipes(repo.repo_instance)
    all_recipe = services.get_recipe(repo.repo_instance)
    all_recipe = sorted(all_recipe, key=lambda r: (r["name"] or "").lower())

    q = (request.args.get('q') or "").strip()
    if q:
        ql = q.lower()
        filtered = [r for r in all_recipe if ql in (r.get("name") or "").lower()]
    else:
        filtered = all_recipe

    page = request.args.get('page', 1, type=int)
    per_page = 24
    total_items = len(filtered)
    total_pages = max((total_items + per_page - 1) // per_page, 1)
    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    end = start + per_page
    recipes_on_page = filtered[start:end]

    return render_template(
        'browse.html',
        title='Browse recipe',
        heading="Browse recipe",
        recipes_on_page=recipes_on_page,
        total_pages=total_pages,
        page=page,
        q=q,
        total_items=total_items,
        num_recipe=num_recipe
    )