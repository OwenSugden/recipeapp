from flask import render_template, Blueprint, request
import recipe.adapters.repository as repo
import recipe.browse.services as services

browse_blueprint = Blueprint('browse_bp', __name__)

def _apply_numeric_filter(rows, key, op, val):
    if val is None or op not in ('lt', 'gt'):
        return rows
    if op == 'lt':
        return [r for r in rows if (r.get(key) is not None and r[key] < val)]
    else:
        return [r for r in rows if (r.get(key) is not None and r[key] > val)]

@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    num_recipe  = services.get_number_of_recipes(repo.repo_instance)
    all_recipes = services.get_recipe(repo.repo_instance)

    q                = (request.args.get('q') or "").strip()
    filter_by        = (request.args.get('filter') or "").strip()
    sort_option      = (request.args.get('sort') or "").strip().lower()

    time_op          = (request.args.get('time_op') or '').strip()
    time_val         = request.args.get('time', type=int)

    calories_op      = (request.args.get('calories_op') or '').strip()
    calories_val     = request.args.get('calories', type=int)

    protein_op       = (request.args.get('protein_op') or '').strip()
    protein_val      = request.args.get('protein', type=int)

    fat_op           = (request.args.get('fat_op') or '').strip()
    fat_val          = request.args.get('fat', type=int)

    carbs_op = (request.args.get('carbohydrates_op') or '').strip()
    carbs_val= request.args.get('carbohydrates', type=int)

    categories = sorted({ r.get("category") for r in all_recipes if r.get("category") })
    categories = categories[4:]

    filtered = list(all_recipes)

    if q:
        ql = q.lower()
        filtered = [r for r in filtered if ql in ((r.get("name") or "").lower())]

    if filter_by and filter_by.lower() != "all":
        fb = filter_by.lower()
        filtered = [r for r in filtered if ((r.get("category") or "").lower() == fb)]

    filtered = _apply_numeric_filter(filtered, 'time', time_op, time_val)

    filtered = _apply_numeric_filter(filtered, 'calories',      calories_op,      calories_val)
    filtered = _apply_numeric_filter(filtered, 'protein',       protein_op,       protein_val)
    filtered = _apply_numeric_filter(filtered, 'fat',           fat_op,           fat_val)
    filtered = _apply_numeric_filter(filtered, 'carbohydrates', carbs_op, carbs_val)

    if sort_option == "name":
        filtered = sorted(filtered, key=lambda r: (r.get("name") or "").lower())
    elif sort_option == "author":
        filtered = sorted(filtered, key=lambda r: (r.get("author") or "").lower())

    page        = request.args.get('page', 1, type=int)
    per_page    = 24
    total_items = len(filtered)
    total_pages = max((total_items + per_page - 1) // per_page, 1)
    page        = max(1, min(page, total_pages))
    start       = (page - 1) * per_page
    end         = start + per_page
    recipes_on_page = filtered[start:end]

    return render_template(
        'browse.html',
        title='Browse recipe',
        heading='Browse recipe',
        recipes_on_page=recipes_on_page,
        total_pages=total_pages,
        page=page,
        q=q,
        filter=filter_by,
        sort_option=sort_option,
        total_items=total_items,
        num_recipe=num_recipe,
        categories=categories,
        time_op=time_op, time=time_val,
        calories_op=calories_op, calories=calories_val,
        protein_op=protein_op, protein=protein_val,
        fat_op=fat_op, fat=fat_val,
        carbohydrates_op=carbs_op, carbohydrates=carbs_val
    )
