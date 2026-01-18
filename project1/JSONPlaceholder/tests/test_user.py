import json
import pytest


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
    assert isinstance(data["name"], str)
    assert isinstance(data["email"], str)

    assert isinstance(data["address"], dict)
    assert {"city", "street", "zipcode", "geo"}.issubset(data["address"].keys())

    assert isinstance(data["address"]["geo"], dict)
    assert {"lat", "lng"}.issubset(data["address"]["geo"].keys())

    assert isinstance(data["company"], dict)
    assert {"name", "catchPhrase", "bs"}.issubset(data["company"].keys())

    print(json.dumps(data, indent=4))
