import sys
sys.path.append("..")

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette import status
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from sentence_transformers import SentenceTransformer

from helper_functions import get_top_user_recipes, get_closest_recipes_with_user_vector, get_user_SVDvector



### FastAPI Stuff
app = FastAPI()

templates = Jinja2Templates(directory="Templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


### Sentance Transformer
model = SentenceTransformer("all-MiniLM-L6-v2")

### User Info
user_id = 1533

### Foods Dictionary
RECIPES = get_top_user_recipes(user_id)

    # {"name": "Fetuccini Alfredo", "type": "pasta"}, 
    # {"name": "Lobster Ravioli", "type": "pasta"}, 
    # {"name": "Deviled Eggs", "type": "Easter Special"}, 
    # {"name": "Upside-down Cake", "type": "Easter Special"}, 
    # {"name": "Chocolate Peanut Butter Ice Cream", "type": "dessert"}
    # ]

search_results = [""]

@app.get("/", response_class=HTMLResponse)
async def read_food_items(request: Request, search: str=""):
    return templates.TemplateResponse("home.html", {"request": request, "message": "Top Recipes for Me", "recipes": RECIPES, "search": search},)


@app.get("/search/", response_class=HTMLResponse)
async def search_window(request: Request):
    # request.search = search_results[-1]
    query = search_results[0]
    results_dictionary = get_closest_recipes_with_user_vector(query)
    return templates.TemplateResponse("search.html", {"request": request, "results_dictionary": results_dictionary, "query": query})
    # return templates.TemplateResponse("search.html", {"request": request, "search": text.split()})


@app.post("/search/", response_class=HTMLResponse)
async def search_window_result(request: Request, query: str=Form(...)):
    search_results[0] = query
    print(search_results)
    return RedirectResponse(url=f"/search/", status_code=status.HTTP_302_FOUND)







