from datetime import datetime

class Favourite:
    def __init__(self, favourite_id: int, user_id: int, recipe_id: int, date: datetime):
        from datetime import datetime
        self.__id = favourite_id
        self.__user_id = user_id
        self.__recipe_id = recipe_id
        self.__date = date if date is not None else datetime.now()

    def __repr__(self):
        return f"<Favourite: User={self.__user_id}, Recipe={self.__recipe_id}>"

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
    def user_id(self):
        return self.__user_id

    @property
    def recipe_id(self):
        return self.__recipe_id

    @property
    def date(self):
        return self.__date