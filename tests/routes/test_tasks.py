import fastapi

from tests.consts import TEST_CLIENT


def test_create_task():
    name="task_name"
    description="task_description"
    due_date="2001-12-20T01:02:00"

    response = TEST_CLIENT.post(
        "/tasks",
        headers={"Content-Type": "application/json", "RISKRECON-USER-ID": "999"},
        json={"name": name, "description": description, "due_date": due_date},
    )

    assert response.status_code == fastapi.status.HTTP_201_CREATED
    data = response.json()
    assert data == {
        "deleted": False,
        "description": description,
        "due_date": due_date,
        "id": 1,
        "name": name,
    }


def test_create_task_invalid_data():
    response = TEST_CLIENT.post(
        "/tasks",
        json={
            "name": "task_name",
        },
    )
    assert response.status_code == fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY
