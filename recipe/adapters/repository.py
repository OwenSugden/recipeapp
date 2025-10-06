import abc
from typing import List

from recipe.domainmodel.author import Author
from recipe.domainmodel.comment import Comment
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.rating import Rating
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.user import User

repo_instance = None

class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')

class AbstractRepository(abc.ABC):

    # region Author_data Methods to manage Authors
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
    def get_authors(self, sort_method: str) -> list[Author]:
        """Returns a list of all Authors in the repository, sorted by sort_method.

        sort_method can be: name or recipes_count.
        """
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

    # region Category_data Methods to manage Categories
    # Methods to manage Categories

    @abc.abstractmethod
    def add_category(self, category: Category):
        """Adds a Category to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_category_by_name(self, name: str) -> Category | None:
        """
        Returns the Category with the specified name from the repository.
        If there is no Category with the given name, this method returns None.
        """
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

    # region Recipe_data Methods to manage Recipes
    # Methods to manage Recipes

    @abc.abstractmethod
    def add_recipe(self, recipe: Recipe):
        """Adds a Recipe to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_recipes(self, recipe: List[Recipe]):
        """Adds multiple Recipes to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_by_id(self, recipe_id: int) -> Recipe | None:
        """
        Returns Recipe with recipe_id from the repository.
        If there is no Recipe with the given recipe_id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes(self, page: int, page_size: int, sort_method: str) -> List[Recipe]:
        """
        Returns a list of all Recipes in the repository, sorted by sort_method.
        sort_method can be: author, date, name, or rating.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_recipes(self) -> int:
        """Returns the number of Recipes in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_by_name(self, page: int, page_size: int, name: str, sort_method: str = 'name') -> List[Recipe]:
        """
        Returns a list of Recipes that match the given name, sorted by sort_method.
        The sort_method can be: name, date, or rating.
        If there are no Recipes with the given name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_by_date(self, page: int, page_size: int, target_date: str, sort_method: str = 'name') -> List[
        Recipe]:
        """
        Returns a list of Recipes that were published on target_date, sorted by sort_method.
        The sort_method can be: name, date, or rating.
        If there are no Recipes on the given date, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_by_author(self, page: int, page_size: int, author: Author, sort_method: str = 'name') -> List[
        Recipe]:
        """
        Returns a list of Recipes by the specified Author, sorted by sort_method.
        sort_method can be: name, date, or rating.
        If there are no Recipes by the given Author, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_by_category(self, page: int, page_size: int, category: Category, sort_method: str = 'name') -> List[
        Recipe]:
        """
        Returns a list of Recipes in the specified Category, sorted by sort_method.
        The sort_method can be: name, date, or rating.
        If there are no Recipes in the given Category, this method returns an empty list.
        """
        raise NotImplementedError

    # endregion

    # region Comment_data Methods to manage Commments
    # Methods to manage Reviews

    @abc.abstractmethod
    def add_comment(self, comment: Comment):
        raise NotImplementedError

    @abc.abstractmethod
    def get_comments(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_comments_for_recipe(self, recipe_id: int):
        raise NotImplementedError

    # endregion

    # region Rating_data Methods to manage Ratings
    # Methods to manage Ratings

    @abc.abstractmethod
    # In AbstractRepository
    def add_rating(self, rating: Rating):
        raise NotImplementedError

    @abc.abstractmethod
    def get_ratings_for_recipe(self, recipe_id: int) -> list[Rating]:
        """ If there is no User with the given user_name, this method returns None. """
        raise NotImplementedError

    # endregion

    # region User_data Methods to manage Users
    # Methods to manage Users

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.
        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    # endregion

    # region Favourites_data Methods to manage Favourites
    # Methods to manage Favourites

    @abc.abstractmethod
    def add_favourite(self, favourite: Favourite):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_favourite(self, favourite: Favourite):
        raise NotImplementedError

    @abc.abstractmethod
    def get_favourites_for_user(self, user_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def is_favourite(self, user_name: str, recipe_id: int):
        raise NotImplementedError

    # endregion

    # region Nutrition_data Methods to manage Nutrition

    @abc.abstractmethod
    def add_nutrition(self, nutrition: Nutrition):
        """Adds a Nutrition to the repository."""
        raise NotImplementedError

    #endregion

