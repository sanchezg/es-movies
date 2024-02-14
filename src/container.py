from dependency_injector import containers, providers

from elasticsearch import AsyncElasticsearch

from src import settings
from src.domain.services import MoviesFetcher
from src.infra.repositories.movies import ESMovieRepo


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".application.controllers"])

    # DB client
    es_client = providers.Factory(
        AsyncElasticsearch,
        settings.ES_URI,
    )

    # Repositories
    movies_repo = providers.Factory(ESMovieRepo, es_client)

    # Services
    movies_fetcher = providers.Factory(MoviesFetcher)
