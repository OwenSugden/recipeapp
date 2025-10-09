from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.review import Review
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe_ingredient import RecipeIngredient
from recipe.domainmodel.recipe_instruction import RecipeInstruction
from datetime import datetime


class Recipe:
    def __init__(self, recipe_id: int, name: str, author: "Author",
                 cook_time: int = 0,
                 preparation_time: int = 0,
                 total_time: int = 0,
                 created_date: datetime = None,
                 description: str = "",
                 images: list[RecipeImage] = None,
                 category: "Category" = None,
                 ingredients: list[RecipeIngredient] = None,
                 nutrition: "Nutrition" = None,
                 servings: int | None = None,
                 recipe_yield: str | None = None,
                 instructions: list[RecipeInstruction] = None):

        self.__id = recipe_id
        self.__name = name
        self.__author = author
        self.__cook_time = cook_time
        self.__preparation_time = preparation_time
        self.__total_time = total_time
        self.__created_date = created_date
        self.__description = description
        self.__images = images if images else []
        self.__category = category
        self.__ingredients = ingredients if ingredients else []
        self.__nutrition = nutrition
        self.__servings = servings if servings else "Not specified"
        self.__recipe_yield = recipe_yield if recipe_yield else "Not specified"
        self.__instructions = instructions if instructions else []
        self.__review = [Review]

    def __repr__(self) -> str:
        return (f"<Recipe {self.__name} with id: {self.id} was created by {self.__author.name} "
                f"on {self.__created_date}>")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Recipe):
            return False
        return self.id == other.id

    def __lt__(self, other) -> bool:
        if not isinstance(other, Recipe):
            raise TypeError("Comparison must be between Recipe instances")
        return self.id < other.id

    def __hash__(self) -> int:
        return hash(self.__id)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def author(self) -> "Author":
        return self.__author

    @property
    def cook_time(self) -> int:
        return self.__cook_time

    @cook_time.setter
    def cook_time(self, value: int):
        if value < 0:
            raise ValueError("Cook time cannot be negative.")
        self.__cook_time = value

    @property
    def preparation_time(self) -> int:
        return self.__preparation_time

    @preparation_time.setter
    def preparation_time(self, value: int):
        if value < 0:
            raise ValueError("Preparation time cannot be negative.")
        self.__preparation_time = value

    @property
    def total_time(self) -> int:
        return self.__total_time

    @total_time.setter
    def total_time(self, value: int):
        if value < 0:
            raise ValueError("Total time cannot be negative.")
        self.__total_time = value

    @property
    def created_date(self) -> datetime:
        return self.__created_date

    @created_date.setter
    def created_date(self, value: datetime):
        if not isinstance(value, datetime):
            raise TypeError("date must be a datetime.")
        self.__created_date = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, text: str):
        self.__description = text.strip()

    @property
    def images(self) -> list[RecipeImage]:
        return self.__images

    @images.setter
    def images(self, value: list[RecipeImage]):
        if not isinstance(value, list) or not all(isinstance(x, RecipeImage) for x in value):
            raise TypeError("images must be a list of RecipeImage objects.")
        self.__images = value

    @property
    def category(self) -> "Category":
        return self.__category

    @category.setter
    def category(self, value: "Category"):
        self.__category = value

    @property
    def ingredients(self) -> list[RecipeIngredient]:
        return self.__ingredients

    @ingredients.setter
    def ingredients(self, value: list[RecipeIngredient]):
        if not isinstance(value, list) or not all(isinstance(x, RecipeIngredient) for x in value):
            raise TypeError("ingredients must be a list of RecipeIngredient objects.")
        self.__ingredients = value

    @property
    def nutrition(self) -> "Nutrition":
        return self.__nutrition

    @nutrition.setter
    def nutrition(self, value: "Nutrition"):
        self.__nutrition = value

    @property
    def servings(self) -> str:
        return self.__servings

    @servings.setter
    def servings(self, value: str):
        self.__servings = value if value else "Not specified"

    @property
    def recipe_yield(self) -> str:
        return self.__recipe_yield

    @recipe_yield.setter
    def recipe_yield(self, value: str):
        self.__recipe_yield = value if value else "Not specified"

    @property
    def instructions(self) -> list[RecipeInstruction]:
        return self.__instructions

    @instructions.setter
    def instructions(self, steps: list[RecipeInstruction]):
        if not isinstance(steps, list) or not all(isinstance(x, RecipeInstruction) for x in steps):
            raise ValueError("instructions must be a list of RecipeInstruction objects.")
        self.__instructions = steps
