import csv
import re
import ast

from datetime import datetime
from bisect import insort_left
from tkinter import Image
from typing import List
from pathlib import Path

from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe_ingredient import RecipeIngredient
from recipe.domainmodel.recipe_instruction import RecipeInstruction
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User

from recipe.adapters.repository import AbstractRepository

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__authors = list()
        self.__categories = list()
        self.__recipes = list()
        self.__recipes_index = dict()
        self.__users = list()
        self.__reviews = dict()
        self.__favourites = dict()
        self.__nutritions = list()
        self.__recipe_images = list()
        self.__recipe_ingredients = list()
        self.__recipe_instructions = list()
        self.__current_user_id = 0
        self.__current_favourite_id = 0
        self.__current_review_id = 0


    # region Author_data
    def add_author(self, author: Author):
        self.__authors.append(author)

    def get_author_by_id(self, author_id: int):
        for author in self.__authors:
            if author.id == author_id:
                return author
        return None

    def get_authors(self) -> list[Author]:
        return self.__authors

    def get_number_of_authors(self) -> int:
        return len(self.__authors)

    def add_multiple_authors(self, authors: List[Author]):
        for author in authors:
            self.add_author(author)

    # endregion

    # region Category_data Methods to manage Categories
    def add_category(self, category: Category):
        self.__categories.append(category)

    def get_category_by_id(self, category_id: int):
        for category in self.__categories:
            if category.id == category_id:
                return category
        return None

    def get_categories(self) -> List[Category]:
        return self.__categories

    def get_number_of_categories(self) -> int:
        return len(self.__categories)

    def add_multiple_categories(self, categories: List[Category]):
        for category in categories:
            self.add_category(category)

    # endregion

    # region Favourite_data Methods to manage Favourites
    def add_favourite(self, favourite: Favourite):
        user_id = favourite.user_id

        # If this user_id doesn't exist yet, create a new list for it
        if user_id not in self.__favourites:
            self.__favourites[user_id] = []

        if not any(f.recipe_id == favourite.recipe_id for f in self.__favourites[user_id]):
            self.__favourites[user_id].append(favourite)

    def remove_favourite(self, user_id: int, recipe_id: int):
        # Check if this user has any favourites stored
        if user_id in self.__favourites:
            favourites_list = self.__favourites[user_id]

            # Find the favourite to remove
            for favourite in list(favourites_list):  # iterate over a copy
                if favourite.recipe_id == recipe_id:
                    favourites_list.remove(favourite)
                    break

            if not favourites_list:
                del self.__favourites[user_id]

    def get_favourites_for_user(self, user_id: int):
        if user_id in self.__favourites:
            favourites_list = self.__favourites[user_id]
            return favourites_list
        return []

    def get_new_favourite_id(self) -> int:
        favourite_id = self.__current_favourite_id
        self.__current_favourite_id += 1
        return favourite_id

    # endregion

    #region Nutrition data Methods to manage Nutrition
    def add_nutrition(self, nutrition: Nutrition):
        self.__nutritions.append(nutrition)

    def get_nutrition_by_id(self, nutrition_id: int):
        for nutrition in self.__nutritions:
            if nutrition.id == nutrition_id:
                return nutrition
        return None

    def get_nutritions(self) -> List[Nutrition]:
        return self.__nutritions

    def add_multiple_nutritions(self, nutritions: List[Nutrition]):
        for nutrition in nutritions:
            self.add_nutrition(nutrition)

    # endregion

    # region Recipe_data Methods to manage Recipes
    def add_recipe(self, recipe: Recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("Expected a Recipe instance")
        insort_left(self.__recipes, recipe)
        self.__recipes_index[recipe.id] = recipe

    def get_recipe_by_id(self, recipe_id):
        for recipe in self.__recipes:
            if recipe.id == recipe_id:
                return recipe
        return None

    def get_recipes(self) -> list[Recipe]:
        return self.__recipes

    def get_number_of_recipes(self) -> int:
        return len(self.__recipes)

    def get_recipes_by_name(self, name: str) -> List[Recipe]:
        searched_recipes = [recipe for recipe in self.__recipes if name in recipe.name]
        return searched_recipes

    def get_recipes_by_category(self, category: str) -> List[Recipe]:
        searched_recipes = [recipe for recipe in self.__recipes if category in recipe.category.name]
        return searched_recipes

    def get_recipes_by_author(self, author: str) -> List[Recipe]:
        searched_recipes = [recipe for recipe in self.__recipes if author in recipe.author.name]
        return searched_recipes

    def add_multiple_recipes(self, recipes: List[Recipe]):
        for recipe in recipes:
            if not isinstance(recipe, Recipe):
                raise TypeError("Expected a Recipe instance")
            self.__recipes.append(recipe)

    # end region

    # region Review data Methods to manage Reviews
    def add_review(self, review: Review):
        user_id = review.user_id

        # If this user_id doesn't exist yet, create a new list for it
        if user_id not in self.__reviews:
            self.__reviews[user_id] = []
            self.__reviews[user_id].append(review)

    def remove_review(self, user_id: int, review_id: int):
        reviews_list = self.__reviews.get(user_id)
        if not reviews_list:
            return

        # find by id, then delete
        for i, r in enumerate(reviews_list):
            if r.id == review_id:
                del reviews_list[i]
                break

        if not reviews_list:
            del self.__reviews[user_id]

    def get_reviews_with_usernames_for_recipe(self, recipe_id: int):
        results = []
        for user_id, user_reviews in self.__reviews.items():
            user = next((u for u in self.__users if u.id == user_id), None)
            username = user.username if user else "Unknown"

            for review in user_reviews:
                if review.recipe_id == recipe_id:
                    results.append((review, username))

        return results

    def get_reviews_and_recipes_for_user(self, user_id: int):
        results = []
        user_reviews = self.__reviews.get(user_id, [])
        for review in user_reviews:
            recipe = self.get_recipe_by_id(review.recipe_id)
            if recipe is not None:
                results.append((review, recipe))
        return results

    def get_reviews_for_user(self, user_id: int):
        if user_id in self.__reviews:
            reviews_list = self.__reviews[user_id]
            return reviews_list
        return None

    def get_reviews_for_recipe(self, recipe_id: int):
        reviews_list = []
        for user_reviews in self.__reviews.values():
            for review in user_reviews:
                if review.recipe_id == recipe_id:
                    reviews_list.append(review)
        return reviews_list

    def get_new_review_id(self) -> int:
        review_id = self.__current_review_id
        self.__current_review_id += 1
        return review_id

    def get_average_rating(self, recipe_id: int):
        ratings = []

        for user_reviews in self.__reviews.values():
            for review in user_reviews:
                if review.recipe_id == recipe_id:
                    ratings.append(review.rating)

        if not ratings:
            return 0.0

        return round(sum(ratings) / len(ratings), 1)

    # endregion

    # region User data Methods to manage Users
    def add_user(self, user: User):
        self.__users.append(user)
        print(self.__users)

    def get_user_by_id(self, user_id: int) -> User | None:
        for user in self.__users:
            if user.id == user_id:
                return user
        return None

    def get_user(self, username: str) -> User | None:
        for user in self.__users:
            if user.username == username:
                return user
        return None

    def get_new_user_id(self) -> int:
        user_id = self.__current_user_id
        self.__current_user_id += 1
        return user_id

    # endregion

    # region RecipeImage data Methods to manage RecipeImage
    def add_recipe_image(self, recipe_image: RecipeImage):
        self.__recipe_images.append(recipe_image)

    def get_recipe_image(self, recipe_id: int, position: int):
        for recipeimage in self.__recipe_images:
            if recipeimage.recipe_id == recipe_id and recipeimage.position == position:
                return recipeimage
        return None

    def get_recipe_images(self) -> list[RecipeImage]:
        return self.__recipe_images

    def add_multiple_recipe_images(self, recipe_images: List[RecipeImage]):
        for recipe_image in recipe_images:
            self.__recipe_images.append(recipe_image)

    # endregion

    # region RecipeIngredient data Methods to manage RecipeIngredient
    def add_recipe_ingredient(self, recipe_ingredient: RecipeIngredient):
        self.__recipe_ingredients.append(recipe_ingredient)

    def get_recipe_ingredient(self, recipe_id: int, position: int):
        for recipeingredient in self.__recipe_ingredients:
            if recipeingredient.recipe_id == recipe_id and recipeingredient.position == position:
                return recipeingredient
        return None

    def get_recipe_ingredients(self) -> list[RecipeIngredient]:
        return self.__recipe_ingredients

    def add_multiple_recipe_ingredients(self, recipe_ingredients: List[RecipeIngredient]):
        for recipe_ingredient in recipe_ingredients:
            self.__recipe_ingredients.append(recipe_ingredient)

    # endregion

    # region RecipeIngredient data Methods to manage RecipeIngredient
    def add_recipe_instruction(self, recipe_instruction: RecipeInstruction):
        self.__recipe_instructions.append(recipe_instruction)

    def get_recipe_instruction(self, recipe_id: int, position: int):
        for recipeinstruction in self.__recipe_instructions:
            if recipeinstruction.recipe_id == recipe_id and recipeinstruction.position == position:
                return recipeinstruction
        return None

    def get_recipe_instructions(self) -> list[RecipeInstruction]:
        return self.__recipe_instructions

    def add_multiple_recipe_instructions(self, recipe_instructions: List[RecipeInstruction]):
        for recipe_instruction in recipe_instructions:
            self.__recipe_instructions.append(recipe_instruction)

    # endregion