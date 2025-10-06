from abc import ABC
from typing import List, Type

from sqlalchemy import func
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.user import User
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe_ingredient import RecipeIngredient
from recipe.domainmodel.recipe_instruction import RecipeInstruction
from recipe.domainmodel.comment import Comment
from recipe.domainmodel.rating import Rating

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

    def get_authors(self, sort_method: str) -> List[Author]:
        authors = self._session_cm.session.query(Author).all()
        return authors

    def get_number_of_authors(self) -> int:
        num_authors = self._session_cm.session.query(Author).count()
        return num_authors

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

    def get_category_by_name(self, name: str) -> Category:
        category = None
        try:
            query = self._session_cm.session.query(Category).filter(
                func.lower(Category.name) == name.strip().lower())
            category = query
        except NoResultFound:
            print(f'Category {name} not found')

        return category

    def get_categories(self) -> List[Category]:
        categories = self._session_cm.session.query(Category).all()
        return categories

    def get_number_of_categories(self) -> int:
        num_categories = self._session_cm.session.query(Category).count()
        return num_categories

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

    # region Recipe_data Methods to manage Recipes

    def add_recipe(self, recipe: Recipe):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if recipe already exists
                existing_recipe = scm.session.query(Recipe).filter(Recipe.id == recipe.id).first()
                if not existing_recipe:
                    scm.session.add(recipe)
            scm.commit()

    def add_multiple_recipes(self, recipes: List[Recipe]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for recipe in recipes:
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

        return recipe

    def get_recipes(self, page: int, page_size: int, sort_method: str) -> List[Recipe]:
        query = self._session_cm.session.query(Recipe)

        # Apply pagination
        start_index = (page - 1) * page_size
        recipes = query.offset(start_index).limit(page_size).all()

        # Populate all recipes with related data
        for recipe in recipes:
            self._populate_recipe_data(recipe)

        return recipes

    def get_all_recipes(self, sort_method: str = 'name') -> List[Recipe]:
        query = self._session_cm.session.query(Recipe)

        recipes = query.all()
        # Populate all recipes with related data
        for recipe in recipes:
            self._populate_recipe_data(recipe)
        return recipes

    def get_recipes_with_category_filter(self, page: int, page_size: int, sort_method: str,
                                         category_name: str = None) -> tuple[List[Recipe], int]:
        pass

    def search_recipes(self, search_type: str, search_term: str, page: int, page_size: int, sort_method: str,
                       category_name: str = None) -> tuple[List[Recipe], int]:
        pass

    def get_number_of_recipes(self) -> int:
        num_recipes = self._session_cm.session.query(Recipe).count()
        return num_recipes

    def get_recipes_by_name(self, page: int, page_size: int, name: str, sort_method: str = 'name') -> List[Recipe]:
        pass

    def get_recipes_by_date(self, page: int, page_size: int, target_date: str, sort_method: str = 'name') -> List[
        Recipe]:
        pass

    def get_recipes_by_author(self, page: int, page_size: int, author: Author, sort_method: str = 'name') -> List[
        Recipe]:
        pass

    def get_recipes_by_category(self, page: int, page_size: int, category: Category, sort_method: str = 'name') -> List[
        Recipe]:
        pass

    # endregion

    # region Comment_data Methods to manage Comments

    def add_comment(self, comment: Comment):
        with self._session_cm as scm:
            scm.session.merge(comment)
            scm.commit()

    def get_comments(self):
        pass

    def get_comments_for_recipe(self, recipe_id: int):
        pass

    # endregion

    # region Rating_data Methods to manage Ratings

    def add_rating(self, rating: Rating):
        with self._session_cm as scm:
            scm.session.merge(rating)
            scm.commit()

    def get_ratings_for_recipe(self, recipe_id: int) -> list[Rating]:
        pass

    # endregion

    # region Favourite_data Methods to manage Favourites
    def add_favourite(self, favourite: Favourite):
        with self._session_cm as scm:
            scm.session.merge(favourite)
            scm.commit()

    def remove_favourite(self, favourite: Favourite):
        pass

    def get_favourites_for_user(self, user_name: str):
        pass

    def is_favourite(self, user_name: str, recipe_id: int):
        pass

    # endregion

    # region Nutrition_data Methods to manage Nutrition
    def get_nutritions(self, sorting: bool = False) -> List[Type[Nutrition]]:
        pass

    def get_nutrition(self, nutrition_id: int) -> Nutrition:
       pass

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

    def get_number_of_nutritions(self) -> List[Nutrition]:
        pass

    def get_nutritions_for_recipe(self, recipe_id: int) -> List[Nutrition]:
        pass

    def get_number_of_nutritions_for_recipe(self, recipe_id: int) -> int:
        pass

    # endregion

    def _populate_recipe_data(self, recipe: Recipe):
        """
        Populate a Recipe object with related data (images, ingredients, instructions)
        to maintain consistent domain model interface between memory and database repositories.
        """
        if recipe is None:
            return

        # Use the same session context
        with self._session_cm as scm:
            self._populate_recipe_data_in_session(recipe, scm.session)

    def _populate_recipe_data_in_session(self, recipe: Recipe, session):
        """
        Populate a Recipe object with related data using the provided session.
        """
        if recipe is None:
            return

        # Load and populate images
        recipe_images = session.query(RecipeImage).filter(
            RecipeImage._RecipeImage__recipe_id == recipe.id
        ).order_by(RecipeImage._RecipeImage__position).all()

        if recipe_images:
            image_urls = [img.url for img in recipe_images]
            recipe._Recipe__images = image_urls
        else:
            print(f"DEBUG: No images found for recipe {recipe.id}")

        # TODO: Load and populate ingredients

        # TODO: Load and populate instructions

    # region RecipeImage Methods
    def add_recipe_image(self, recipe_image: RecipeImage):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if RecipeImage already exists
                existing_recipe_image = scm.session.query(RecipeImage).filter(RecipeImage.id == recipe_image.id).first()
                if not existing_recipe_image:
                    scm.session.add(recipe_image)
            scm.commit()

    def add_multiple_recipe_images(self, recipe_images: List[RecipeImage]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for recipe_image in recipe_images:
                    # Check if nutrition already exists
                    existing_recipe_image = scm.session.query(RecipeImage).filter(RecipeImage.id == recipe_image.id).first()
                    if not existing_recipe_image:
                        scm.session.add(recipe_image)
            scm.commit()

    def get_recipe_images(self, recipe_id: int) -> List[RecipeImage]:
        pass

    # endregion

    # region RecipeIngredient Methods
    def add_recipe_ingredient(self, recipe_ingredient: RecipeIngredient):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if RecipeImage already exists
                existing_recipe_ingredient = scm.session.query(RecipeIngredient).filter(RecipeIngredient.id == recipe_ingredient.id).first()
                if not existing_recipe_ingredient:
                    scm.session.add(recipe_ingredient)
            scm.commit()

    def add_multiple_recipe_ingredients(self, recipe_ingredients: List[RecipeIngredient]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for recipe_ingredient in recipe_ingredients:
                    # Check if RecipeImage already exists
                    existing_recipe_image = scm.session.query(RecipeIngredient).filter(RecipeIngredient.id == recipe_ingredient.id).first()
                    if not existing_recipe_image:
                        scm.session.add(recipe_ingredient)
            scm.commit()

    def get_recipe_ingredients(self, recipe_id: int) -> List[RecipeIngredient]:
        pass

    # endregion

    # region RecipeInstruction Methods
    def add_recipe_instruction(self, recipe_instruction: RecipeInstruction):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if RecipeInstruction already exists
                existing_recipe_instruction = scm.session.query(RecipeInstruction).filter(RecipeInstruction.id == recipe_instruction.id).first()
                if not existing_recipe_instruction:
                    scm.session.add(recipe_instruction)
            scm.commit()

    def add_multiple_recipe_instructions(self, recipe_instructions: List[RecipeInstruction]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for recipe_instruction in recipe_instructions:
                    # Check if RecipeImage already exists
                    existingrecipe_instruction = scm.session.query(RecipeInstruction).filter(RecipeInstruction.id == recipe_instructions.id).first()
                    if not existingrecipe_instruction:
                        scm.session.add(recipe_instructions)
            scm.commit()

    def get_recipe_instructions(self, recipe_id: int) -> List[RecipeInstruction]:
        pass

    # endregion

    # region User methods

    def add_user(self, user: User):
        pass

    def get_user(self, user_name) -> User:
        pass