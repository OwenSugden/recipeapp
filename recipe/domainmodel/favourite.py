class Favourite:
    def __init__(self, user_name: str, recipe_id: int):
        self.__user_name = user_name
        self.__recipe_id = recipe_id

    def __repr__(self):
        return f"<User: {self.__user_name} favourite recipe: {self.__recipe_id}>"

    def __eq__(self, other):
        if not isinstance(other, Favourite):
            return False
        return self.__user_name == other.__user_name and self.__recipe_id == other.__recipe_id

    def __lt__(self, other):
        if not isinstance(other, Favourite):
            raise TypeError("Comparison must be between Favourite instances")
        return self.__user_name < other.__user_name or self.__recipe_id < other.__recipe_id

    def __hash__(self):
        return hash((self.__user_name, self.__recipe_id))

    @property
    def user_name(self):
        return self.__user_name

    @property
    def recipe_id(self):
        return self.__recipe_id

