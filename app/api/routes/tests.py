from typing import Optional

from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
    },
]


@router.get("/recipe/{rid}", status_code=200)
def get_recipe_by_id(*, rid: int) -> dict:
    # for recipe in RECIPES:
    #     if recipe["id"] == rid:
    #         return recipe
    # return {"msg": "Recipe not found"}
    result = [recipe for recipe in RECIPES if recipe["id"] == rid]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=500, detail="Recipe not found")


@router.get("/search", status_code=200)
def search_recipes(
        keyword: Optional[str] = None, max_results: int = Query(..., le=50)
) -> dict:
    """
    Search for recipes based on label keyword
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": RECIPES[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)
    return {"results": list(results)[:max_results]}
