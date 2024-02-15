def test_get_movies(test_client):
    response = test_client.get("/movies/", params={"title": "matrix"})
    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "The Matrix",
            "year": 1999,
            "imdbid": "tt0133093",
        },
        {
            "title": "The Matrix Reloaded",
            "year": 2003,
            "imdbid": "tt0234215",
        },
        {
            "title": "The Matrix Revolutions",
            "year": 2003,
            "imdbid": "tt0242653",
        },
    ]


def test_get_movies_not_found(test_client):
    response = test_client.get("/movies/", params={"title": "notfound"})
    assert response.status_code == 404
    assert response.text == "No results"


def test_get_movies_without_arguments_422(test_client):
    response = test_client.get("/movies/")
    assert response.status_code == 422


def test_post_movies_fetcher(test_client):
    response = test_client.post("/movies/fetcher", json={"title": "matrix"})
    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "The Matrix",
            "year": 1999,
            "imdbid": "tt0133093",
        },
        {
            "title": "The Matrix Reloaded",
            "year": 2003,
            "imdbid": "tt0234215",
        },
        {
            "title": "The Matrix Revolutions",
            "year": 2003,
            "imdbid": "tt0242653",
        },
    ]


def test_post_movies_fetcher_without_arguments(test_client):
    response = test_client.post("/movies/fetcher")
    assert response.status_code == 200
    assert len(response.json()) == 6
