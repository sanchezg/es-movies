import pytest
from dependency_injector.providers import Factory
from fastapi.testclient import TestClient

from src.main import app as main_app
from src.tests.fakes import MockESMovieRepo, MockMoviesFetcher


@pytest.fixture
def app():
    with main_app.container.movies_fetcher.override(Factory(MockMoviesFetcher)):  # type: ignore
        with main_app.container.movies_repo.override(Factory(MockESMovieRepo)):  # type: ignore
            yield main_app


@pytest.fixture
def test_client(app):
    with TestClient(app) as client:
        yield client
