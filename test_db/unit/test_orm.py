from datetime import datetime

from sqlalchemy import text
from recipe import SqlAlchemyRepository
from recipe.domainmodel.author import Author
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.recipe import Review
from recipe.domainmodel.user import User
from recipe.domainmodel.nutrition import Nutrition

#helper

from sqlalchemy import text

def insert_nutrition(empty_session, nutrition):
    empty_session.execute(
        text(
            f'INSERT INTO nutrition (id, calories, fat, saturated_fat, cholesterol, sodium, '
            f'carbohydrates, fiber, sugar, protein) VALUES ('
            f'{nutrition.id}, '
            f'{nutrition.calories}, '
            f'{nutrition.fat}, '
            f'{nutrition.saturated_fat}, '
            f'{nutrition.cholesterol}, '
            f'{nutrition.sodium}, '
            f'{nutrition.carbohydrates}, '
            f'{nutrition.fiber}, '
            f'{nutrition.sugar}, '
            f'{nutrition.protein})'
        )
    )
    row = empty_session.execute(
        text('SELECT id FROM nutrition ORDER BY id DESC LIMIT 1')
    ).fetchone()
    return row[0]


def insert_user(empty_session, user):
    empty_session.execute(
        text(
            f'INSERT INTO users (id, username, password) VALUES ({user.id}, "{user.username}", "{user.password}")'
        )
    )
    row = empty_session.execute(
        text('SELECT id FROM users ORDER BY id DESC LIMIT 1')
    ).fetchone()
    return row[0]

def insert_user_favourite(empty_session, user, recipe):
    empty_session.execute(
        text(
            f'INSERT INTO favourites (user_id, recipe_id, date_added) VALUES ({user.id}, {recipe.id}, "{datetime.now()}")'
        )
    )


def insert_category(empty_session, category):
    empty_session.execute(
        text(f'INSERT INTO categories (id, name) VALUES ({category.id}, "{category.name}")')
    )
    row = empty_session.execute(text('SELECT id FROM categories ORDER BY id DESC LIMIT 1')).fetchone()
    return row[0]



