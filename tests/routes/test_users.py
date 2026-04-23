import fastapi

from tests.consts import TEST_CLIENT


def test_create_user():
    first_name = "John"
    last_name = "Doe"
    home_address = "123 Main St."

    response = TEST_CLIENT.post(
        "/users",
        json={"first_name": first_name, "last_name": last_name, "home_address": home_address},
    )

    assert response.status_code == fastapi.status.HTTP_201_CREATED
    data = response.json()
    assert data["first_name"] == first_name
    assert data["last_name"] == last_name
    assert data["home_address"] == home_address
    assert data["id"] == 1


def test_create_user_invalid_data():
    response = TEST_CLIENT.post(
        "/users",
        json={
            "first_name": "",  # Empty string should fail validation
            "last_name": "Doe",
            "home_address": "123 Main St",
        },
    )
    assert response.status_code == fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY
