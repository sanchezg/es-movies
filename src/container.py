from dependency_injector import containers, providers

import asyncio
from elasticsearch import AsyncElasticsearch

from src import settings
# from src.domain.services.movies import 
from src.infra.repositories.es import ESRepo
from src.infra.repositories.movies import ESMovieRepo


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".application.controllers"])

    # DB client
    es_client = providers.Factory(
        AsyncElasticsearch,
        settings.ES_URI,
    )

    # Repositories
    url_repo = providers.Factory(ESMovieRepo, es_client)

    # Services
    pass
