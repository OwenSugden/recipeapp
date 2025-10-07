import os
from pathlib import Path

from recipe.adapters.repository import AbstractRepository
from recipe.adapters.datareader.CSVdatareader import CSVDataReader


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool, testing: bool):
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

    # if database_mode:
    #     print("Populating additional tables...")
    #
    #     # Add recipe images
    #     recipe_images = getattr(reader, "dataset_of_recipe_images", None)
    #     add_imgs = getattr(repo, "add_multiple_recipe_images", None)
    #     if recipe_images and callable(add_imgs):
    #         add_imgs(recipe_images)
    #
    #     # Add recipe ingredients
    #     recipe_ingredients = getattr(reader, "dataset_of_recipe_ingredients", None)
    #     add_ingredients = getattr(repo, "add_multiple_recipe_ingredients", None)
    #     if recipe_ingredients and callable(add_ingredients):
    #         add_ingredients(recipe_ingredients)
    #
    #     # Add recipe instructions
    #     recipe_instructions = getattr(reader, "dataset_of_instructions", None)
    #     add_instructions = getattr(repo, "add_multiple_recipe_instructions", None)
    #     if recipe_instructions and callable(add_instructions):
    #         add_instructions(recipe_instructions)

