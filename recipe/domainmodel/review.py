from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from recipe.domainmodel.user import User
    from recipe.domainmodel.recipe import Recipe

class Review:
    def __init__(self, review_id: int, user_id: int, date: datetime, recipe_id: int, rating: float, comment: str):
        self.__id = review_id
        self.__user_id = user_id
        self.__date = date
        self.__recipe_id = recipe_id
        if not (0 <= rating <= 5):
            raise ValueError("Rating must be between 0 and 5")
        else:
            self.__rating = rating
        self.__comment = comment

    def __repr__(self) -> str:
        return f"<Review: User: {self.__user_id}, Recipe: {self.__recipe_id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Review):
            return False
        return self.id == other.id

    def __lt__(self, other) -> bool:
        if not isinstance(other, Review):
            raise TypeError("Comparison must be between Review instances")
        if self.__rating is None:
            return False
        if other.__rating is None:
            return True
        return self.__rating < other.__rating

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def date(self) -> datetime:
        return self.__date

    @property
    def recipe_id(self) -> int:
        return self.__recipe_id

    @property
    def rating(self) -> float:
        return self.__rating

    @property
    def comment(self) -> str:
        return self.__comment

    def update_rating(self, new_rating: float) -> None:
        if not (0 <= new_rating <= 5):
            raise ValueError("Rating must be between 0 and 5")
        self.__rating = new_rating

    def update_comment(self, new_comment: str) -> None:
        self.__comment = new_comment

