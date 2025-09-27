import csv
import re
import ast

from datetime import datetime
from bisect import insort_left
from typing import List
from pathlib import Path

from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.user import User

from recipe.adapters.repository import AbstractRepository

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__recipe = list()
        self.__recipes_index = dict()
        self.__users = list()

    def add_recipe(self, recipe: Recipe):
        if isinstance(recipe, Recipe):
            insort_left(self.__recipe, recipe)
            self.__recipes_index[recipe.id] = recipe

    def get_all_recipes(self) -> List[Recipe]:
        return self.__recipe

    def get_number_of_recipe(self):
        return len(self.__recipe)

    def get_recipe_by_id(self, recipe_id):
        for recipe in self.__recipe:
            if recipe.id == recipe_id:
                return recipe
        return None

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.username == username), None)

def read_csv_file(filename: str, authors, categories) -> List[Recipe]:
    recipes: List[Recipe] = []

    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Skip header row if present
        next(reader, None)

        for line in reader:
            recipe = create_object(line, authors, categories)
            if recipe:
                recipes.append(recipe)

    return recipes


def create_object(line, authors, categories) -> Recipe:
    recipe_id = int(line[0])
    name = line[1]
    author_id = int(line[2])
    author_name = line[3]
    cook_time = int(line[4])
    preparation_time = int(line[5])
    total_time = line[6]
    created_date = datetime.strptime(re.sub(r'(st|nd|rd|th)', '', line[7]), "%d %b %Y")
    description = line[8]
    images = ast.literal_eval(line[9])
    category = line[10]
    ingredient_quantities = ast.literal_eval(line[11])
    ingredients = ast.literal_eval(line[12])
    calories = float(line[13])
    fat_content = float(line[14])
    saturated_fat_content = float(line[15])
    cholesterol_content = float(line[16])
    sodium_content = float(line[17])
    carb_content = float(line[18])
    fiber_content = float(line[19])
    sugar_content = float(line[20])
    protein_content = float(line[21])
    servings = line[22]
    recipe_yield = line[23]
    instructions = ast.literal_eval(line[24])

    # authors dict
    if author_name in authors:
        author = authors[author_name]
    else:
        author = Author(author_id, author_name)
        authors[author_name] = author

    # categories dict
    if category in categories:
        category_obj = categories[category]
    else:
        category_obj = Category(category, None, recipe_id)
        categories[category] = category_obj

    nutrition = Nutrition(
        calories,
        fat_content,
        saturated_fat_content,
        cholesterol_content,
        sodium_content,
        carb_content,
        fiber_content,
        sugar_content,
        protein_content,
    )

    recipe = Recipe(
        recipe_id,
        name,
        author,
        cook_time,
        preparation_time,
        created_date,
        description,
        images,
        category_obj,
        ingredient_quantities,
        ingredients,
        nutrition,
        servings,
        recipe_yield,
        instructions,
    )

    return recipe

def load_recipe(data_path: Path, repo: MemoryRepository) -> None:
    filename = str(data_path / "recipes.csv")
    authors = dict()
    categories = dict()
    recipes = read_csv_file(filename, authors, categories)

    for r in recipes:
        repo.add_recipe(r)

def populate(data_path: Path, repo: MemoryRepository):
    load_recipe(data_path, repo)


