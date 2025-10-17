from datetime import datetime
from tests.conftest import *
from datetime import datetime
from recipe.domainmodel.recipe import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.recipe import RecipeImage
from recipe.domainmodel.recipe import RecipeIngredient
from recipe.domainmodel.recipe import RecipeInstruction
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User



# MemoryRepository tests
# Author tests
def test_add_author(memory_repository, my_author):
    memory_repository.add_author(my_author)
    authors = memory_repository.get_authors()
    assert len(authors) == 1
    assert authors[0] == my_author

def test_get_author_by_id(memory_repository, my_author):
    memory_repository.add_author(my_author)
    found = memory_repository.get_author_by_id(my_author.id)
    assert found == my_author

def test_get_authors(memory_repository, my_author):
    memory_repository.add_author(my_author)
    authors = memory_repository.get_authors()

    assert authors[0].id == 1

def test_get_number_of_authors(memory_repository, my_author):
    memory_repository.add_author(my_author)
    authors = memory_repository.get_authors()
    number_of_authors = memory_repository.get_number_of_authors()
    expected = len(authors)
    assert number_of_authors == expected

def test_add_multiple_authors(memory_repository):
    authors = [
        Author(1, "Gordon Ramsay"),
        Author(2, "Nigella Lawson"),
        Author(3, "Jamie Oliver"),
    ]

    memory_repository.add_multiple_authors(authors)
    result = memory_repository.get_authors()
    assert result == authors
    assert len(result) == 3

# Category tests
def test_add_category(memory_repository, my_category):
    memory_repository.add_category(my_category)
    categories = memory_repository.get_categories()
    assert len(categories) == 1
    assert categories[0] == my_category

def test_get_category_by_id(memory_repository, my_category):
    memory_repository.add_category(my_category)
    found = memory_repository.get_category_by_id(my_category.id)
    assert found == my_category

def test_get_categories(memory_repository, my_category):
    memory_repository.add_category(my_category)
    categories = memory_repository.get_categories()

    assert categories[0].id == 1

def test_get_number_of_categories(memory_repository, my_category):
    memory_repository.add_category(my_category)
    categories = memory_repository.get_categories()
    number_of_categories = memory_repository.get_number_of_categories()
    expected = len(categories)
    assert number_of_categories == expected

def test_add_multiple_categories(memory_repository, my_recipe):
    categories = [
        Category(1, "C1", [my_recipe]),
        Category(2, "C2", [my_recipe]),
        Category(3, "C2", [my_recipe])
    ]

    memory_repository.add_multiple_categories(categories)
    result = memory_repository.get_categories()
    assert result == categories
    assert len(result) == 3

# Favourite tests
# TODO finish this

# Nutrition tests
def test_add_nutrition(memory_repository, my_nutrition):
    memory_repository.add_nutrition(my_nutrition)
    nutritions = memory_repository.get_nutritions()
    assert len(nutritions) == 1
    assert nutritions[0] == my_nutrition

def test_get_nutrition_by_id(memory_repository, my_nutrition):
    memory_repository.add_nutrition(my_nutrition)
    found = memory_repository.get_nutrition_by_id(my_nutrition.id)
    assert found == my_nutrition

def test_get_nutritions(memory_repository, my_nutrition):
    memory_repository.add_nutrition(my_nutrition)
    nutritions = memory_repository.get_nutritions()

    assert nutritions[0].id == 1

def test_add_multiple_nutritions(memory_repository, my_nutrition):
    nutritions = [
        Nutrition(
            nutrition_id=1,
            calories=250.0,
            fat=10.0,
            saturated_fat=3.0,
            cholesterol=30.0,
            sodium=200.0,
            carbohydrates=30.0,
            fiber=5.0,
            sugar=12.0,
            protein=8.0
        ),
        Nutrition(
            nutrition_id=2,
            calories=450.0,
            fat=20.0,
            saturated_fat=8.0,
            cholesterol=60.0,
            sodium=500.0,
            carbohydrates=50.0,
            fiber=3.0,
            sugar=20.0,
            protein=15.0
        ),
        Nutrition(
            nutrition_id=3,
            calories=120.0,
            fat=2.0,
            saturated_fat=0.5,
            cholesterol=10.0,
            sodium=100.0,
            carbohydrates=15.0,
            fiber=4.0,
            sugar=5.0,
            protein=6.0
        ),
    ]

    memory_repository.add_multiple_nutritions(nutritions)
    result = memory_repository.get_nutritions()
    assert result == nutritions
    assert len(result) == 3

# Recipe tests
def test_add_recipe(memory_repository, my_recipe):
    memory_repository.add_author(my_recipe.author)
    memory_repository.add_category(my_recipe.category)
    memory_repository.add_recipe(my_recipe)
    recipes = memory_repository.get_recipes()
    assert len(recipes) == 1
    assert recipes[0] == my_recipe

def test_get_recipe_by_id(memory_repository, my_recipe):
    memory_repository.add_recipe(my_recipe)
    found = memory_repository.get_recipe_by_id(my_recipe.id)
    assert found == my_recipe

