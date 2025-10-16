import abc
from tkinter import Image
from typing import List, Optional

from recipe.domainmodel.author import Author
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe_ingredient import RecipeIngredient
from recipe.domainmodel.recipe_instruction import RecipeInstruction
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User

repo_instance = None

class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')

class AbstractRepository(abc.ABC):
    # region Author data Methods to manage Authors
    # Methods to manage Authors
    @abc.abstractmethod
    def add_author(self, author: Author):
        """Adds an Author to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_author_by_id(self, author_id: int):
        """Gets an Author from the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_authors(self) -> list[Author]:
        """Returns a list of all Authors in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_authors(self) -> int:
        """Returns the number of Authors in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_authors(self, authors: List[Author]):
        """Adds multiple Authors to the repository."""
        raise NotImplementedError

    #endregion

    # region Category data Methods to manage Categories
    # Methods to manage Categories

    @abc.abstractmethod
    def add_category(self, category: Category):
        """Adds a Category to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_category_by_id(self, category_id: int):
        """Gets a Category from the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_categories(self) -> List[Category]:
        """Returns a list of all Categories in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_categories(self) -> int:
        """Returns the number of Categories in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_categories(self, categories: List[Category]):
        """Adds multiple Categories to the repository."""
        raise NotImplementedError

    # endregion

    # region Favourites data Methods to manage Favourites
    # Methods to manage Favourites
    @abc.abstractmethod
    def add_favourite(self, favourite: Favourite):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_favourite(self, user_id: int, recipe_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_favourites_for_user(self, user_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_new_favourite_id(self) -> int:
        raise NotImplementedError

    # endregion

    # region Nutrition data Methods to manage Nutrition
    # Methods to manage Nutrition
    @abc.abstractmethod
    def add_nutrition(self, nutrition: Nutrition):
        """Adds a Nutrition to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_nutrition_by_id(self, nutrition_id: int):
        """Gets a Nutrition from the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_nutritions(self) -> List[Nutrition]:
        """Returns a list of all Nutritions in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_nutritions(self, nutritions: List[Nutrition]):
        """Adds multiple Nutritions to the repository."""
        raise NotImplementedError

    # endregion

    # region Recipe data Methods to manage Recipes
    # Methods to manage Recipes
    @abc.abstractmethod
    def add_recipe(self, recipe: Recipe):
        """Adds a Recipe to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_by_id(self, recipe_id: int) -> Recipe | None:
        """
        Returns Recipe with recipe_id from the repository.
        If there is no Recipe with the given recipe_id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes(self) -> List[Recipe]:
        """Returns a list of all Recipes in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_recipes(self) -> int:
        """Returns the number of Recipes in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_by_name(self, name: str) -> List[Recipe]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_by_category(self, category: str) -> List[Recipe]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_by_author(self, author: str) -> List[Recipe]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_recipes(self, recipe: List[Recipe]):
        """Adds multiple Recipes to the repository."""
        raise NotImplementedError

    # endregion

    # region Review_data Methods to manage Reviews
    # Methods to manage Reviews
    @abc.abstractmethod
    def add_review(self, review: Review):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_review(self, user_id: int, recipe_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_for_user(self, user_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_for_recipe(self, recipe_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_new_review_id(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_and_recipes_for_user(self, user_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_with_usernames_for_recipe(self, recipe_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_average_rating(self, user_id: int):
        raise NotImplementedError

    # endregion

    # region User_data Methods to manage Users
    # Methods to manage Users

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_id(self, user_id: int) -> User | None:
        """
        Returns User with user_id from the repository.
        If there is no User with the given user_id, this method returns None.
        """
        raise NotImplementedError

    # @abc.abstractmethod
    # def get_user_by_name(self, username: str) -> User | None:
    #     """
    #     Returns the User with the provided username from the repository.
    #     If there is no User with the given username, this method returns None.
    #     """
    #     raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str) -> User | None:
        """
        Returns the User with the provided username from the repository.
        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_new_user_id(self) -> int:
        raise NotImplementedError

    # endregion

    @abc.abstractmethod
    def add_recipe_image(self, recipe_image: RecipeImage):
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_image(self, recipe_id: int, position: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_images(self) -> List[RecipeImage]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_recipe_images(self, recipe_images: List[RecipeImage]):
        """Adds multiple Images to the repository."""
        raise NotImplementedError

    # endregion

    @abc.abstractmethod
    def add_recipe_ingredient(self, recipe_ingredient: RecipeIngredient):
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_ingredient(self, recipe_id: int, position: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_ingredients(self) -> List[RecipeImage]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_recipe_ingredients(self, recipe_ingredients: List[RecipeIngredient]):
        """Adds multiple RecipeIngredients to the repository."""
        raise NotImplementedError

    # endregion

    @abc.abstractmethod
    def add_recipe_instruction(self, recipe_instruction: RecipeInstruction):
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_instruction(self, recipe_id: int, position: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_instructions(self) -> List[RecipeImage]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_recipe_instructions(self, recipe_instructions: List[RecipeInstruction]):
        """Adds multiple RecipeInstructions to the repository."""
        raise NotImplementedError