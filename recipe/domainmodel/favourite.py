from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from recipe.domainmodel.user import User
    from recipe.domainmodel.recipe import Recipe

class Favourite:
    def __init__(self, favourite_id: int, user: "User", recipe: "Recipe", date=None):
        from datetime import datetime
        self.__id = favourite_id
        self.__user = user
        self.__recipe = recipe
        self.__date = date if date is not None else datetime.now()

    def __repr__(self):
        return f"<Favourite: User={self.user}, Recipe={self.__recipe}>"

    def __eq__(self, other):
        if not isinstance(other, Favourite):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Favourite):
            raise TypeError("Comparison must be between Favourite instances")
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def id(self):
        return self.__id

    @property
    def user(self):
        return self.__user

    @property
    def recipe(self):
        return self.__recipe

    @property
    def date(self):
        return self.__date
