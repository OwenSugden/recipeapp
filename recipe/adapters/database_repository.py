from abc import ABC
from typing import List, Type, Optional

from sqlalchemy import func
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from recipe.adapters.repository import AbstractRepository

from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User

# feature 1 test
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self) -> object:
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # region Author_data Methods to manage Authors
    def add_author(self, author: Author):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if author already exists
                existing_author = scm.session.query(Author).filter(Author.id == author.id).first()
                if not existing_author:
                    scm.session.add(author)
            scm.commit()

    def get_authors(self) -> List[Author]:
        authors = self._session_cm.session.query(Author).all()
        return authors

    def get_number_of_authors(self) -> int:
        num_authors = self._session_cm.session.query(Author).count()
        return num_authors

    def get_author_by_name(self, name: str) -> Author | None:
        author = None
        try:
            query = self._session_cm.session.query(Author).filter(
                func.lower(Author.name) == name.strip().lower())
            author = query
        except NoResultFound:
            print(f'Author {name} not found')

        return author

    def add_multiple_authors(self, authors: List[Author]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for author in authors:
                    # Check if author already exists
                    existing_author = scm.session.query(Author).filter(Author.id == author.id).first()
                    if not existing_author:
                        scm.session.add(author)
            scm.commit()

    # end region

    # region Category_data Methods to manage Categories
    def add_category(self, category: Category):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if category already exists
                existing_category = scm.session.query(Category).filter(Category.id == category.id).first()
                if not existing_category:
                    scm.session.add(category)
            scm.commit()

    def get_categories(self) -> List[Category]:
        categories = self._session_cm.session.query(Category).all()
        return categories

    def get_number_of_categories(self) -> int:
        num_categories = self._session_cm.session.query(Category).count()
        return num_categories

    def get_category_by_name(self, name: str) -> Category:
        category = None
        try:
            query = self._session_cm.session.query(Category).filter(
                func.lower(Category.name) == name.strip().lower())
            category = query
        except NoResultFound:
            print(f'Category {name} not found')

        return category

    def add_multiple_categories(self, categories: List[Category]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for category in categories:
                    # Check if category already exists
                    existing_category = scm.session.query(Category).filter(Category.id == category.id).first()
                    if not existing_category:
                        scm.session.add(category)
            scm.commit()

    # end region

    # region Favourite_data Methods to manage Favourites
    def add_favourite(self, user: User, recipe: Recipe):
        pass

    def remove_favourite(self, user: User, recipe: Recipe):
        pass

    def get_favourite_for_user(self, page: int, page_size: int, user: User) -> List[Recipe]:
        pass

    def is_favourite(self, user: User, recipe: Recipe) -> bool:
        with self._session_cm as scm:
            exists = (
                    scm.session.query(Favourite)
                    .filter(
                        Favourite.user == user,
                        Favourite.recipe == recipe,
                    )
                    .first()
                    is not None
            )
            return exists

    # endregion

    # region Nutrition_data Methods to manage Nutrition
    def add_nutrition(self, nutrition: Nutrition):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if nutrition already exists
                existing_nutrition = scm.session.query(Nutrition).filter(Nutrition.id == nutrition.id).first()
                if not existing_nutrition:
                    scm.session.add(nutrition)
            scm.commit()

    def add_multiple_nutritions(self, nutritions: List[Nutrition]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for nutrition in nutritions:
                    # Check if nutrition already exists
                    existing_nutrition = scm.session.query(Nutrition).filter(Nutrition.id == nutrition.id).first()
                    if not existing_nutrition:
                        scm.session.add(nutrition)
            scm.commit()

    # endregion

    # region Recipe_data Methods to manage Recipes
    def add_recipe(self, recipe: Recipe):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if recipe already exists
                existing_recipe = scm.session.query(Recipe).filter(Recipe.id == recipe.id).first()
                if not existing_recipe:
                    scm.session.add(recipe)
            scm.commit()

    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        recipe = None
        try:
            query = self._session_cm.session.query(Recipe).filter(
                Recipe._Recipe__id == recipe_id)
            recipe = query.one()
            # Populate the recipe with related data for consistent domain model interface
            self._populate_recipe_data(recipe)
        except NoResultFound:
            print(f'Recipe {recipe_id} was not found')

    def get_recipes(self) -> list[Recipe]:
        recipes = self._session_cm.session.query(Recipe).all()
        return recipes

    # def get_recipes(self, page: int, page_size: int, sort_method: str) -> List[Recipe]:
    #     query = self._session_cm.session.query(Recipe)
    #
    #     # Apply pagination
    #     start_index = (page - 1) * page_size
    #     recipes = query.offset(start_index).limit(page_size).all()
    #
    #     # Populate all recipes with related data
    #     for recipe in recipes:
    #         self._populate_recipe_data(recipe)
    #
    #     return recipes

    def get_number_of_recipes(self) -> int:
        num_recipes = self._session_cm.session.query(Recipe).count()
        return num_recipes

    def add_multiple_recipes(self, recipes: List[Recipe]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for recipe in recipes:
                    scm.session.add(recipe)
            scm.commit()

        return recipe

    # endregion

    # region Review_data Methods to manage Reviews

    def add_review(self, user: User, review: Review):
        pass

    def get_reviews(self, page: int, page_size: int, sort_method: str) -> list[Review]:
        pass

    def get_user_reviews(self, page: int, page_size: int, user: User, sort_method: str) -> list[Review]:
        pass

    def get_recipe_reviews(self, page: int, page_size: int, recipe: Recipe, sort_method: str) -> list[Review]:
        pass

    def get_recipes_reviewed_by_user(self, page: int, page_size: int, user: User, sort_method: str) -> \
            list[Recipe]:
        pass

    def get_review_by_id(self, review_id: int) -> Review | None:
        pass

    # endregion

    # region User methods
    def add_user(self, user: User):
        pass

    def get_user_by_id(self, user_id: int) -> User | None:
        pass

    def get_user_by_name(self, username: str) -> User | None:
        pass

    # endregion