def insert_recipe(empty_session, recipe):
    empty_session.execute(
        text(
            'INSERT INTO recipes (id, name, author_id, description, nutrition_id, '
            'cook_time, preparation_time, total_time, created_date, servings, recipe_yield, category_id) '
            'VALUES ('
            f'{recipe.id}, '
            f'"{recipe.name}", '
            f'{recipe.author.id}, '
            f'"{recipe.description}", '
            f'{recipe.nutrition.id}, '
            f'{recipe.cook_time}, '
            f'{recipe.preparation_time}, '
            f'{recipe.total_time}, '
            f'"{recipe.created_date}", '
            f'{recipe.servings}, '
            f'"{recipe.recipe_yield}", '
            f'{recipe.category.id}'
            ')'
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




def test_loading_of_authors(empty_session, my_author):
    author_key = insert_author(empty_session, my_author)
    fetched_author = empty_session.execute(text('SELECT id, name FROM authors')).fetchone()
    assert fetched_author == (my_author.id, my_author.name)
    assert author_key == fetched_author[0]

def test_saving_of_author(empty_session, my_author):
    insert_author(empty_session, my_author)
    empty_session.commit()
    rows = empty_session.query(Author).one()
    assert rows == my_author


def test_author_recipe_relationship(empty_session, my_author, my_recipe):
    insert_recipe(empty_session, my_recipe)
    insert_author(empty_session, my_author)
    empty_session.commit()

    #rows = list(empty_session.execute(text('SELECT id, author_id FROM recipes')))
    rows = empty_session.query(Recipe).one()
    assert rows == my_recipe
    #assert rows == [(recipe.id, author.id)]
    assert my_author.recipes == [my_recipe]


def test_loading_of_recipe(empty_session, my_recipe):
    recipe_key = insert_recipe(empty_session, my_recipe)
    fetched_recipe = empty_session.query(Recipe).one()

    # Confirm the fetched recipe has the same recipe_id as expected
    assert recipe_key == fetched_recipe.id
    # Test the fetched recipe is identical to the recipe we created in advance
    assert my_recipe == fetched_recipe


def test_saving_of_recipe(empty_session, my_recipe):
    empty_session.add(my_recipe)
    empty_session.commit()

    rows = list(empty_session.execute(
        text('SELECT id, name, author_id, description, nutrition_id '
             'FROM recipes')))

    # Confirm all the recipe attributes were saved successfully including foreign keys
    assert rows == [(
        my_recipe.id,
        my_recipe.name,
        my_recipe.author.id,
        my_recipe.description,
        my_recipe.nutrition.id,
    )]


def test_loading_of_users(empty_session):
    users = list()
    users.append(User(2, "mr", "password"))
    users.append(User(3, "dob", "secret"))

    for user in users:
        insert_user(empty_session, user)

    expected = [
        User(2, "mr", "password"),
        User(3, "dob", "secret")
    ]

    fetched_users = empty_session.query(User).all()

    assert fetched_users == expected


def test_nutrition_recipe_relationship(empty_session, my_recipe, my_nutrition):
    insert_nutrition(empty_session, my_nutrition)
    insert_recipe(empty_session, my_recipe)
    empty_session.commit()

    fetched_recipe = empty_session.query(Recipe).one()
    assert fetched_recipe.nutrition == my_nutrition

def test_saving_of_favourite(empty_session, my_user, my_recipe, my_favourite):
    empty_session.add(my_user)
    empty_session.add(my_recipe)
    empty_session.add(my_favourite)
    empty_session.commit()

    rows = list(empty_session.execute(
        text('SELECT user_id, recipe_id FROM favourites')
    ))

    assert rows == [(my_user.id, my_recipe.id)]

def test_saving_of_review(empty_session, my_user, my_recipe, my_review):
    empty_session.add(my_user)
    empty_session.add(my_recipe)
    empty_session.add(my_review)
    empty_session.commit()

    rows = list(empty_session.execute(
        text('SELECT user_id, recipe_id, rating, comment FROM reviews')
    ))

    assert rows == [(my_user.id, my_recipe.id, my_review.rating, my_review.comment)]


def test_user_review_relationship(empty_session, my_user, my_recipe, my_review):
    insert_user(empty_session, my_user)
    insert_recipe(empty_session, my_recipe)
    empty_session.add(my_review)
    empty_session.commit()

    fetched_review = empty_session.query(Review).one()
    fetched_user = empty_session.query(User).one()
    fetched_recipe = empty_session.query(Recipe).one()

    assert fetched_review in fetched_user._User__reviews
    assert fetched_review in fetched_recipe._Recipe__reviews



def test_multiple_reviews(empty_session, my_user, my_recipe):
    empty_session.add(my_user)
    empty_session.add(my_recipe)

    review1 = Review(1, my_user.id, datetime.now(), my_recipe.id, 5, "bestever")
    review2 = Review(2, my_user.id, datetime.now(), my_recipe.id, 4, "decent")
    empty_session.add_all([review1, review2])
    empty_session.commit()

    rows = list(empty_session.execute(
        text('SELECT user_id, recipe_id, rating, comment FROM reviews ORDER BY rating DESC')
    ))

    assert rows == [
        (my_user.id, my_recipe.id, 5, "bestever"),
        (my_user.id, my_recipe.id, 4, "decent")
    ]

def test_recipe_category_relationship(empty_session, my_recipe, my_category):
    empty_session.add(my_category)
    empty_session.add(my_recipe)
    empty_session.commit()

    fetched_recipe = empty_session.query(Recipe).one()
    assert fetched_recipe in my_category.recipes
    assert my_category.recipes == [my_recipe]


def test_recipe_without_nutrition(empty_session, my_recipe):
    my_recipe.nutrition = None
    empty_session.add(my_recipe)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT id, nutrition_id FROM recipes')))
    assert rows[0][1] is None


def test_multiple_users_favourites(empty_session, my_user, my_recipe):

    my_user2 = User(2, "bob", "snake123")
    empty_session.add_all([my_user, my_user2, my_recipe])

    fav1 = Favourite(3,my_user.id, my_recipe.id, datetime.now())
    fav2 = Favourite(4, my_user2.id, my_recipe.id, datetime.now())

    empty_session.add_all([fav1, fav2])
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT user_id, recipe_id FROM favourites ORDER BY user_id')))
    assert rows == [
        (my_user.id, my_recipe.id),
        (my_user2.id, my_recipe.id),
    ]



def test_user_favourite_relationship(empty_session, my_user, my_recipe):
    insert_user(empty_session, my_user)
    insert_recipe(empty_session, my_recipe)
    insert_user_favourite(empty_session, my_user, my_recipe)
    empty_session.commit()

    row = empty_session.execute(
        text('SELECT user_id, recipe_id FROM favourites')
    ).fetchone()

    assert row == (my_user.id, my_recipe.id)



def test_saving_of_user(empty_session, my_user):
    empty_session.add(my_user)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT id, username, password FROM users')))
    assert rows == [(my_user.id, my_user.username, my_user.password)]
