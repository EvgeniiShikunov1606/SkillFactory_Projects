import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture
def api_client():
    return requests.Session()
