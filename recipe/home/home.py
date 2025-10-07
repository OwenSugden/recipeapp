from flask import render_template, Blueprint
import recipe.adapters.repository as repo
import recipe.home.services as services
import random

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    all_recipes = services.get_recipes(repo.repo_instance)
    featured_recipes = random.sample(all_recipes, min(3, len(all_recipes)))
    return render_template('index.html',  recipes_on_page=featured_recipes)
