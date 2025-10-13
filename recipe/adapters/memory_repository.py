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
        self.__reviews = list()
        self.__users = list()
        self.__nutritions = list()
        self.__recipe_images = list()
        self.__recipe_ingredients = list()
        self.__recipe_instructions = list()
        self._next_user_id = 1
        self._next_category_id = 1

    # region Author_data
    def add_author(self, author: Author):
        self._validate_author(author)
        self.__authors.append(author)

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
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance")
        if category.id is None:
            category._Category__id = self._next_category_id
            self._next_category_id += 1
        self._validate_category(category)
        self.__categories.append(category)

    def get_categories(self) -> List[Category]:
        return self.__categories

    def get_number_of_categories(self) -> int:
        return len(self.__categories)

    def add_multiple_categories(self, categories: List[Category]):
        for category in categories:
            self.add_category(category)

    # endregion
    def add_favourite(self, user: User, recipe: Recipe):
        pass

    def remove_favourite(self, user: User, recipe: Recipe):
        pass

    def get_favourite_for_user(self, page: int, page_size: int, user: User) -> list[Recipe]:
        pass

    def is_favourite(self, user_name: str, recipe_id: int):
        return Favourite(user_name, recipe_id) in self.__favourites

    # endregion

    #region Nutrition data Methods to manage Nutrition
    def add_nutrition(self, nutrition: Nutrition):
        self.__nutritions.append(nutrition)

    def add_multiple_nutritions(self, nutritions: List[Nutrition]):
        for nutrition in nutritions:
            self.add_nutrition(nutrition)

    # endregion

    # region Recipe_data Methods to manage Recipes
    def add_recipe(self, recipe: Recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("Expected a Recipe instance")
        self._validate_recipe(recipe)
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
        """
        Adds multiple Recipes to the repository after validating them.
        """
        for recipe in recipes:
            if not isinstance(recipe, Recipe):
                raise TypeError("Expected a Recipe instance")
            self._validate_recipe(recipe)
            self.__recipes.append(recipe)

    # end region

    # region Review data Methods to manage Reviews
    def add_review(self, user: User, review: Review):
        pass

    def get_reviews(self) -> list[Review]:
        pass

    def get_user_reviews(self) -> list[Review]:
        pass

    def get_recipe_reviews(self) -> list[
        Review]:
        pass

    def get_review_by_id(self, review_id: int) -> Review | None:
        pass

    # endregion

    # region User data Methods to manage Users
    def add_user(self, user: User):
        if not isinstance(user, User):
            raise TypeError("Expected a User instance")
        self._validate_recipe(user)
        insort_left(self.__users, user)
        self.__recipes_index[user.id] = user


    def get_user_by_id(self, user_id: int) -> User | None:
        for user in self.__users:
            if user.id == user_id:
                return user
        return None

    def get_user_by_name(self, username: str) -> User | None:
        for user in self.__users:
            if user.username == username:
                return user
        return None

    # endregion

    def add_recipe_image(self, recipe_image: RecipeImage):
        self.__recipe_images.append(recipe_image)

    def add_multiple_recipe_images(self, recipe_images: List[RecipeImage]):
        for recipe_image in recipe_images:
            self.__recipe_images.append(recipe_image)

    def get_recipe_images(self, recipe_id: int) -> List[RecipeImage]:
        recipe_images = []
        for recipe_image in self.__recipe_images:
            if recipe_image.recipe_id == recipe_id:
                recipe_images.append(recipe_image)

        return recipe_images

    # endregion

    def add_recipe_ingredient(self, recipe_ingredient: RecipeIngredient):
        self.__recipe_ingredients.append(recipe_ingredient)

    def add_multiple_recipe_ingredients(self, recipe_ingredients: List[RecipeIngredient]):
        for recipe_ingredient in recipe_ingredients:
            self.__recipe_ingredients.append(recipe_ingredient)

    def get_recipe_ingredients(self, recipe_id: int) -> List[RecipeIngredient]:
        recipe_ingredients = []
        for recipe_ingredient in self.__recipe_ingredients:
            if recipe_ingredient.recipe_id == recipe_id:
                recipe_ingredients.append(recipe_ingredient)
        return recipe_ingredients

    # endregion

    def add_recipe_instruction(self, recipe_instruction: RecipeInstruction):
        self.__recipe_instructions.append(recipe_instruction)

    def add_multiple_recipe_instructions(self, recipe_instructions: List[RecipeInstruction]):
        for recipe_instruction in recipe_instructions:
            self.__recipe_instructions.append(recipe_instruction)

    def get_recipe_instructions(self, recipe_id: int) -> List[RecipeInstruction]:
        recipe_instructions = []
        for recipe_instruction in self.__recipe_instructions:
            if recipe_instruction.recipe_id == recipe_id:
                recipe_instructions.append(recipe_instruction)
        return recipe_instructions

    # endregion

    def _validate_author(self, author: Author):
        if not isinstance(author, Author):
            raise TypeError("Expected an Author instance")
        if author in self.__authors:
            raise FileExistsError(
                f"Author {author.name} already exists in repository")
        if not author.name:
            raise ValueError("Author name cannot be empty")
        if not isinstance(author.name, str):
            raise TypeError("Author name must be a string")
        if author.id < 0:
            raise ValueError("Author ID must be a non-negative integer")
        if not isinstance(author.recipes, list) or not all(
                isinstance(recipe, Recipe) for recipe in author.recipes):
            raise TypeError(
                "Author recipes must be a list of Recipe instances")
        return

    def _validate_category(self, category: Category):
        if category in self.__categories:
            raise FileExistsError(
                f"Category {category.name} already exists in repository")
        if not category.name:
            raise ValueError("Category name cannot be empty")
        if not isinstance(category.name, str):
            raise TypeError("Category name must be a string")
        return

    def _validate_recipe(self, recipe: Recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("Expected a Recipe instance")
        if recipe.author not in self.__authors:
            raise ValueError(
                f"Author {recipe.author.name} not found in repository")
        if recipe.category not in self.__categories:
            raise ValueError(
                f"Category {recipe.category.name} not found in repository")
        if any(r.id == recipe.id for r in self.__recipes):
            raise FileExistsError(
                f"Recipe with ID {recipe.id} already exists in repository")
        if recipe.rating is not None:
            if not (0 <= recipe.rating <= 5):
                raise ValueError("Rating must be between 0 and 5")
        if not isinstance(recipe.date, datetime):
            raise TypeError("Expected a datetime instance for date")
        if recipe in self.__recipes:
            raise FileExistsError("Recipe already exists in the repository")
        if recipe.id < 0:
            raise ValueError("Recipe ID must be a non-negative integer")
        if not isinstance(recipe.name, str) or not recipe.name:
            raise ValueError("Recipe name must be a non-empty string")
        if not isinstance(recipe.author, Author):
            raise TypeError("Expected an Author instance for author")
        if not isinstance(recipe.category, Category):
            raise TypeError("Expected a Category instance for category")
        if not isinstance(recipe.images, list) or not all(
                isinstance(img, str) for img in recipe.images):
            raise TypeError("Expected a list of strings for images")
        if not isinstance(recipe.ingredients, list) or not all(
                isinstance(ing, str) for ing in recipe.ingredients):
            raise TypeError("Expected a list of strings for ingredients")
        if not isinstance(recipe.ingredient_quantities, list) or not all(
                isinstance(qty, str) for qty in recipe.ingredient_quantities):
            raise TypeError(
                "Expected a list of strings for ingredient quantities")
        if not isinstance(recipe.description, str) or not recipe.description:
            raise ValueError("Recipe description must be a non-empty string")
        if not (isinstance(recipe.rating, float) or recipe.rating is None):
            print(recipe.rating)
            print(type(recipe.rating))
            raise ValueError("Recipe rating must be an float or None")
        return

    def _validate_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Expected a Review instance")
        if review.user not in self.__users:
            raise ValueError(
                f"User {review.user.username} not found in repository")
        if review.recipe not in self.__recipes:
            raise ValueError(
                f"Recipe {review.recipe.name} not found in repository")
        if not (0 <= review.rating <= 5):
            raise ValueError("Rating must be between 0 and 5")
        if not isinstance(review.date, datetime):
            raise TypeError("Expected a datetime instance for date")
        return

    def _validate_user(self, user):
        if user in self.__users:
            raise FileExistsError(
                f"User {user.username} already exists in repository")
        if user.username in [u.username for u in self.__users]:
            raise FileExistsError(
                f"Username {user.username} already exists in repository")
        if not user.username:
            raise ValueError("Username cannot be empty")
        if not isinstance(user.username, str):
            raise TypeError("Username must be a string")
        if not user.password:
            raise ValueError("Password cannot be empty")
        if not isinstance(user.password, str):
            raise TypeError("Password must be a string")
        return

    # endregion