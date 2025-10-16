from tests.conftest import *
from datetime import datetime

from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe import RecipeIngredient
from recipe.domainmodel.recipe import RecipeInstruction
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User

# Author tests
def test_author_construction():
    author = Author(1, "Jamie Oliver")
    assert author.id == 1
    assert author.name == "Jamie Oliver"
    assert author.recipes == []


def test_author_equality():
    author1 = Author(1, "Chef A")
    author2 = Author(1, "Chef B")
    author3 = Author(2, "Chef A")
    assert author1 == author2
    assert author1 != author3


def test_author_less_than():
    author1 = Author(1, "Chef A")
    author2 = Author(2, "Chef B")
    assert author1 < author2

def test_author_hash():
    author1 = Author(1, "Chef A")
    author2 = Author(1, "Chef B")
    author_set = {author1, author2}
    assert len(author_set) == 1

def test_author_repr(my_author):
    # my_author: Author(1, "Gordon Ramsay")
    assert repr(my_author) == "<Author 1: Gordon Ramsay>"

# Category tests
def test_category_construction():
    cat = Category(10, "Desserts", [])
    assert cat.id == 10
    assert cat.name == "Desserts"
    assert cat.recipes == []

def test_category_equality():
    c1 = Category(1, "Italian", [])
    c2 = Category(1, "Pasta", [])   # same id, different name -> equal
    c3 = Category(2, "Italian", [])
    assert c1 == c2
    assert c1 != c3

def test_category_less_than():
    c1 = Category(1, "A", [])
    c2 = Category(2, "B", [])
    assert c1 < c2

def test_category_hash():
    c1 = Category(1, "A", [])
    c2 = Category(1, "B", [])
    cat_set = {c1, c2}
    assert len(cat_set) == 1

def test_category_repr(my_category):
    # my_category: Category("Italian", [], 1)
    assert repr(my_category) == "<Category 1: Italian>"

# Favourite tests
def test_favourite_construction(my_user, my_recipe):
    dt = datetime(2024, 1, 1)
    fav = Favourite(42, my_user.id, my_recipe.id, dt)
    assert fav.id == 42
    assert fav.user_id is my_user.id
    assert fav.recipe_id is my_recipe.id
    assert fav.date == dt

def test_favourite_equality(my_user, my_recipe):
    dt = datetime(2024, 1, 1)
    f1 = Favourite(1, my_user, my_recipe, dt)
    f2 = Favourite(1, my_user, my_recipe, dt)
    f3 = Favourite(2, my_user, my_recipe, dt)
    assert f1 == f2
    assert f1 != f3

def test_favourite_less_than(my_user, my_recipe):
    f1 = Favourite(1, my_user, my_recipe, datetime(2024, 1, 1))
    f2 = Favourite(2, my_user, my_recipe, datetime(2024, 1, 2))
    assert f1 < f2

def test_favourite_hash(my_user, my_recipe):
    f1 = Favourite(1, my_user, my_recipe, datetime(2024, 1, 1))
    f2 = Favourite(2, my_user, my_recipe, datetime(2024, 1, 2))
    fav_set = {f1, f2}
    assert len(fav_set) == 2

def test_favourite_repr(my_favourite, my_user, my_recipe):
    # my_favourite: Favourite(1, my_user, my_recipe, datetime(2024, 1, 1))
    assert repr(my_favourite) == f"<Favourite: User={my_user.id}, Recipe={my_recipe.id}>"

# Nutrition tests
def test_nutrition_construction():
    n = Nutrition(1, 250.0, 10.0, 3.0, 30.0, 200.0, 30.0, 5.0, 12.0, 8.0)
    assert n.id == 1
    assert n.calories == 250.0
    assert n.fat == 10.0
    assert n.saturated_fat == 3.0
    assert n.cholesterol == 30.0
    assert n.sodium == 200.0
    assert n.carbohydrates == 30.0
    assert n.fiber == 5.0
    assert n.sugar == 12.0
    assert n.protein == 8.0

def test_nutrition_equality():
    a = Nutrition(1, 100.0, 5.0, 1.0, 10.0, 50.0, 20.0, 3.0, 5.0, 6.0)
    b = Nutrition(1, 999.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0)  # same id -> equal
    c = Nutrition(2, 100.0, 5.0, 1.0, 10.0, 50.0, 20.0, 3.0, 5.0, 6.0)
    assert a == b
    assert a != c

