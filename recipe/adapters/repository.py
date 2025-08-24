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
        raise NotImplementedError()

    @abc.abstractmethod
    def get_recipe(self) -> List[Recipe]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_number_of_recipes(self) -> List[int]:
        raise NotImplementedError()