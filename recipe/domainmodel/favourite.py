class Favourite:
    def __init__(self, user_id: int, recipe_id: int):
        self.__user_id = user_id
        self.__recipe_id = recipe_id

    def __repr__(self):
        return f"<User: {self.__user_id} favourite recipe: {self.__recipe_id}>"

    def __eq__(self, other):
        if not isinstance(other, Favourite):
            return False
        return self.__user_id == other.__user_id and self.__recipe_id == other.__recipe_id

    def __lt__(self, other):
        if not isinstance(other, Favourite):
            raise TypeError("Comparison must be between Favourite instances")
        return self.__user_id < other.__user_id or self.__recipe_id < other.__recipe_id

    def __hash__(self):
        return hash((self.__user_id, self.__recipe_id))

    @property
    def user_id(self):
        return self.__user_id

    @property
    def recipe_id(self):
        return self.__recipe_id