def test_nutrition_less_than():
    low = Nutrition(1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    high = Nutrition(2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    assert low < high

def test_nutrition_hash():
    a = Nutrition(7, 100.0, 5.0, 1.0, 10.0, 50.0, 20.0, 3.0, 5.0, 6.0)
    b = Nutrition(7, 200.0, 6.0, 2.0, 12.0, 60.0, 25.0, 4.0, 6.0, 8.0)  # same id
    c = Nutrition(8, 100.0, 5.0, 1.0, 10.0, 50.0, 20.0, 3.0, 5.0, 6.0)
    s = {a, b, c}
    assert len(s) == 2
    assert a in s and b in s and c in s

def test_nutrition_repr():
    n = Nutrition(3, 200.0, 9.0, 2.0, 25.0, 150.0, 28.0, 4.0, 10.0, 12.0)
    r = repr(n)
    assert r == "<Nutrition: Calories: 200.0, Protein: 12.0, Fat Total: 9.0, Carbohydrates: 28.0>"

def test_health_star(my_nutrition):
    rating = my_nutrition.health_star()
    expected = 3.0
    assert rating == expected

def test_health_star_with_missing_data():
    n = Nutrition(1,None, 10, 3, 20, 200, 15, 5, 7, 8)
    assert n.health_star() == "Health star rating unavailable"

# Recipe tests
def test_recipe_construction(my_author, my_category, my_nutrition, my_recipe_image, my_recipe_ingredients, my_recipe_instructions):
    recipe = Recipe(
        recipe_id=1,
        name="Spaghetti Carbonara",
        author=my_author,
        cook_time=20,
        preparation_time=15,
        created_date=datetime(2024, 1, 1),
        description="Classic Italian pasta dish",
        images=[my_recipe_image],
        category=my_category,
        ingredients=my_recipe_ingredients,
        nutrition=my_nutrition,
        servings=4,
        recipe_yield="4 portions",
        instructions=my_recipe_instructions,
    )
    assert recipe.id == 1
    assert recipe.name == "Spaghetti Carbonara"
    assert recipe.author is my_author
    assert recipe.cook_time == 20
    assert recipe.preparation_time == 15
    assert isinstance(recipe.created_date, datetime)
    assert "Classic Italian" in recipe.description
    assert isinstance(recipe.images, list) and recipe.images[0] is my_recipe_image
    assert recipe.category is my_category
    assert recipe.ingredients == my_recipe_ingredients
    assert recipe.nutrition is my_nutrition
    assert recipe.servings == 4
    assert recipe.recipe_yield == "4 portions"
    assert recipe.instructions == my_recipe_instructions

def test_recipe_equality(my_author, my_category, my_nutrition):
    r1 = Recipe(
        recipe_id=10,
        name="A",
        author=my_author,
        cook_time=5,
        preparation_time=5,
        created_date=datetime(2024, 1, 1),
        description="x",
        images=[],
        category=my_category,
        ingredients=[],
        nutrition=my_nutrition,
        servings=1,
        recipe_yield="1",
        instructions=[]
    )
    r2 = Recipe(
        recipe_id=10,  # same id -> equal
        name="B",
        author=my_author,
        cook_time=7,
        preparation_time=3,
        created_date=datetime(2024, 1, 2),
        description="y",
        images=[],
        category=my_category,
        ingredients=[],
        nutrition=my_nutrition,
        servings=2,
        recipe_yield="2",
        instructions=[]
    )
    r3 = Recipe(
        recipe_id=11,
        name="C",
        author=my_author,
        cook_time=7,
        preparation_time=3,
        created_date=datetime(2024, 1, 2),
        description="z",
        images=[],
        category=my_category,
        ingredients=[],
        nutrition=my_nutrition,
        servings=2,
        recipe_yield="2",
        instructions=[]
    )
    assert r1 == r2
    assert r1 != r3

def test_recipe_less_than(my_author, my_category, my_nutrition):
    a = Recipe(
        recipe_id=1,
        name="A",
        author=my_author,
        cook_time=0,
        preparation_time=0,
        created_date=datetime(2024, 1, 1),
        description="",
        images=[],
        category=my_category,
        ingredients=[],
        nutrition=my_nutrition,
        servings=1,
        recipe_yield="1",
        instructions=[]
    )
    b = Recipe(
        recipe_id=2,
        name="B",
        author=my_author,
        cook_time=0,
        preparation_time=0,
        created_date=datetime(2024, 1, 1),
        description="",
        images=[],
        category=my_category,
        ingredients=[],
        nutrition=my_nutrition,
        servings=1,
        recipe_yield="1",
        instructions=[]
    )
    assert a < b

def test_recipe_hash(my_author, my_category, my_nutrition):
    a = Recipe(
        recipe_id=7,
        name="A",
        author=my_author,
        cook_time=0,
        preparation_time=0,
        created_date=datetime(2024, 1, 1),
        description="",
        images=[],
        category=my_category,
        ingredients=[],
        nutrition=my_nutrition,
        servings=1,
        recipe_yield="1",
        instructions=[]
    )
    b = Recipe(
        recipe_id=7,
        name="B",
        author=my_author,
        cook_time=10,
        preparation_time=5,
        created_date=datetime(2024, 1, 2),
        description="desc",
        images=[],
        category=my_category,
        ingredients=[],
        nutrition=my_nutrition,
        servings=2,
        recipe_yield="2",
        instructions=[]
    )
    c = Recipe(
        recipe_id=8,
        name="C",
        author=my_author,
        cook_time=0,
        preparation_time=0,
        created_date=datetime(2024, 1, 1),
        description="",
        images=[],
        category=my_category,
        ingredients=[],
        nutrition=my_nutrition,
        servings=1,
        recipe_yield="1",
        instructions=[]
    )

    s = {a, b, c}
    assert len(s) == 2
    assert a in s and b in s and c in s

def test_recipe_repr(my_recipe):
    r = repr(my_recipe)
    assert "Recipe" in r or "recipe" in r
    assert str(my_recipe.id) in r
    assert my_recipe.name in r

# RecipeImage tests
def test_recipe_image_construction():
    img = RecipeImage(recipe_id=1, url="https://example.com/a.jpg", position=0)
    assert img.recipe_id == 1
    assert img.url == "https://example.com/a.jpg"
    assert img.position == 0

def test_recipe_image_equality():
    a = RecipeImage(1, "https://x/a.jpg", 0)
    b = RecipeImage(1, "https://x/other.jpg", 0)
    c = RecipeImage(1, "https://x/a.jpg", 1)
    d = RecipeImage(2, "https://x/a.jpg", 0)
    assert a == b
    assert a != c
    assert a != d

def test_recipe_image_hash():
    a = RecipeImage(1, "https://x/a.jpg", 0)
    b = RecipeImage(1, "https://x/b.jpg", 0)
    c = RecipeImage(1, "https://x/a.jpg", 1)
    s = {a, b, c}
    assert len(s) == 2
    assert a in s and b in s and c in s

def test_recipe_image_repr():
    img = RecipeImage(3, "https://img.site/pic.png", 4)
    assert repr(img) == "<RecipeImage: Recipe 3, Position 4, URL: https://img.site/pic.png>"

# RecipeIngredient tests
def test_recipe_ingredient_construction():
    ing = RecipeIngredient(recipe_id=1, quantity="1 cup", ingredient="flour", position=0)
    assert ing.recipe_id == 1
    assert ing.quantity == "1 cup"
    assert ing.ingredient == "flour"
    assert ing.position == 0

def test_recipe_ingredient_equality():
    a = RecipeIngredient(1, "1 cup", "flour", 0)
    b = RecipeIngredient(1, "2 cups", "sugar", 0)
    c = RecipeIngredient(1, "1 cup", "flour", 1)
    d = RecipeIngredient(2, "1 cup", "flour", 0)
    assert a == b
    assert a != c
    assert a != d

def test_recipe_ingredient_hash():
    a = RecipeIngredient(1, "1 cup", "flour", 0)
    b = RecipeIngredient(1, "2 cups", "sugar", 0)
    c = RecipeIngredient(1, "1 cup", "flour", 1)
    s = {a, b, c}
    assert len(s) == 2
    assert a in s and b in s and c in s

def test_recipe_ingredient_repr():
    ing = RecipeIngredient(3, "200 g", "spaghetti", 4)
    assert repr(ing) == "<RecipeIngredient: Recipe 3, Position 4, 200 g spaghetti>"

# RecipeInstruction tests
def test_recipe_instruction_construction():
    instr = RecipeInstruction(recipe_id=1, step="Boil water", position=0)
    assert instr.recipe_id == 1
    assert instr.step == "Boil water"
    assert instr.position == 0

def test_recipe_instruction_equality():
    a = RecipeInstruction(1, "Boil water", 0)
    b = RecipeInstruction(1, "Add pasta", 0)
    c = RecipeInstruction(1, "Boil water", 1)
    d = RecipeInstruction(2, "Boil water", 0)
    assert a == b
    assert a != c
    assert a != d

def test_recipe_instruction_hash():
    a = RecipeInstruction(1, "Step A", 0)
    b = RecipeInstruction(1, "Different text same pos", 0)
    c = RecipeInstruction(1, "Step C", 1)
    s = {a, b, c}
    assert len(s) == 2
    assert a in s and b in s and c in s

def test_recipe_instruction_repr():
    instr = RecipeInstruction(3, "Mix well", 4)
    assert repr(instr) == "<RecipeInstruction: Recipe 3, Step 4: Mix well...>"

# Review tests
def test_review_construction(my_user, my_recipe):
    dt = datetime(2024, 1, 1)
    r = Review(1, my_user.id, dt, my_recipe.id, 4.0, "Nice!")
    assert r.id == 1
    assert r.user_id is my_user.id
    assert r.date == dt
    assert r.recipe_id is my_recipe.id
    assert r.rating == 4.0
    assert r.comment == "Nice!"

def test_review_equality(my_user, my_recipe):
    a = Review(10, my_user, datetime(2024, 1, 1), my_recipe, 3.0, "ok")
    b = Review(10, my_user, datetime(2024, 1, 2), my_recipe, 5.0, "great")
    c = Review(11, my_user, datetime(2024, 1, 1), my_recipe, 3.0, "ok")
    assert a == b
    assert a != c

def test_review_less_than(my_user, my_recipe):
    low = Review(1, my_user, datetime(2024, 1, 1), my_recipe, 2.0, "low")
    high = Review(2, my_user, datetime(2024, 1, 1), my_recipe, 4.0, "high")
    assert low < high

def test_review_hash(my_user, my_recipe):
    a = Review(7, my_user, datetime(2024, 1, 1), my_recipe, 3.0, "a")
    b = Review(7, my_user, datetime(2024, 1, 2), my_recipe, 5.0, "b")  # same id
    c = Review(8, my_user, datetime(2024, 1, 3), my_recipe, 1.0, "c")
    s = {a, b, c}
    assert len(s) == 2
    assert a in s and b in s and c in s

def test_review_repr(my_review, my_user, my_recipe):
    assert repr(my_review) == f"<Review: User: {my_user.id}, Recipe: {my_recipe.id}>"

def test_review_update_rating_valid(my_user, my_recipe):
    rv = Review(1, my_user, datetime(2024, 1, 1), my_recipe, 2.5, "meh")
    rv.update_rating(4.0)
    assert rv.rating == 4.0
    rv.update_rating(0.0)
    assert rv.rating == 0.0
    rv.update_rating(5.0)
    assert rv.rating == 5.0

def test_review_update_comment(my_user, my_recipe):
    rv = Review(3, my_user, datetime(2024, 1, 1), my_recipe, 3.5, "old")
    rv.update_comment("new comment")
    assert rv.comment == "new comment"

# User tests
def test_user_construction():
    u = User(42, "Alice", "secret123")
    assert u.id == 42
    assert u.username == "Alice"
    assert u.password == "secret123"


def test_user_equality():
    a = User(1, "A", "x")
    b = User(1, "B", "y")
    c = User(2, "C", "z")
    assert a == b
    assert a != c

def test_user_less_than():
    u1 = User(1, "Lower", "x")
    u2 = User(2, "Higher", "y")
    assert u1 < u2

def test_user_hash():
    a = User(7,"A", "x")
    b = User(7, "B", "y")  # same id
    c = User(8, "C", "z")
    s = {a, b, c}
    assert len(s) == 2
    assert a in s and b in s and c in s

def test_user_repr(my_user):
     assert repr(my_user) == f"<User {my_user.id}: {my_user.username}>"

def test_user_add_review(my_user, my_recipe):
    rv = Review(1, my_user, datetime(2024, 1, 1), my_recipe, 4.0, "Nice")
    # add
    my_user.add_review(rv)
    assert rv in my_user.reviews
    assert len(my_user.reviews) >= 1

def test_user_check_password_correct_and_incorrect(my_user):
    assert my_user.check_password("password123") is True
    assert my_user.check_password("wrong-pass") is False
