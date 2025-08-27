import os
import csv
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from datetime import datetime
import re
import ast


class CSVDataReader:
    def __init__(self, filename: str):
        self.__filename = filename
        self.__recipes = list()
        self.__authors = dict()
        self.__categories = dict()

    def read_csv_file(self):
        with open(self.__filename, 'r') as csvfile:
            reader = csv.reader(csvfile)

            # skip header
            next(reader)
            for line in reader:
                self.create_object(line)

    def parse_date(self, date_str):
        new_date = re.sub(r'(st|nd|rd|th)', '', date_str)
        return datetime.strptime(new_date, "%d %b %Y")

    def create_object(self, line):
        recipe_id = int(line[0])
        name = line[1]
        author_id = int(line[2])
        author_name = line[3]
        cook_time = int(line[4])
        preparation_time = int(line[5])
        total_time = line[6]
        created_date = self.parse_date(line[7])
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

        if author_name in self.__authors:
            author = self.__authors[author_name]
        else:
            author = Author(author_id, author_name)
            self.__authors[author_name] = author
        if category in self.__categories:
            category_obj = self.__categories[category]
        else:
            category_obj = Category(category, None, recipe_id)
            self.__categories[category] = category_obj

        nutrition = Nutrition(
            calories,
            fat_content,
            saturated_fat_content,
            cholesterol_content,
            sodium_content,
            carb_content,
            fiber_content,
            sugar_content,
            protein_content
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
            None,
            nutrition,
            servings,
            recipe_yield,
            instructions
        )
        self.__recipes.append(recipe)
        author.add_recipe(recipe)
        category_obj.add_recipe(recipe)

    def get_recipes(self):
        return self.__recipes

    def get_categories(self):
        return list(self.__categories.values())

    def get_authors(self):
        return list(self.__authors.values())

if __name__ == "__main__":
    csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipe_detail.csv')
    reader = CSVDataReader(csv_file_path)
    reader.read_csv_file()
    recipes = reader.get_recipes()

