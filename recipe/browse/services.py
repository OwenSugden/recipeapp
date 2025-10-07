from typing import Dict, List
from recipe.adapters.repository import AbstractRepository

def get_number_of_recipes(repo: AbstractRepository) -> int:
    return repo.get_number_of_recipes()

def get_recipe(repo: AbstractRepository) -> List[dict]:
    recipes = repo.get_recipes()
    recipe_dicts = []
    for recipe in recipes:
        recipe_dicts.append({
            "id": recipe.id,
            "name": recipe.name,
            "author": recipe.author.name,
            "images": recipe.images,
            "category": recipe.category.name if recipe.category else None,
            "time": (recipe.cook_time or 0) + (recipe.preparation_time or 0),
            "nutrition": recipe.nutrition,
            "calories": getattr(recipe.nutrition, "calories", None),
            "protein": getattr(recipe.nutrition, "protein", None),
            "fat": getattr(recipe.nutrition, "fat", None),
            "carbohydrates": getattr(recipe.nutrition, "carbohydrates", None),
        })
    return recipe_dicts

def get_categories(recipes, skip_n=4):
    categories = sorted({r.get("category") for r in recipes if r.get("category")})
    return categories[skip_n:]

def filter_text_and_category(recipes, q, filter_by):
    out = list(recipes)
    if q:
        ql = q.lower()
        out = [r for r in out if ql in ((r.get("name") or "").lower())]
    if filter_by and filter_by.lower() != "all":
        fb = filter_by.lower()
        out = [r for r in out if ((r.get("category") or "").lower() == fb)]
    return out

def apply_numeric_filter(rows: List[dict], key: str, op: str, val) -> List[dict]:
    if val is None or op not in ("lt", "gt"):
        return rows
    if op == "lt":
        return [r for r in rows if (r.get(key) is not None and r[key] < val)]
    else:
        return [r for r in rows if (r.get(key) is not None and r[key] > val)]

def sort_recipes(recipes, sort_option):
    if sort_option == "name":
        return sorted(recipes, key=lambda r: (r.get("name") or "").lower())
    if sort_option == "author":
        return sorted(recipes, key=lambda r: (r.get("author") or "").lower())
    return recipes

def pagination(items, page, per_page):
    total_items = len(items)
    total_pages = max((total_items + per_page - 1) // per_page, 1)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], total_pages, page, total_items

def browse_recipes(repo: AbstractRepository,
                   q: str,
                   filter_by: str,
                   sort_option: str,
                   numeric_filters: Dict[str, tuple[str, int]],
                   page: int,
                   per_page: int) -> dict:

    all_recipes = get_recipe(repo)  # list of dicts

    categories = get_categories(all_recipes, skip_n=4)

    filtered = filter_text_and_category(all_recipes, q, filter_by)
    for key in ("time", "calories", "protein", "fat", "carbohydrates"):
        op, val = numeric_filters.get(key, ("", None))
        filtered = apply_numeric_filter(filtered, key, op, val)
    filtered = sort_recipes(filtered, sort_option)

    recipes_on_page, total_pages, page, total_items = pagination(filtered, page, per_page)

    return {
        "title": "Browse recipe",
        "heading": "Browse recipe",
        "recipes_on_page": recipes_on_page,
        "total_pages": total_pages,
        "page": page,
        "q": q,
        "filter": filter_by,
        "sort_option": sort_option,
        "total_items": total_items,
        "num_recipe": get_number_of_recipes(repo),
        "categories": categories,
        "time_op": numeric_filters.get("time", ("", None))[0],
        "time":    numeric_filters.get("time", ("", None))[1],
        "calories_op": numeric_filters.get("calories", ("", None))[0],
        "calories":    numeric_filters.get("calories", ("", None))[1],
        "protein_op":  numeric_filters.get("protein", ("", None))[0],
        "protein":     numeric_filters.get("protein", ("", None))[1],
        "fat_op":      numeric_filters.get("fat", ("", None))[0],
        "fat":         numeric_filters.get("fat", ("", None))[1],
        "carbohydrates_op": numeric_filters.get("carbohydrates", ("", None))[0],
        "carbohydrates":    numeric_filters.get("carbohydrates", ("", None))[1],
    }
