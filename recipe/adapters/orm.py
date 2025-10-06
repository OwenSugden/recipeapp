from datetime import datetime

from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import registry, relationship

from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.comment import Comment
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.rating import Rating
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe_ingredient import RecipeIngredient
from recipe.domainmodel.recipe_instruction import RecipeInstruction
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User

mapper_registry = registry()

# Recipes table
recipes_table = Table(
    'recipes', mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('description', Text, nullable=False),
    Column('cook_time', Integer, nullable=False),
    Column('preparation_time', Integer, nullable=False),
    Column('created_date', DateTime, nullable=False),
    Column('servings', String(255), nullable=False),
    Column('recipe_yield', String(255), nullable=False),
    Column('nutrition_id', Integer, ForeignKey('nutrition.id'), unique=True),
    Column('author_id', Integer, ForeignKey('authors.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

# Recipe images table
recipe_images_table = Table(
    'recipe_images', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), nullable=False),
    Column('url', String(500), nullable=False),
    Column('position', Integer, nullable=False)
)

# Recipe ingredients table
recipe_ingredients_table = Table(
    'recipe_ingredients', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), nullable=False),
    Column('quantity', String(255), nullable=False),
    Column('ingredient', String(255), nullable=False),
    Column('position', Integer, nullable=False)
)

# Recipe instructions table
recipe_instructions_table = Table(
    'recipe_instructions', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), nullable=False),
    Column('step', String(255), nullable=False),
    Column('position', Integer, nullable=False)
)

# Nutrition table
nutrition_table = Table(
    'nutrition', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('calories', Float, nullable=False),
    Column('fat', Float, nullable=False),
    Column('saturated_fat', Float, nullable=False),
    Column('cholesterol', Float, nullable=False),
    Column('sodium', Float, nullable=False),
    Column('carbohydrates', Float, nullable=False),
    Column('fiber', Float, nullable=False),
    Column('sugar', Float, nullable=False),
    Column('protein', Float, nullable=False)
)

# Authors table
authors_table = Table(
    'authors', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

# Category table
categories_table = Table(
    'categories', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

# Favourite table
favourites_table = Table(
    'favourites', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), nullable=False),
    Column('date_added', DateTime, nullable=False)
)

# Comment table
comments_table = Table(
    'comments', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('text', Text, nullable=False),
    Column('timestamp', DateTime, nullable=False),
    Column('user_name', String(255), nullable=False)
)

# Rating table
ratings_table = Table(
    'ratings', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('user_name', String(255), nullable=False),
    Column('value', Integer, nullable=False)
)

# User table
users_table = Table(
    'users', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), nullable=False),
    Column('password', String(255), nullable=False),
)

