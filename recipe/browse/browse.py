from flask import render_template, Blueprint, request
import recipe.adapters.repository as repo
import recipe.browse.services as services

browse_blueprint = Blueprint('browse_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    q = (request.args.get('q') or "").strip()
    filter_by = (request.args.get('filter') or "").strip()
    sort_option = (request.args.get('sort') or "").strip().lower()

    time_op = (request.args.get('time_op') or '').strip()
    time_val = request.args.get('time', type=int)

    calories_op = (request.args.get('calories_op') or '').strip()
    calories_val = request.args.get('calories', type=int)

    protein_op = (request.args.get('protein_op') or '').strip()
    protein_val = request.args.get('protein', type=int)

    fat_op = (request.args.get('fat_op') or '').strip()
    fat_val = request.args.get('fat', type=int)

    carbs_op = (request.args.get('carbohydrates_op') or '').strip()
    carbs_val = request.args.get('carbohydrates', type=int)

    page = request.args.get('page', 1, type=int)
    per_page = 24

    dto = services.browse_recipes(
        repo=repo.repo_instance,
        q=q,
        filter_by=filter_by,
        sort_option=sort_option,
        numeric_filters={
            "time": (time_op, time_val),
            "calories": (calories_op, calories_val),
            "protein": (protein_op, protein_val),
            "fat": (fat_op, fat_val),
            "carbohydrates": (carbs_op, carbs_val),
        },
        page=page,
        per_page=per_page,
    )

    return render_template('browse.html', **dto)