from jsonschema import validate
from jsonschema.exceptions import ValidationError

import pytest
import json

from ..schemas.user_schema import USER_SCHEMA


@pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
def test_get_user_by_id_returns_valid_user(base_url, api_client, user_id):
    response = api_client.get(f"{base_url}/users/{user_id}")

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    data = response.json()

    assert isinstance(data, dict)

    expected_fields = {
        "id",
        "name",
        "username",
        "email",
        "address",
        "phone",
        "website",
        "company",
    }
    assert expected_fields.issubset(data.keys())

    assert isinstance(data["id"], int)
    assert data["id"] == user_id

    assert isinstance(data["name"], str)
    assert isinstance(data["email"], str)

    assert isinstance(data["address"], dict)
    assert {"city", "street", "zipcode", "geo"}.issubset(data["address"].keys())

    assert isinstance(data["address"]["geo"], dict)
    assert {"lat", "lng"}.issubset(data["address"]["geo"].keys())

    assert isinstance(data["company"], dict)
    assert {"name", "catchPhrase", "bs"}.issubset(data["company"].keys())

    print(json.dumps(data, indent=4))


def test_users_have_unique_emails(base_url, api_client):
    response = api_client.get(f"{base_url}/users")

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    users = response.json()
    assert isinstance(users, list)

    emails = [user["email"] for user in users]

    assert len(emails) == len(set(emails)), "Duplicate emails found"


def test_create_user(base_url, api_client):
    body = {
        "name": "Evgenii Shikunov",
        "username": "Evgenii",
        "email": "mytestemail@mail.com",
        "address": {
            "street": "test_street",
            "suite": "test_suite",
            "city": "Saransk",
            "zipcode": "23542-252",
            "geo": {
                "lat": "12.12",
                "lng": "15.15",
            },
        },
        "phone": "234234",
        "website": "myweb.com",
        "company": {
            "name": "Evg",
            "catchPhrase": "test_catch_phrase",
            "bs": "test_bs",
        },
    }

    response = api_client.post(f"{base_url}/users", json=body)

    assert response.status_code == 201
    assert response.headers["Content-Type"].startswith('application/json')

    data = response.json()

    assert isinstance(data, dict)

    expected_fields = {
        "id",
        "name",
        "username",
        "email",
        "address",
        "phone",
        "website",
        "company",
    }

    assert expected_fields.issubset(data.keys())

    assert isinstance(data["id"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["username"], str)
    assert isinstance(data["address"], dict)

    print(json.dumps(data, indent=4))


def test_user_schema(base_url, api_client):
    response = api_client.get(f'{base_url}/users/1')

    assert response.headers["Content-Type"].startswith('application/json')

    data = response.json()

    try:
        validate(instance=data, schema=USER_SCHEMA)
    except ValidationError as e:
        print(e)