# ORM Mappings
def map_model_to_tables():
    # Recipe mapping
    mapper_registry.map_imperatively(Recipe, recipes_table, properties={
        '_Recipe__id': recipes_table.c.id,
        '_Recipe__name': recipes_table.c.name,
        '_Recipe__description': recipes_table.c.description,
        '_Recipe__cook_time': recipes_table.c.cook_time,
        '_Recipe__preparation_time': recipes_table.c.preparation_time,
        '_Recipe__created_date': recipes_table.c.created_date,
        '_Recipe__servings': recipes_table.c.servings,
        '_Recipe__recipe_yield': recipes_table.c.recipe_yield,
        '_Recipe__nutrition': relationship(Nutrition, back_populates='_Nutrition__recipe', uselist=False),
        '_Recipe__author': relationship(Author, back_populates='_Author__recipes'),
        '_Recipe__category': relationship(Category, back_populates='_Category__recipes'),
        '_Recipe__images': relationship(RecipeImage, back_populates='_RecipeImage__recipe', cascade='all, delete-orphan'),
        '_Recipe__ingredients': relationship(RecipeIngredient, back_populates='_RecipeIngredient__recipe', cascade='all, delete-orphan'),
        '_Recipe__instructions': relationship(RecipeInstruction, back_populates='_RecipeInstruction__recipe', cascade='all, delete-orphan'),
        '_Recipe__favourites': relationship(Favourite, back_populates='_Favourite__recipe', cascade='all, delete-orphan'),
        '_Recipe__comments': relationship(Comment, back_populates='_Comment__recipe', cascade='all, delete-orphan'),
        '_Recipe__ratings': relationship(Rating, back_populates='_Rating__recipe', cascade='all, delete-orphan')
    })

    # RecipeImage mapping
    mapper_registry.map_imperatively(RecipeImage, recipe_images_table, properties={
        '_RecipeImage__id': recipe_images_table.c.id,
        '_RecipeImage__recipe_id': recipe_images_table.c.recipe_id,
        '_RecipeImage__url': recipe_images_table.c.url,
        '_RecipeImage__position': recipe_images_table.c.position,
        '_RecipeImage__recipe': relationship(Recipe, back_populates='_Recipe__images')
    })

    # RecipeIngredient mapping
    mapper_registry.map_imperatively(RecipeIngredient, recipe_ingredients_table, properties={
        '_RecipeIngredient__id': recipe_ingredients_table.c.id,
        '_RecipeIngredient__recipe_id': recipe_ingredients_table.c.recipe_id,
        '_RecipeIngredient__quantity': recipe_ingredients_table.c.quantity,
        '_RecipeIngredient__ingredient': recipe_ingredients_table.c.ingredient,
        '_RecipeIngredient__position': recipe_ingredients_table.c.position,
        '_RecipeIngredient__recipe': relationship(Recipe, back_populates='_Recipe__ingredients')
    })

    # RecipeInstruction mapping
    mapper_registry.map_imperatively(RecipeInstruction, recipe_instructions_table, properties={
        '_RecipeInstruction__id': recipe_instructions_table.c.id,
        '_RecipeInstruction__recipe_id': recipe_instructions_table.c.recipe_id,
        '_RecipeInstruction__step': recipe_instructions_table.c.step,
        '_RecipeInstruction__position': recipe_instructions_table.c.position,
        '_RecipeInstruction__recipe': relationship(Recipe, back_populates='_Recipe__instructions')
    })

    # Nutrition mapping
    mapper_registry.map_imperatively(Nutrition, nutrition_table, properties={
        '_Nutrition__id': nutrition_table.c.id,
        '_Nutrition__calories': nutrition_table.c.calories,
        '_Nutrition__fat': nutrition_table.c.fat,
        '_Nutrition__saturated_fat': nutrition_table.c.saturated_fat,
        '_Nutrition__cholesterol': nutrition_table.c.cholesterol,
        '_Nutrition__sodium': nutrition_table.c.sodium,
        '_Nutrition__carbohydrates': nutrition_table.c.carbohydrates,
        '_Nutrition__fiber': nutrition_table.c.fiber,
        '_Nutrition__sugar': nutrition_table.c.sugar,
        '_Nutrition__protein': nutrition_table.c.protein,
        '_Nutrition__recipe': relationship(Recipe, back_populates='_Recipe__nutrition', uselist=False)
    })

    # Author mapping
    mapper_registry.map_imperatively(Author, authors_table, properties={
        '_Author__id': authors_table.c.id,
        '_Author__name': authors_table.c.name,
        '_Author__recipes': relationship(Recipe, back_populates='_Recipe__author')
    })

    # Category mapping
    mapper_registry.map_imperatively(Category, categories_table, properties={
        '_Category__id': categories_table.c.id,
        '_Category__name': categories_table.c.name,
        '_Category__recipes': relationship(Recipe, back_populates='_Recipe__category')
    })

    # Favourite mapping
    mapper_registry.map_imperatively(Favourite, favourites_table, properties={
        '_Favourite__id': favourites_table.c.id,
        '_Favourite__user_id': favourites_table.c.user_id,
        '_Favourite__recipe_id': favourites_table.c.recipe_id,
        '_Favourite__date_added': favourites_table.c.date_added,
        '_Favourite__user': relationship(User, back_populates='_User__favourites'),
        '_Favourite__recipe': relationship(Recipe, back_populates='_Recipe__favourites')
    })

    # Comment mapping
    mapper_registry.map_imperatively(Comment, comments_table, properties={
        '_Comment__id': comments_table.c.id,
        '_Comment__recipe_id': comments_table.c.recipe_id,
        '_Comment__user_id': comments_table.c.user_id,
        '_Comment__text': comments_table.c.text,
        '_Comment__timestamp': comments_table.c.timestamp,
        '_Comment__user_name': comments_table.c.user_name,
        '_Comment__recipe': relationship(Recipe, back_populates='_Recipe__comments'),
        '_Comment__user': relationship(User, back_populates='_User__comments')
    })

    # Rating mapping
    mapper_registry.map_imperatively(Rating, ratings_table, properties={
        '_Rating__id': ratings_table.c.id,
        '_Rating__recipe_id': ratings_table.c.recipe_id,
        '_Rating__user_id': ratings_table.c.user_id,
        '_Rating__user_name': ratings_table.c.user_name,
        '_Rating__value': ratings_table.c.value,
        '_Rating__recipe': relationship(Recipe, back_populates='_Recipe__ratings'),
        '_Rating__user': relationship(User, back_populates='_User__ratings')
    })

    # User mapping
    mapper_registry.map_imperatively(User, users_table, properties={
        '_User__id': users_table.c.id,
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__favourites': relationship(Favourite, back_populates='_Favourite__user', cascade='all, delete-orphan'),
        '_User__comments': relationship(Comment, back_populates='_Comment__user', cascade='all, delete-orphan'),
        '_User__ratings': relationship(Rating, back_populates='_Rating__user', cascade='all, delete-orphan')
    })