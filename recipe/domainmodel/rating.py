class Rating:
    def __init__(self, rating_id: int, recipe_id: int, user_id: int, value: int, user_name: str):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")

        self.__user_name = user_name
        self.__id = rating_id
        self.__recipe_id = recipe_id
        self.__user_id = user_id
        self.__value = value

    @property
    def id(self):
        return self.__id

    @property
    def recipe_id(self):
        return self.__recipe_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: int):
        if new_value < 1 or new_value > 5:
            raise ValueError("Rating must be between 1 and 5")
        self.__value = new_value

    @property
    def user_name(self):
        return self.__user_name