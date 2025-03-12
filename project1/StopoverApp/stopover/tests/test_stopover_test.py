import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from stopover.models import Stopover


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(email="testuser@example.com"):
        User = get_user_model()
        return User.objects.create(email=email, fam="Евгеньев", name="Евгений", phone="+79001234567")
    return make_user


@pytest.fixture
def create_stopover(db, create_user):
    def make_stopover(title="Тестовый Перевал", status="new"):
        user = create_user()
        return Stopover.objects.create(title=title, beauty_title="Перевал", user=user, status=status)
    return make_stopover


def test_get_stopover_list(api_client, create_stopover):
    create_stopover()
    response = api_client.get("/api/stopover-list/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_stopover_by_id(api_client, create_stopover):
    stopover = create_stopover()
    response = api_client.get(f"/get-stopover/{stopover.id}")
    assert response.status_code == 200
    assert response.json()["title"] == stopover.title


def test_create_stopover(api_client, create_user):
    user = create_user()
    data = {
        "beauty_title": "Гора",
        "title": "Эльбрус",
        "user": {"email": user.email},
        "status": "new"
    }
    response = api_client.post("/create-stopover/", data, format="json")
    assert response.status_code == 201
    assert Stopover.objects.filter(title="Эльбрус").exists()


def test_patch_stopover(api_client, create_stopover):
    stopover = create_stopover()
    response = api_client.patch(f"/patch-stopover/{stopover.id}", {"title": "Новый Тестовый Перевал"}, format="json")
    assert response.status_code == 200
    stopover.refresh_from_db()
    assert stopover.title == "Новый Тестовый Перевал"


def test_filter_stopovers_by_user(api_client, create_user, create_stopover):
    user = create_user(email="filter@example.com")
    create_stopover(title="Фильтруемый Перевал")
    create_stopover(title="Фильтрованный Перевал", status="accepted")
    response = api_client.get(f"/get-stopover/?user__email={user.email}")
    assert response.status_code == 200
    assert len(response.json()) >= 2
