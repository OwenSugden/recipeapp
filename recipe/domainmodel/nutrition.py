class Nutrition:
    def __init__(self, nutrition_id: int, calories: float, fat: float, saturated_fat: float, cholesterol: float,
                 sodium: float, carbohydrates: float, fiber: float, sugar: float, protein: float):
        self.__id = nutrition_id
        self.__calories = calories
        self.__fat = fat
        self.__saturated_fat = saturated_fat
        self.__cholesterol = cholesterol
        self.__sodium = sodium
        self.__carbohydrates = carbohydrates
        self.__fiber = fiber
        self.__sugar = sugar
        self.__protein = protein

    def __repr__(self) -> str:
        return (f"<Nutrition: Calories: {self.calories}, Protein: {self.protein}, Fat Total: {self.fat}, "
                f"Carbohydrates: {self.carbohydrates}>")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Nutrition):
            return False
        return self.id == other.id

    def __lt__(self, other) -> bool:
        if not isinstance(other, Nutrition):
            raise TypeError("Comparison must be between Nutrition instances")
        return self.id < other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def health_star(self):
        if (self.calories is None or self.saturated_fat is None or self.sugar is None or self.sodium is None
                or self.protein is None or self.fiber is None):
            return "Health star rating unavailable"

        else:
            neg = 30 * min(self.calories / 700.0, 1.5) \
                  + 25 * min(self.saturated_fat / 10.0, 1.5) \
                  + 25 * min(self.sugar / 25.0, 1.5) \
                  + 20 * min(self.sodium / 1000.0, 1.5)

            pos = 20 * min(self.protein / 25.0, 1.0) \
                  + 20 * min(self.fiber / 8.0, 1.0)

            raw = max(0.0, min(100.0, 100 - neg + pos))
            return round((raw / 20.0) * 2) / 2.0

    @property
    def id(self) -> int:
        return self.__id

    @property
    def calories(self) -> float:
        return self.__calories

    @property
    def fat(self) -> float:
        return self.__fat

    @property
    def saturated_fat(self) -> float:
        return self.__saturated_fat

    @property
    def cholesterol(self) -> float:
        return self.__cholesterol

    @property
    def sodium(self) -> float:
        return self.__sodium

    @property
    def carbohydrates(self) -> float:
        return self.__carbohydrates

    @property
    def fiber(self) -> float:
        return self.__fiber

    @property
    def sugar(self) -> float:
        return self.__sugar

    @property
    def protein(self) -> float:
        return self.__protein