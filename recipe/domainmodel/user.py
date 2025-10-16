from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from recipe.domainmodel.favourite import Favourite
    from recipe.domainmodel.review import Review

class User:
    def __init__(self, user_id: int, username: str, password: str):
        self.__id = user_id
        self.__username = username
        self.__password = password
        self.__favourite_recipes = []
        self.__reviews = []

    def __getattr__(self, name):
        """Ensure private attributes are initialized when accessed via SQLAlchemy"""
        if name == '_User__favourite_recipes':
            if not hasattr(self, '__favourite_recipes'):
                self.__favourite_recipes = []
            return self.__favourite_recipes
        elif name == '_User__reviews':
            if not hasattr(self, '__reviews'):
                self.__reviews = []
            return self.__reviews
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __repr__(self) -> str:
        return f"<User {self.id}: {self.username}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __lt__(self, other) -> bool:
        if not isinstance(other, User):
            raise TypeError("Comparison must be between User instances")
        return self.id < other.id

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def username(self) -> str:
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    @property
    def favourite_recipes(self) -> list["Favourite"]:
        return self.__favourite_recipes

    @property
    def reviews(self) -> list["Review"]:
        return self.__reviews

    def add_favourite_recipe(self, recipe: "Favourite") -> None:
        if not isinstance(recipe, Favourite):
            raise TypeError("Expected a Favourite instance")
        if recipe not in self.__favourite_recipes:
            self.__favourite_recipes.append(recipe)
        else:
            raise ValueError("Recipe already in user_profile's favourites")

    def remove_favourite_recipe(self, recipe: "Favourite") -> None:
        if recipe in self.__favourite_recipes:
            self.__favourite_recipes.remove(recipe)
        else:
            raise ValueError("Recipe not found in user_profile's favourites")

    def add_review(self, review: "Review") -> None:
        from recipe.domainmodel.review import Review
        if not isinstance(review, Review):
            raise TypeError("Expected a Review instance")
        self.__reviews.append(review)

    def remove_review(self, review: "Review") -> None:
        from recipe.domainmodel.review import Review
        if review in self.__reviews:
            self.__reviews.remove(review)
        else:
            raise ValueError("Review not found in user_profile's reviews")

    def check_password(self, password: str) -> bool:
        from werkzeug.security import check_password_hash
        return check_password_hash(self.__password, password)