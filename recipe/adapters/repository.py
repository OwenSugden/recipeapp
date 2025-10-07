import abc
from typing import List, Optional

from recipe.domainmodel.author import Author
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.recipe import Recipe
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
    def get_authors(self) -> list[Author]:
        """Returns a list of all Authors in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_authors(self) -> int:
        """Returns the number of Authors in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_author_by_name(self, name: str) -> Author | None:
        """
        Returns the Author with the specified name from the repository.
        If there is no Author with the given name, this method returns None.
        """
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
    def get_categories(self) -> List[Category]:
        """Returns a list of all Categories in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_categories(self) -> int:
        """Returns the number of Categories in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_category_by_name(self, name: str) -> Category | None:
        """
        Returns the Category with the specified name from the repository.
        If there is no Category with the given name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_categories(self, categories: List[Category]):
        """Adds multiple Categories to the repository."""
        raise NotImplementedError

    # endregion

    # region Favourites data Methods to manage Favourites
    # Methods to manage Favourites

    @abc.abstractmethod
    def add_favourite(self, user: User, recipe: Recipe):
        """Adds a Recipe to the User's list of favourite Recipes."""
        raise NotImplementedError

    @abc.abstractmethod
    def remove_favourite(self, user: User, recipe: Recipe):
        """Removes a Recipe from the User's list of favourite Recipes."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_favourite_for_user(self, page: int, page_size: int, user: User) -> list[Recipe]:
        """Returns a list of the User's favourite Recipes."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_favourite(self, user: User, recipe: Recipe) -> bool:
        raise NotImplementedError

    # endregion

    # region Nutrition data Methods to manage Nutrition

    @abc.abstractmethod
    def add_nutrition(self, nutrition: Nutrition):
        """Adds a Nutrition to the repository."""
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

    # TODO implement the sorting and filtering, searching here

    @abc.abstractmethod
    def add_multiple_recipes(self, recipe: List[Recipe]):
        """Adds multiple Recipes to the repository."""
        raise NotImplementedError

    # endregion

    # region Review_data Methods to manage Reviews
    # Methods to manage Reviews

    @abc.abstractmethod
    def add_review(self, user: User, review: Review):
        """Adds a Review to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self, page: int, page_size: int, sort_method: str) -> list[Review]:
        """
        Returns a list of all Reviews in the repository, sorted by sort_method.
        sort_method can be: date, rating, or user.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_reviews(self, page: int, page_size: int, user: User, sort_method: str) -> list[Review]:
        """
        Returns a list of Reviews submitted by the specified User, sorted by sort_method.
        sort_method can be: date, rating, or recipe.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_reviews(self, page: int, page_size: int, recipe: Recipe, sort_method: str) -> list[
        Review]:
        """
        Returns a list of Reviews for the specified Recipe, sorted by sort_method.
        sort_method can be: date, rating, or user.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_review_by_id(self, review_id: int) -> Review | None:
        """
        Returns the Review with the specified review_id from the repository.
        If there is no Review with the given review_id, this method returns None.
        """
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

    @abc.abstractmethod
    def get_user_by_name(self, username: str) -> User | None:
        """
        Returns the User with the provided username from the repository.
        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    # endregion

