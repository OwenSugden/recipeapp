from flask import Blueprint, request, redirect, url_for

search_blueprint = Blueprint('search_bp', __name__)

@search_blueprint.route('/search', methods=['GET'])
def search():
    q         = (request.args.get('q') or '').strip()
    filter_by = (request.args.get('filter') or '').strip()
    sort      = (request.args.get('sort') or '').strip().lower()

    params = {}
    if q:
        params['q'] = q
    if filter_by and filter_by != 'all':
        params['filter'] = filter_by
    if sort in {'name', 'author'}:
        params['sort'] = sort

    return redirect(url_for('browse_bp.browse', **params))