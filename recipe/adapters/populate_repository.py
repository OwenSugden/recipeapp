import os
from pathlib import Path

from recipe.adapters.repository import AbstractRepository
from recipe.adapters.datareader.CSVdatareader import CSVDataReader


def populate(data_path: Path, repo: AbstractRepository, testing: bool):
    # Get the absolute path to the data directory
    dir_name = os.path.abspath(data_path)

    if testing:
        # Different files for the testing mode.
        recipe_filename = os.path.join(dir_name, "recipes-excerpt.csv")
    else:
        recipe_filename = os.path.join(dir_name, "recipes.csv")

    reader = CSVDataReader(recipe_filename)
    reader.read_recipes_csv()

    authors = reader.dataset_of_authors
    categories = reader.dataset_of_categories
    recipes = reader.dataset_of_recipes

    repo.add_multiple_authors(authors)
    repo.add_multiple_categories(categories)
    repo.add_multiple_recipes(recipes)

    recipe_images = reader.dataset_of_recipe_images
    recipe_ingredients = reader.dataset_of_recipe_ingredients
    recipe_instructions = reader.dataset_of_recipe_instructions

    repo.add_multiple_recipe_images(recipe_images)
    repo.add_multiple_recipe_ingredients(recipe_ingredients)
    repo.add_multiple_recipe_instructions(recipe_instructions)