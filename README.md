# es-movies

This app fetches movies from `https://jsonmock.hackerrank.com/api/moviesdata/search/` API and provides an API to search for them locally.

After fetching the movies from the API, they are stored in an ElasticSearch DB.

The API docs can be accessed via `/docs/` (example: `http://localhost:8000/docs/`).

# Running instructions

Since this app was implemented using Docker, the best way is to run it with it:

`$ docker-compose -f docker/docker-compose.yml build`
`$ docker-compose -f docker/docker-compose.yml up`

There are a few environment variables that can be set using an `.env.local` file, but I recommend keeping they with default values (unless you want to deploy this in a different environment):

```
ES_URI
ES_CHUNK_SIZE
ES_MAX_SIZE
```

If you want to instead run the app locally, keep in mind you must use Python3.11+, and then install the dependencies with poetry:

`$ pip install poetry`
`$ poetry install --no-root`

# Design

The app is designed using DDD + DI + Repository Pattern. In that way, the business logic (domain) is kept splited away from implementation details (DB chosen).
Using DI (via `dependency-injector` package) we can inject objects into the dependants, and make the higher level modules (application, or domain) independents of lower level modules (infrastructure) by depending only from abstractions.

Having said that, the module structure looks like:

```
.
└── src
    ├── __init__.py
    ├── application
    │   ├── __init__.py
    │   ├── controllers.py
    │   └── templates
    │       └── index.html
    ├── config
    ├── container.py
    ├── domain
    │   ├── __init__.py
    │   ├── interfaces.py
    │   ├── model.py
    │   ├── repository.py
    │   └── services.py
    ├── infra
    │   ├── __init__.py
    │   └── repositories
    │       ├── __init__.py
    │       ├── es.py
    │       └── movies.py
    ├── main.py
    └── settings.py
```

- `application`: contains higher level modules, like controllers methods, which provides the higher level definitions for the API endpoints.
- `domain`: contains business logic modules, mostly in `services.py` where the services fetching and formating data resides. It could be an additional service owner of storing data into the ES DB, but since this procedure is quite simple, it was omited in favor of keeping things simple here. `repository.py` contains the abstractions of the repositories implementation.
- `infra`: contains the lower level modules coupled to infrastructure. Here we have the specific implementation of the repository pattern tied to the specific DB used. Note that if we would like to change the DB (implementation decision), we just need to change the repository implementation here without changing the code in domain.
- `container.py`: additionally to `main.py`, the code here provides the factories for the different providers that are the dependencies injected.

The FastAPI app provides two endpoints:

1. `POST /movies/fetcher/`:

Body params: `title`, `year`

Calls the `https://jsonmock.hackerrank.com/api/moviesdata/search/` using async requests, passing the above query params if provided. If the requested API returns more than 1 page results, the calls are incremented until no pages left.

Note: because of this requirement:

> Every time the endpoint is called, the index is overwritten with the JSON data returned by it.

**All** the documents in the index are removed with every call (if the above request returns at least one document).

2. `GET /movies/`:

Query params: `title`, `year`

Searches the local ES DB for the movies wanted. If no params are provided, all results are returned.

