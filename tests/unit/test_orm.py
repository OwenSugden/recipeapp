from datetime import datetime

from sqlalchemy import text
from recipe import SqlAlchemyRepository
from recipe.domainmodel.author import Author
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.nutrition import Nutrition


def make_author():
    author = Author(1, 'Bob')
    return author


def make_nutrition() -> Nutrition:
    nutrition = Nutrition(
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
    )
    return nutrition


def make_recipe() -> Recipe:
    author = make_author()
    nutrition = make_nutrition()
    recipe = Recipe(5001, 'Test recipe 1', author, 0, 0,
                    datetime(2023, 1, 1), 'Test description', [], "",
                    ['1 cup'], ['flour'], 4.5, nutrition, '4',
                    '1 batch', ['Mix ingredients'])

    return recipe


def insert_recipe(empty_session, recipe):
    empty_session.execute(
        text(
            'INSERT INTO recipes (id, name, author_id, '
            'description, nutrition_id) VALUES '
            f'({recipe.id}, "{recipe.name}", {recipe.author.id}, '
            f'"{recipe.description}", {recipe.nutrition.id})'
        )
)
    row = empty_session.execute(text('SELECT id FROM recipes ORDER BY id DESC LIMIT 1')).fetchone()
    return row[0]


def insert_author(empty_session, author: Author):
    empty_session.execute(
        text('INSERT INTO authors (id, name) VALUES '
            f'({author.id}, "{author.name}" )'''))
    row = empty_session.execute(text('SELECT id FROM authors ORDER BY id DESC LIMIT 1')).fetchone()
    return row[0]

def test_loading_of_authors(empty_session):
    author = make_author()
    author_key = insert_author(empty_session, author)
    fetched_author = empty_session.execute(text('SELECT id, name FROM authors')).fetchone()
    assert fetched_author == (author.id, author.name)
    assert author_key == fetched_author[0]

def test_saving_of_author(empty_session):
    author = make_author()
    insert_author(empty_session, author)
    empty_session.commit()
    #rows = list(empty_session.execute(text('SELECT id, name FROM authors')))
    rows = empty_session.query(Author).one()
    assert rows == author
    #assert rows == [(author.id, author.name)]


def test_author_recipe_relationship(empty_session):
    author = make_author()
    recipe = make_recipe()
    recipe.author = author
    insert_recipe(empty_session, recipe)
    insert_author(empty_session, author)
    empty_session.commit()

    #rows = list(empty_session.execute(text('SELECT id, author_id FROM recipes')))
    rows = empty_session.query(Recipe).one()
    assert rows == recipe
    #assert rows == [(recipe.id, author.id)]
    assert author.recipes == [recipe]


def test_loading_of_recipe(empty_session):
    recipe = make_recipe()
    recipe_key = insert_recipe(empty_session, recipe)
    fetched_recipe = empty_session.query(Recipe).one()

    # Confirm the fetched recipe has the same recipe_id as expected
    assert recipe_key == fetched_recipe.id
    # Test the fetched recipe is identical to the recipe we created in advance
    assert recipe == fetched_recipe


def test_saving_of_recipe(empty_session):
    recipe = make_recipe()
    empty_session.add(recipe)
    empty_session.commit()

    rows = list(empty_session.execute(
        text('SELECT id, name, author_id, description, nutrition_id '
             'FROM recipes')))

    # Confirm all the recipe attributes were saved successfully including foreign keys
    assert rows == [(
        recipe.id,
        recipe.name,
        recipe.author.id,
        recipe.description,
        recipe.nutrition.id,
    )]

    #TODO
    def test_review_recipe_relationship(empty_session):
        pass

    #TODO
    def test_category_recipe_relationship(empty_session):
        pass

    #TODO
    def test_user_review_relationship(empty_session):
        pass

    #TODO
    def test_user_favourite_relationship(empty_session):
        pass

    #TODO
    def test_recipe_ingredient_recipe_relationship(empty_session):
        pass

    #TODO
    def test_nutrition_recipe_relationship(empty_session):
        pass

