import pytest
from tests_db.conftest import *

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
def test_repository_can_add_author(session_factory, my_author):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_author(my_author)

    assert repo.get_author_by_id(1533) == my_author

def test_repository_can_get_author_by_id(session_factory, my_author):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_author(my_author)
    found = repo.get_author_by_id(1533)
    assert found == my_author

def test_repository_can_retrieve_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    authors = repo.get_authors()

    assert authors[0].id == 1533

def test_repository_can_get_number_of_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    authors = repo.get_authors()
    expected = len(authors)

    number_of_authors = repo.get_number_of_authors()
    assert expected == number_of_authors

def test_repository_can_add_multiple_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    authors = [
        Author(5000, "Nathan"),
        Author(5001, "Bob"),
        Author(5002, "Alice"),
    ]
    repo.add_multiple_authors(authors)

    assert repo.get_author_by_id(5000) == authors[0]
    assert repo.get_author_by_id(5001) == authors[1]
    assert repo.get_author_by_id(5002) == authors[2]

# Category tests
def test_repository_can_add_category(session_factory, my_category):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_category(my_category)

    assert repo.get_category_by_id(1) == my_category

def test_repository_can_get_category_by_id(session_factory, my_category):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_category(my_category)
    found = repo.get_category_by_id(1)
    assert found == my_category

