import abc
from typing import List
from recipe.domainmodel.recipe import Recipe

repo_instance = None

class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_recipe(self, recipe: Recipe):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_recipes(self) -> List[Recipe]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_recipe(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_by_id(self, recipe_id) -> Recipe:
        raise NotImplementedError