def test_get_recipes(memory_repository, my_recipe):
    memory_repository.add_recipe(my_recipe)
    recipes = memory_repository.get_recipes()
    assert recipes == [my_recipe]
    assert len(recipes) == 1
    assert recipes[0] == my_recipe

def test_get_number_of_recipes(memory_repository, my_recipe):
    memory_repository.add_recipe(my_recipe)
    recipes = memory_repository.get_recipes()
    number_of_recipes = memory_repository.get_number_of_recipes()
    expected = len(recipes)
    assert number_of_recipes == expected

def test_get_recipes_by_name(memory_repository, my_recipe):
    memory_repository.add_recipe(my_recipe)
    result = memory_repository.get_recipes_by_name("Spaghetti")
    assert result == [my_recipe]

def test_get_recipes_by_category(memory_repository, my_recipe):
    memory_repository.add_recipe(my_recipe)
    result = memory_repository.get_recipes_by_category(my_recipe.category.name)
    assert result == [my_recipe]

def test_get_recipes_by_author(memory_repository, my_recipe):
    memory_repository.add_recipe(my_recipe)
    result = memory_repository.get_recipes_by_author(my_recipe.author.name)
    assert result == [my_recipe]

def test_add_multiple_recipes(memory_repository, my_author, my_category, my_nutrition):
    r1 = Recipe(
        recipe_id=10, name="A", author=my_author, cook_time=5, preparation_time=5,
        created_date=datetime(2024, 1, 1), description="x", images=[],
        category=my_category, ingredients=[], nutrition=my_nutrition,
        servings=1, recipe_yield="1", instructions=[]
    )
    r2 = Recipe(
        recipe_id=11, name="B", author=my_author, cook_time=6, preparation_time=4,
        created_date=datetime(2024, 1, 2), description="y", images=[],
        category=my_category, ingredients=[], nutrition=my_nutrition,
        servings=2, recipe_yield="2", instructions=[]
    )
    recipes = [r1, r2]
    memory_repository.add_multiple_recipes(recipes)
    result = memory_repository.get_recipes()
    assert result == recipes
    assert len(result) == 2

# Favourite tests
# TODO finish this
def test_add_and_get_favourites(memory_repository, my_user, my_recipe):
    fav_id = memory_repository.get_new_favourite_id()
    favourite = Favourite(
        fav_id,
        user_id=my_user.id,
        recipe_id=my_recipe.id,
        date=datetime.now()
    )

    memory_repository.add_favourite(favourite)
    result = memory_repository.get_favourites_for_user(my_user.id)

    assert len(result) == 1
    assert result[0].recipe_id == my_recipe.id
    assert result[0].user_id == my_user.id

def test_add_duplicate_favourite(memory_repository, my_user, my_recipe):
    fav_id = memory_repository.get_new_favourite_id()
    favourite = Favourite(
        fav_id,
        user_id=my_user.id,
        recipe_id=my_recipe.id,
        date=datetime.now()
    )
    memory_repository.add_favourite(favourite)
    memory_repository.add_favourite(favourite)

    result = memory_repository.get_favourites_for_user(my_user.id)
    assert len(result) == 1

def test_remove_favourite(memory_repository, my_user, my_recipe):
    fav_id = memory_repository.get_new_favourite_id()
    favourite = Favourite(
        fav_id,
        user_id=my_user.id,
        recipe_id=my_recipe.id,
        date=datetime.now()
    )

    memory_repository.add_favourite(favourite)
    memory_repository.remove_favourite(my_user.id, my_recipe.id)

    result = memory_repository.get_favourites_for_user(my_user.id)
    assert result == []
# User tests
# TODO finish this
def test_add_and_get_user(memory_repository, my_user):
    memory_repository.add_user(my_user)
    retrieved = memory_repository.get_user_by_id(my_user.id)

    assert retrieved == my_user
    assert retrieved.username == my_user.username

def test_get_user_by_username(memory_repository, my_user):
    memory_repository.add_user(my_user)
    retrieved = memory_repository.get_user(my_user.username)

    assert retrieved == my_user

def test_get_new_user_id(memory_repository):
    id1 = memory_repository.get_new_user_id()
    id2 = memory_repository.get_new_user_id()
    assert id2 == id1 + 1

#Review Tests
# TODO finish this

def test_add_and_get_reviews(memory_repository, my_user, my_recipe):
    review_id = memory_repository.get_new_review_id()
    review = Review(review_id, user_id=my_user.id,
                    recipe_id=my_recipe.id,
                    rating=5,
                    comment="coolio!",
                    date=datetime.now())

    memory_repository.add_review(review)
    reviews = memory_repository.get_reviews_for_recipe(my_recipe.id)

    assert len(reviews) == 1
    assert reviews[0].comment == "coolio!"

def test_remove_review(memory_repository, my_user, my_recipe):
    review_id = memory_repository.get_new_review_id()
    review = Review(review_id, user_id=my_user.id,
                    recipe_id=my_recipe.id,
                    rating=4, comment="snake!",
                    date=datetime.now())

    memory_repository.add_review(review)
    memory_repository.remove_review(my_user.id, review_id)

    reviews = memory_repository.get_reviews_for_user(my_user.id)
    assert reviews is None or len(reviews) == 0


