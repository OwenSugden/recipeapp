
from datetime import datetime

from recipe.domainmodel.user import User


class Comment:
    def __init__(self, user_name: str, comment_id: int, recipe_id: int, user_id: int, text: str, timestamp: datetime = None):
        self.__id = comment_id
        self.__recipe_id = recipe_id
        self.__user_id = user_id
        self.__text = text.strip()
        self.__timestamp = timestamp or datetime.now()
        self.__user_name = user_name

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
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value.strip()

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def user_name(self):
        return self.__user_name