def test_repository_can_retrieve_categories(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    categories = repo.get_categories()

    assert categories[0].id == 1

def test_repository_can_get_number_of_categories(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    categories = repo.get_categories()
    expected = len(categories)

    number_of_categories = repo.get_number_of_categories()
    assert expected == number_of_categories

def test_repository_can_add_multiple_categories(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    categories = [
        Category(1, "African"),
        Category(2, "Asian"),
        Category(3, "Mexican"),
    ]
    repo.add_multiple_categories(categories)

    assert repo.get_category_by_id(1) == categories[0]
    assert repo.get_category_by_id(2) == categories[1]
    assert repo.get_category_by_id(3) == categories[2]

# Favourites tests
# TODO finish these
def test_repository_can_add_favourite(session_factory, my_user, my_recipe):
    repo = SqlAlchemyRepository(session_factory)
    fav = Favourite(1, my_user.id, my_recipe.id, datetime.now())
    repo.add_favourite(fav)

    favourites = repo.get_favourites_for_user(my_user.id)
    assert len(favourites) == 1
    assert favourites[0].recipe_id == my_recipe.id

def test_repository_prevents_duplicate_favourite(session_factory, my_user, my_recipe):
    repo = SqlAlchemyRepository(session_factory)
    fav1 = Favourite(1, my_user.id, my_recipe.id, datetime(2024, 1, 1))
    fav2 = Favourite(2, my_user.id, my_recipe.id, datetime(2024, 1, 2))

    repo.add_favourite(fav1)
    repo.add_favourite(fav2)

    favourites = repo.get_favourites_for_user(my_user.id)
    assert len(favourites) == 1

def test_repository_can_remove_favourite(session_factory, my_user, my_recipe):
    repo = SqlAlchemyRepository(session_factory)
    fav = Favourite(1, my_user.id, my_recipe.id, datetime(2024, 1, 1))
    repo.add_favourite(fav)

    repo.remove_favourite(my_user.id, my_recipe.id)
    favourites = repo.get_favourites_for_user(my_user.id)
    assert favourites == []

def test_repository_can_generate_new_favourite_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    fav_id = repo.get_new_favourite_id()
    assert isinstance(fav_id, int)
    assert fav_id >= 1


# Nutrition tests
def test_repository_can_add_nutrition(session_factory, my_nutrition):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_nutrition(my_nutrition)

    assert repo.get_nutrition_by_id(1) == my_nutrition

def test_repository_can_get_nutrition_by_id(session_factory, my_nutrition):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_nutrition(my_nutrition)
    found = repo.get_nutrition_by_id(1)
    assert found == my_nutrition

def test_repository_can_retrieve_nutritions(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    nutritions = repo.get_nutritions()

    assert nutritions[0].id == 1

def test_repository_can_add_multiple_nutritions(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    nutritions = [
        Nutrition(5000, 250.0, 10.0, 3.0, 30.0, 200.0, 30.0, 5.0, 12.0, 8.0),
        Nutrition(5001, 120.0, 4.0, 1.0, 10.0, 90.0, 18.0, 2.0, 5.0, 4.0),
        Nutrition(5003, 400.0, 18.0, 6.0, 55.0, 350.0, 42.0, 7.0, 14.0, 15.0),
    ]

    repo.add_multiple_nutritions(nutritions)

    assert repo.get_nutrition_by_id(5000) == nutritions[0]
    assert repo.get_nutrition_by_id(5001) == nutritions[1]
    assert repo.get_nutrition_by_id(5003) == nutritions[2]

# Recipe tests
def test_repository_can_add_recipe(session_factory, my_recipe):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_recipe(my_recipe)

    assert repo.get_recipe_by_id(38) == my_recipe

def test_repository_can_get_recipe_by_id(session_factory, my_recipe):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_recipe(my_recipe)
    found = repo.get_recipe_by_id(38)
    assert found == my_recipe

def test_repository_can_retrieve_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    recipes = repo.get_recipes()

    assert recipes[0].id == 38

def test_repository_can_get_number_of_recipes(session_factory, my_recipe):
    repo = SqlAlchemyRepository(session_factory)
    recipes = repo.get_recipes()
    expected = len(recipes)

    number_of_recipes = repo.get_number_of_recipes()
    assert expected == number_of_recipes

def test_get_recipes_by_name(session_factory, my_recipe):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_recipe(my_recipe)
    result = repo.get_recipes_by_name("Low-Fat Berry Blue Frozen Dessert")
    assert result == [my_recipe]

def test_get_recipes_by_category(session_factory, my_recipe):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_recipe(my_recipe)
    result = repo.get_recipes_by_category(my_recipe.category.name)
    assert result == [my_recipe]

def test_get_recipes_by_author(session_factory, my_recipe):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_recipe(my_recipe)
    result = repo.get_recipes_by_author(my_recipe.author.name)
    assert result == [my_recipe]

def test_add_multiple_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    a1 = Author(101, "Alice")
    c1 = Category(201, "Desserts")
    n1 = Nutrition(5000, 250.0, 10.0, 3.0, 30.0, 200.0, 30.0, 5.0, 12.0, 8.0)
    r1 = Recipe(3001, "Blueberry Froyo", a1, 0, 0, 0, datetime(2023, 1, 1), "Quick blueberry frozen yogurt.", [], c1, [], n1, 4, "1 batch", [])

    a2 = Author(102, "Bob")
    c2 = Category(202, "Mains")
    n2 = Nutrition(5001, 420.0, 18.0, 6.0, 55.0, 350.0, 42.0, 7.0, 14.0, 15.0)
    r2 = Recipe(3002, "Garlic Chicken", a2, 15, 10, 25, datetime(2023, 2, 2), "Simple garlicky chicken.", [], c2, [], n2, 2, "2 servings", [])

    recipes = [r1, r2]
    repo.add_multiple_recipes(recipes)

    assert repo.get_recipe_by_id(3001) == recipes[0]
    assert repo.get_recipe_by_id(3002) == recipes[1]

# Review tests
# TODO finish these off
def test_repository_can_add_review(session_factory, my_user, my_recipe):
    repo = SqlAlchemyRepository(session_factory)
    review = Review(1, my_user.id,  datetime(2024, 1, 1), my_recipe.id, 5, "wowsogood")
    repo.add_review(review)

    reviews = repo.get_reviews_for_recipe(my_recipe.id)
    assert len(reviews) == 1
    assert reviews[0].comment == "wowsogood"

def test_repository_can_remove_review(session_factory, my_user, my_recipe):
    repo = SqlAlchemyRepository(session_factory)
    review = Review(1, my_user.id,  datetime(2024, 1, 1), my_recipe.id, 5, "wowsogood")
    repo.add_review(review)
    repo.remove_review(my_user.id, 1)

    reviews = repo.get_reviews_for_recipe(my_recipe.id)
    assert len(reviews) == 0

def test_repository_can_get_reviews_for_user(session_factory, my_user, my_recipe):
    repo = SqlAlchemyRepository(session_factory)
    review = Review(1, my_user.id,  datetime(2024, 1, 1), my_recipe.id, 5, "wowsogood")
    repo.add_review(review)

    reviews = repo.get_reviews_for_user(my_user.id)
    assert len(reviews) == 1
    assert reviews[0].rating == 5


# User tests
# TODO finish these off
def test_repository_can_add_user(session_factory, my_user):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(my_user)
    found = repo.get_user_by_id(my_user.id)
    assert found == my_user

def test_repository_can_get_user_by_id(session_factory, my_user):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(my_user)
    found = repo.get_user_by_id(my_user.id)
    assert found.id == my_user.id

def test_repository_returns_none_for_nonexistent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    found = repo.get_user_by_id(9999)
    assert found is None

def test_repository_can_retrieve_user(session_factory, my_user):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(my_user)
    user = repo.get_user(my_user.username)
    assert user.username == my_user.username


# RecipeImage tests
def test_can_add_recipe_image(session_factory, my_recipe_image):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_recipe_image(my_recipe_image)

    assert repo.get_recipe_image(38, 1) == my_recipe_image

def test_repository_can_get_recipe_image(session_factory, my_recipe_image):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_recipe_image(my_recipe_image)
    found = repo.get_recipe_image(38, 1)
    assert found == my_recipe_image

def test_repository_can_retrieve_recipe_images(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    recipe_images = repo.get_recipe_images()

    assert recipe_images[0].recipe_id == 38
    assert recipe_images[0].position == 1

def test_repository_can_add_multiple_recipe_images(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    recipe_images = [
        RecipeImage(40, "https://x/a.jpg", 1),
        RecipeImage(40, "https://x/b.jpg", 2),
    ]
    repo.add_multiple_recipe_images(recipe_images)

    assert repo.get_recipe_image(40, 1) == recipe_images[0]
    assert repo.get_recipe_image(40, 2) == recipe_images[1]

# RecipeIngredient tests
def test_can_add_recipe_ingredient(session_factory, my_recipe_ingredient):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_recipe_ingredient(my_recipe_ingredient)
    assert repo.get_recipe_ingredient(38, 1) == my_recipe_ingredient

def test_repository_can_get_recipe_ingredient(session_factory, my_recipe_ingredient):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_recipe_ingredient(my_recipe_ingredient)
    found = repo.get_recipe_ingredient(38, 1)
    assert found == my_recipe_ingredient

def test_repository_can_retrieve_recipe_ingredients(session_factory, my_recipe_ingredient):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_recipe_ingredient(my_recipe_ingredient)
    recipe_ingredients = repo.get_recipe_ingredients()
    assert recipe_ingredients[0].recipe_id == 38
    assert recipe_ingredients[0].position == 1

def test_repository_can_add_multiple_recipe_ingredients(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    ings = [
        RecipeIngredient(40, "4", "blueberries", 1),
        RecipeIngredient(40, "1/4", "granulated sugar", 2),
    ]
    repo.add_multiple_recipe_ingredients(ings)
    assert repo.get_recipe_ingredient(40, 1) == ings[0]
    assert repo.get_recipe_ingredient(40, 2) == ings[1]

# RecipeInstruction tests
def test_can_add_recipe_instruction(session_factory, my_recipe_instruction):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_recipe_instruction(my_recipe_instruction)
    assert repo.get_recipe_instruction(38, 1) == my_recipe_instruction

def test_repository_can_get_recipe_instruction(session_factory, my_recipe_instruction):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_recipe_instruction(my_recipe_instruction)
    found = repo.get_recipe_instruction(38, 1)
    assert found == my_recipe_instruction

def test_repository_can_retrieve_recipe_instructions(session_factory, my_recipe_instruction):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_recipe_instruction(my_recipe_instruction)
    recipe_instructions = repo.get_recipe_instructions()
    assert recipe_instructions[0].recipe_id == 38
    assert recipe_instructions[0].position == 1

def test_repository_can_add_multiple_recipe_instructions(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    instrs = [
        RecipeInstruction(40, "Chop onions.", 1),
        RecipeInstruction(40, "Sauté until soft.", 2),
    ]
    repo.add_multiple_recipe_instructions(instrs)
    assert repo.get_recipe_instruction(40, 1) == instrs[0]
    assert repo.get_recipe_instruction(40, 2) == instrs[1]