def test_get_reviews_with_usernames(memory_repository, my_user, my_recipe):
    memory_repository.add_user(my_user)
    review_id = memory_repository.get_new_review_id()
    review = Review(review_id, user_id=my_user.id,
                    recipe_id=my_recipe.id,
                    rating=3,
                    comment="Ok",
                    date=datetime.now())

    memory_repository.add_review(review)
    results = memory_repository.get_reviews_with_usernames_for_recipe(my_recipe.id)

    assert len(results) == 1
    assert results[0][1] == my_user.username


def test_average_rating_same_user(memory_repository, my_user, my_recipe):
    r1 = Review(memory_repository.get_new_review_id(),
                user_id=my_user.id, recipe_id=my_recipe.id,
                rating=4, comment="god", date=datetime.now())

    r2 = Review(memory_repository.get_new_review_id(), user_id=my_user.id,
                recipe_id=my_recipe.id, rating=2,
                comment="bad", date=datetime.now())

    memory_repository.add_review(r1)
    memory_repository.add_review(r2)

    avg = memory_repository.get_average_rating(my_recipe.id)
    assert avg == 4.0


# RecipeImage tests
def test_add_recipe_image(memory_repository, my_recipe_image):
    memory_repository.add_recipe_image(my_recipe_image)
    result = memory_repository.get_recipe_image(38, my_recipe_image.position)
    assert result == my_recipe_image

def test_get_recipe_image(memory_repository, my_recipe_image):
    memory_repository.add_recipe_image(my_recipe_image)
    found = memory_repository.get_recipe_image(38, my_recipe_image.position)
    assert found == my_recipe_image

def test_get_recipe_images(memory_repository, my_recipe_image):
    memory_repository.add_recipe_image(my_recipe_image)
    recipe_images = memory_repository.get_recipe_images()

    assert recipe_images[0].recipe_id == 38

def test_add_multiple_recipe_image(memory_repository):
    imgs = [
        RecipeImage(recipe_id=1, url="https://x/a.jpg", position=0),
        RecipeImage(recipe_id=1, url="https://x/b.jpg", position=1),
    ]
    memory_repository.add_multiple_recipe_images(imgs)
    result = memory_repository.get_recipe_images()
    assert result == imgs
    assert len(result) == 2

# RecipeIngredient tests
def test_add_recipe_ingredient(memory_repository, my_recipe_ingredient):
    memory_repository.add_recipe_ingredient(my_recipe_ingredient)
    result = memory_repository.get_recipe_ingredient(38, my_recipe_ingredient.position)
    assert result == my_recipe_ingredient

def test_get_recipe_ingredient(memory_repository, my_recipe_ingredient):
    memory_repository.add_recipe_ingredient(my_recipe_ingredient)
    found = memory_repository.get_recipe_ingredient(38, my_recipe_ingredient.position)
    assert found == my_recipe_ingredient

def test_get_recipe_ingredients(memory_repository, my_recipe_ingredient):
    memory_repository.add_recipe_ingredient(my_recipe_ingredient)
    recipe_ingredients = memory_repository.get_recipe_ingredients()

    assert recipe_ingredients[0].recipe_id == 38

def test_add_multiple_recipe_ingredients(memory_repository):
    ings = [
        RecipeIngredient(recipe_id=1, quantity="4",   ingredient="blueberries",      position=1),
        RecipeIngredient(recipe_id=1, quantity="1/4", ingredient="granulated sugar", position=2),
    ]
    memory_repository.add_multiple_recipe_ingredients(ings)
    result = memory_repository.get_recipe_ingredients()
    assert result == ings
    assert len(result) == 2

# RecipeInstruction tests
def test_add_recipe_instruction(memory_repository, my_recipe_instruction):
    memory_repository.add_recipe_instruction(my_recipe_instruction)
    result = memory_repository.get_recipe_instruction(38, my_recipe_instruction.position)
    assert result == my_recipe_instruction

def test_get_recipe_instruction(memory_repository, my_recipe_instruction):
    memory_repository.add_recipe_instruction(my_recipe_instruction)
    found = memory_repository.get_recipe_instruction(38, my_recipe_instruction.position)
    assert found == my_recipe_instruction

def test_get_recipe_instructions(memory_repository, my_recipe_instruction):
    memory_repository.add_recipe_instruction(my_recipe_instruction)
    recipe_instructions = memory_repository.get_recipe_instructions()
    assert recipe_instructions[0].recipe_id == 38

def test_add_multiple_recipe_instructions(memory_repository):
    instrs = [
        RecipeInstruction(recipe_id=1, step="Chop onions.", position=1),
        RecipeInstruction(recipe_id=1, step="Sauté until soft.", position=2),
    ]
    memory_repository.add_multiple_recipe_instructions(instrs)
    result = memory_repository.get_recipe_instructions()
    assert result == instrs
    assert len(result) == 2