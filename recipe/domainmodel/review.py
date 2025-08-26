class Review:
    def __init__(self, review_id: int, recipe_id: int, user_id: int, rating: int, comment: str = None):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        if not isinstance(review_id, int) or review_id <= 0:
            raise ValueError("id must be a positive int.")

        self.__id = review_id
        self.__recipe_id = recipe_id
        self.__user_id = user_id
        self.__rating = rating
        self.__comment = comment

    def __repr__(self) -> str:
        return (f"<Review with id: {self.id} from recipe_id: {self.recipe_id} was made by user_id: {self.user_id}, "
                f"leaving a rating of {self.rating} stars and this comment: \n{self.comment!r}>")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Review):
            return False
        return self.id == other.id

    def __lt__(self, other) -> bool:
        if not isinstance(other, Review):
            raise TypeError("Comparison must be between Review instances")
        # Sort by rating first, then lexicographically by comment
        if self.rating != other.rating:
            return self.rating < other.rating
        return self.comment < other.comment

    def __hash__(self) -> int:
        return hash(self.__id)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def recipe_id(self) -> int:
        return self.__recipe_id

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def rating(self) -> int:
        return self.__rating

    @rating.setter
    def rating(self, value: float):
        if value is not None and (value < 0 or value > 5):
            raise ValueError("Rating must be between 0 and 5.")
        self.__rating = value

    @property
    def comment(self) -> str:
        return self.__comment

    @comment.setter
    def comment(self, value: str):
        self.__comment = value.strip()
