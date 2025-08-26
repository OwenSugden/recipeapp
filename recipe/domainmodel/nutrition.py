class Nutrition:
    def __init__(self, calories: float, fat_content: float, carbohydrates_content: float,
                 protein_content: float,
                 saturated_fat_content: float = 0.0, cholesterol_content: float = 0.0, sodium_content: float = 0.0,
                 fiber_content: float = 0.0 , sugar_content: float = 0.0):

        self.__calories = calories
        self.__fat = fat_content
        self.__protein = protein_content
        self.__carbohydrates = carbohydrates_content
        self.__saturated_fat = saturated_fat_content
        self.__cholesterol = cholesterol_content
        self.__sodium = sodium_content
        self.__fiber = fiber_content
        self.__sugar = sugar_content

    def __repr__(self) -> str:
        return (f"<Nutrition: cal={self.calories}, fat={self.fat}, carbs={self.carbohydrates}, "
                f"protein={self.protein}, sat_fat={self.saturated_fat}, chol={self.cholesterol}, sodium={self.sodium}, "
                f"fiber={self.fiber}, sugar={self.sugar}>")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Nutrition):
            return False
        return (self.calories == other.calories and
                self.fat == other.fat and
                self.carbohydrates == other.carbohydrates and
                self.protein == other.protein and
                self.saturated_fat == other.saturated_fat and
                self.cholesterol == other.cholesterol and
                self.sodium == other.sodium and
                self.fiber == other.fiber and
                self.sugar == other.sugar)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Nutrition):
            raise TypeError("Comparison must be between Nutrition instances")
        return self.calories < other.calories

    def __hash__(self) -> int:
        return hash((self.calories, self.fat, self.carbohydrates, self.protein, self.saturated_fat, self.cholesterol,
                     self.sodium, self.fiber, self.sugar))

    @property
    def calories(self) -> float:
        return self.__calories

    @calories.setter
    def calories(self, value: float):
        if value < 0.0:
            raise ValueError("Calories cannot be negative")
        self.__calories = float(value)

    @property
    def fat(self) -> float:
        return self.__fat

    @fat.setter
    def fat(self, value: float):
        if value < 0.0:
            raise ValueError("Fat cannot be negative")
        self.__fat = float(value)

    @property
    def carbohydrates(self) -> float:
        return self.__carbohydrates

    @carbohydrates.setter
    def carbohydrates(self, value: float):
        if value < 0.0:
            raise ValueError("Carbohydrates cannot be negative")
        self.__carbohydrates = float(value)

    @property
    def protein(self) -> float:
        return self.__protein

    @protein.setter
    def protein(self, value: float):
        if value < 0.0:
            raise ValueError("Protein cannot be negative")
        self.__protein = float(value)

    @property
    def saturated_fat(self) -> float:
        return self.__saturated_fat

    @saturated_fat.setter
    def saturated_fat(self, value: float):
        if value < 0.0:
            raise ValueError("Saturated fat cannot be negative")
        self.__saturated_fat = float(value)

    @property
    def cholesterol(self) -> float:
        return self.__cholesterol

    @cholesterol.setter
    def cholesterol(self, value: float):
        if value < 0.0:
            raise ValueError("Cholesterol cannot be negative")
        self.__cholesterol = float(value)

    @property
    def sodium(self) -> float:
        return self.__sodium

    @sodium.setter
    def sodium(self, value: float):
        if value < 0.0:
            raise ValueError("Sodium cannot be negative")
        self.__sodium = float(value)

    @property
    def fiber(self) -> float:
        return self.__fiber

    @fiber.setter
    def fiber(self, value: float):
        if value < 0.0:
            raise ValueError("Fiber cannot be negative")
        self.__fiber = float(value)

    @property
    def sugar(self) -> float:
        return self.__sugar

    @sugar.setter
    def sugar(self, value: float):
        if value < 0.0:
            raise ValueError("Sugar cannot be negative")
        self.__sugar = float(value)
