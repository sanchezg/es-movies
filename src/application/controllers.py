from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, responses, status
from fastapi.templating import Jinja2Templates

from src.container import Container
from src.domain.model import Movie, MovieQuery
from src.domain.repository import MovieRepo
from logging import getLogger

from src.domain.services import MoviesFetcher

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
    year: int | None = None,
    movies_lookup: MovieRepo = Depends(Provide[Container.movies_repo]),
) -> Movie | list[Movie] | str:
    documents = await movies_lookup.get(title=title, year=year)
    if not documents:
        return responses.Response("No results", status_code=status.HTTP_404_NOT_FOUND)  # type: ignore
    return documents


@router.post("/movies/fetcher/", response_model=Movie)
@inject
async def post_url(
    data: MovieQuery | None = None,
    movies_fetcher: MoviesFetcher = Depends(Provide[Container.movies_fetcher]),
    movies_store: MovieRepo = Depends(Provide[Container.movies_repo]),
):
    title = data.title if data else None
    result = await movies_fetcher(title=title)
    if result:
        await movies_store.delete(all=True)
    count = await movies_store.insert(documents=result)
    logger.debug(f"Inserted {count} documents")
    return responses.JSONResponse(content=result, status_code=status.HTTP_200_OK)
