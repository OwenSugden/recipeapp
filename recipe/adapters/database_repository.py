from abc import ABC
from typing import List, Type, Optional

from sqlalchemy import func
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from recipe.adapters.orm import users_table, favourites_table, reviews_table
from recipe.adapters.repository import AbstractRepository

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
                existing_author = scm.session.query(Author).filter(Author._Author__id == author.id).first()
                if not existing_author:
                    scm.session.add(author)
            scm.commit()

    def get_author_by_id(self, author_id: int):
        author = None
        try:
            query = self._session_cm.session.query(Author).filter(
                Author._Author__id == author_id)
            author = query.one()
        except NoResultFound:
            print(f'Author {author_id} was not found')

        return author

    def get_authors(self) -> List[Author]:
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
                    existing_author = scm.session.query(Author).filter(Author._Author__id == author.id).first()
                    if not existing_author:
                        scm.session.add(author)
            scm.commit()

    # end region

    # region Category_data Methods to manage Categories
    def add_category(self, category: Category):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if category already exists
                existing_category = scm.session.query(Category).filter(Category._Category__id == category.id).first()
                if not existing_category:
                    scm.session.add(category)
            scm.commit()

    def get_category_by_id(self, category_id: int):
        category = None
        try:
            query = self._session_cm.session.query(Category).filter(
                Category._Category__id == category_id)
            category = query.one()
        except NoResultFound:
            print(f'Author {category_id} was not found')

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
                    existing_category = scm.session.query(Category).filter(Category._Category__id == category.id).first()
                    if not existing_category:
                        scm.session.add(category)
            scm.commit()

    # end region

    # region Favourite_data Methods to manage Favourites
    def add_favourite(self, favourite: Favourite):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if favourite already exists for this user AND recipe
                existing_favourite = (
                    scm.session.query(Favourite)
                    .filter(
                        Favourite._Favourite__user_id == favourite.user_id,
                        Favourite._Favourite__recipe_id == favourite.recipe_id,
                    )
                    .first()
                )

                if not existing_favourite:
                    scm.session.add(favourite)

            scm.commit()

    def remove_favourite(self, user_id: int, recipe_id: int):
        with self._session_cm as scm:
            fav = (scm.session.query(Favourite)
                .filter(
                    Favourite._Favourite__user_id == user_id,
                    Favourite._Favourite__recipe_id == recipe_id,
                )
                .one_or_none()
            )
            scm.session.delete(fav)
            scm.commit()

    def get_favourites_for_user(self, user_id: str):
        favourites = (self._session_cm.session.query(Favourite)
                      .filter(Favourite._Favourite__user_id == user_id)
                      ).all()
        return favourites

    def get_new_favourite_id(self) -> int:
        favourite_id = self._session_cm.session.query(func.max(favourites_table.c.id)).one()[0]
        if favourite_id is None:
            favourite_id = 1
        else:
            favourite_id += 1
        return favourite_id

    # endregion

    # region Nutrition_data Methods to manage Nutrition
    def add_nutrition(self, nutrition: Nutrition):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if nutrition already exists
                existing_nutrition = scm.session.query(Nutrition).filter(Nutrition._Nutrition__id == nutrition.id).first()
                if not existing_nutrition:
                    scm.session.add(nutrition)
            scm.commit()

    def get_nutrition_by_id(self, nutrition_id: int):
        nutrition = None
        try:
            query = self._session_cm.session.query(Nutrition).filter(
                Nutrition._Nutrition__id == nutrition_id)
            nutrition = query.one()
        except NoResultFound:
            print(f'Nutrition {nutrition_id} was not found')

        return nutrition

    def get_nutritions(self) -> List[Nutrition]:
        nutritions = self._session_cm.session.query(Nutrition).all()
        return nutritions

    def add_multiple_nutritions(self, nutritions: List[Nutrition]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for nutrition in nutritions:
                    # Check if nutrition already exists
                    existing_nutrition = scm.session.query(Nutrition).filter(Nutrition._Nutrition__id == nutrition.id).first()
                    if not existing_nutrition:
                        scm.session.add(nutrition)
            scm.commit()

    # endregion

    # region Recipe_data Methods to manage Recipes
    def add_recipe(self, recipe: Recipe):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if recipe already exists
                existing_recipe = scm.session.query(Recipe).filter(Recipe._Recipe__id == recipe.id).first()
                if not existing_recipe:
                    scm.session.add(recipe)
            scm.commit()

    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        recipe = None
        try:
            query = self._session_cm.session.query(Recipe).filter(
                Recipe._Recipe__id == recipe_id)
            recipe = query.one()
        except NoResultFound:
            print(f'Recipe {recipe_id} was not found')

        return recipe

    def get_recipes(self) -> List[Recipe]:
        recipes = self._session_cm.session.query(Recipe).all()
        return recipes

    def get_number_of_recipes(self) -> int:
        num_recipes = self._session_cm.session.query(Recipe).count()
        return num_recipes

    def get_recipes_by_name(self, name: str) -> List[Recipe]:
        try:
            with self._session_cm as scm:
                searched_recipes = scm.session.query(Recipe).filter(
                    func.lower(Recipe._Recipe__name).like(f'%{name.lower().strip()}%')
                ).all()

            if not searched_recipes:
                print(f'No recipes found containing the name {name}.')
                return []

        except Exception as e:
            print(f"An error occurred while searching for recipes by name: {e}")
            return []

        return searched_recipes

    def get_recipes_by_author(self, author: str) -> List[Recipe]:
        try:
            with self._session_cm as scm:
                searched_recipes = (scm.session.query(Recipe).join(Recipe._Recipe__author)
                    .filter(Author._Author__name.ilike(f"%{author}%"))
                    ).all()

            if not searched_recipes:
                print(f'No recipes found with author {author}.')
                return []

        except Exception as e:
            print(f"An error occurred while searching for recipes by author: {e}")
            return []

        return searched_recipes

    def get_recipes_by_category(self, category: str) -> List[Recipe]:
        try:
            with self._session_cm as scm:
                searched_recipes = (scm.session.query(Recipe).join(Recipe._Recipe__category)
                                    .filter(Category._Category__name.ilike(f"%{category}%"))
                                    ).all()

            if not searched_recipes:
                print(f'No recipes found with category {category}.')
                return []

        except Exception as e:
            print(f"An error occurred while searching for recipes by category: {e}")
            return []

        return searched_recipes


    def add_multiple_recipes(self, recipes: List[Recipe]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for recipe in recipes:
                    scm.session.add(recipe)
            scm.commit()

    # endregion

    # region Review data Methods to manage Reviews
    def add_review(self, review: Review):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if review already exists
                existing_review = scm.session.query(Review).filter(Review._Review__user_id == review.user_id).first()
                if not existing_review:
                    scm.session.add(review)

            scm.commit()

    def remove_review(self, user_id: int, review_id: int):
        with self._session_cm as scm:
            review = scm.session.get(Review, review_id)
            if review is not None and review._Review__user_id == user_id:
                scm.session.delete(review)
                scm.commit()

    def get_reviews_with_usernames_for_recipe(self, recipe_id: int):
        rows = (
            self._session_cm.session.query(Review, User._User__username)
            .join(User, Review._Review__user_id == User._User__id)
            .filter(Review._Review__recipe_id == recipe_id)
            .all()
        )

        return [(review, username) for review, username in rows]

    def get_reviews_and_recipes_for_user(self, user_id: int):
        rows = (
            self._session_cm.session.query(Review, Recipe)
            .join(Recipe, Review._Review__recipe_id == Recipe._Recipe__id)
            .filter(Review._Review__user_id == user_id)
            .all()
        )
        return rows

    def get_reviews_for_user(self, user_id: int):
        reviews = (self._session_cm.session.query(Review)
                      .filter(Review._Review__user_id == user_id)
                      ).all()
        return reviews

    def get_reviews_for_recipe(self, recipe_id: int):
        reviews = (self._session_cm.session.query(Review)
                   .filter(Review._Review__recipe_id == recipe_id)
                   ).all()
        return reviews

    def get_new_review_id(self) -> int:
        review_id = self._session_cm.session.query(func.max(reviews_table.c.id)).one()[0]
        if review_id is None:
            review_id = 1
        else:
            review_id += 1
        return review_id

    def get_average_rating(self, recipe_id: int):
        ratings = (self._session_cm.session.query(Review._Review__rating)
                .filter(Review._Review__recipe_id == recipe_id)
                .all())

        if not ratings:
            return 0.0

        rating_values = [r[0] for r in ratings]
        return round(sum(rating_values) / len(rating_values), 1)

    # endregion

    # region User methods
    def add_user(self, user: User):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                # Check if user already exists
                existing_user = scm.session.query(User).filter(User._User__id == user.id).first()
                if not existing_user:
                    scm.session.add(user)
            scm.commit()

    def get_user_by_id(self, user_id: int) -> User | None:
        user = None
        try:
            query = self._session_cm.session.query(User).filter(
                User._User__id == user_id)
            user = query.one()
        except NoResultFound:
            print(f'User {user_id} was not found')
        return user

    def get_user(self, username: str) -> User | None:
        user = None
        try:
            query = self._session_cm.session.query(User).filter(User._User__username == username )
            user = query.one()
        except NoResultFound:
            print(f'User with username {username} was not found')
        return user

    def get_new_user_id(self) -> int:
        user_id = self._session_cm.session.query(func.max(users_table.c.id)).one()[0]
        if user_id is None:
            user_id = 1
        else:
            user_id += 1
        return user_id

    # endregion

    # region RecipeImage Methods
    def add_recipe_image(self, recipe_image: RecipeImage):
        with self._session_cm as scm:
            scm.session.add(recipe_image)
            scm.commit()

    def get_recipe_image(self, recipe_id: int, position: int):
        recipe_image = None
        try:
            recipe_image = (
            self._session_cm.session.query(RecipeImage)
            .filter(
                RecipeImage._RecipeImage__recipe_id == recipe_id,
                RecipeImage._RecipeImage__position == position,
            )
            .order_by(RecipeImage._RecipeImage__id.asc())
            .first()
        )
        except NoResultFound:
            print(f'Recipe_image with Recipe {recipe_id} and Position {position} was not found')

        return recipe_image

    def get_recipe_images(self):
        recipe_images = self._session_cm.session.query(RecipeImage).all()
        return recipe_images

    def add_multiple_recipe_images(self, recipe_images: List[RecipeImage]):
        with self._session_cm as scm:
            for recipe_image in recipe_images:
                scm.session.add(recipe_image)
            scm.commit()

    # endregion

    # region RecipeIngredient Methods
    def add_recipe_ingredient(self, recipe_ingredient: RecipeIngredient):
        with self._session_cm as scm:
            scm.session.add(recipe_ingredient)
            scm.commit()

    def get_recipe_ingredient(self, recipe_id: int, position: int):
        recipe_ingredient = None
        try:
            recipe_ingredient = (
                self._session_cm.session.query(RecipeIngredient)
                .filter(
                    RecipeIngredient._RecipeIngredient__recipe_id == recipe_id,
                    RecipeIngredient._RecipeIngredient__position == position,
                )
                .order_by(RecipeIngredient._RecipeIngredient__id.asc())
                .first()
            )
        except NoResultFound:
            print(f"Recipe_ingredient with Recipe {recipe_id} and Position {position} was not found")
        return recipe_ingredient

    def get_recipe_ingredients(self) -> List[RecipeIngredient]:
        recipe_ingredients = self._session_cm.session.query(RecipeIngredient).all()
        return recipe_ingredients

    def add_multiple_recipe_ingredients(self, recipe_ingredients: List[RecipeIngredient]):
        with self._session_cm as scm:
            for ri in recipe_ingredients:
                scm.session.add(ri)
            scm.commit()

    # endregion

    # region RecipeInstruction Methods
    def add_recipe_instruction(self, recipe_instruction: RecipeInstruction):
        with self._session_cm as scm:
            scm.session.add(recipe_instruction)
            scm.commit()

    def get_recipe_instruction(self, recipe_id: int, position: int):
        recipe_instruction = None
        try:
            recipe_instruction = (
                self._session_cm.session.query(RecipeInstruction)
                .filter(
                    RecipeInstruction._RecipeInstruction__recipe_id == recipe_id,
                    RecipeInstruction._RecipeInstruction__position == position,
                )
                .order_by(RecipeInstruction._RecipeInstruction__id.asc())
                .first()
            )
        except NoResultFound:
            print(f"Recipe_instruction with Recipe {recipe_id} and Position {position} was not found")
        return recipe_instruction

    def get_recipe_instructions(self) -> List[RecipeInstruction]:
        recipe_instructions = self._session_cm.session.query(RecipeInstruction).all()
        return recipe_instructions

    def add_multiple_recipe_instructions(self, recipe_instructions: List[RecipeInstruction]):
        with self._session_cm as scm:
            for rins in recipe_instructions:
                scm.session.add(rins)
            scm.commit()

    # endregion
