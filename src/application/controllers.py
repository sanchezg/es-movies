from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request, responses, status
from fastapi.templating import Jinja2Templates

# from src import settings
from src.container import Container
from src.domain.model import Movie, MovieQuery
from logging import getLogger

from src.domain.services import MoviesFetcher
# from src.domain.services.movies import MoviesLookup, MoviesFetcher

router = APIRouter()
templates = Jinja2Templates(directory="src/application/templates")

logger = getLogger("default")

@router.get("/", response_class=responses.HTMLResponse)
@inject
async def index(request: Request):
    # Basic index
    return templates.TemplateResponse("index.html", context={"request": {}})


@router.get("/movies/")
@inject
async def get_url(
    title: str,
    year: int,
    # movies_lookup: MoviesLookup = Depends(Provide[Container.movies_lookup]),
):
    # documents = await movies_lookup(q=title, year=year)
    # if documents:
    #     return responses.Response(documents, status_code=status.HTTP_200_OK)
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found")
    return responses.Response("ok", status_code=status.HTTP_200_OK)


@router.post("/movies/fetcher/", response_model=Movie)
@inject
async def post_url(
    data: MovieQuery | None = None,
    movies_fetcher: MoviesFetcher = Depends(Provide[Container.movies_fetcher]),
    # movies_store: MoviesStore = Depends(Provide[Container.movies_store]),
):
    title = data.title if data else None
    result = await movies_fetcher(title=title)
    # await movies_store.save(result)
    return responses.JSONResponse(content=result, status_code=status.HTTP_200_OK)
