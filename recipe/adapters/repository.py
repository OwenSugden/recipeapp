import abc
from typing import List

from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.user import User

repo_instance = None

class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_recipe(self, recipe: Recipe):
        """ Adds a Recipe to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_recipes(self) -> List[Recipe]:
        """ Returns all Recipes in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_recipe(self):
        """ Returns the number of Recipes in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        """ Returns the Recipe with the given id from the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None. """
        raise NotImplementedError
