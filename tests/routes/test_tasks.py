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


def test_get_tasks_for_authenticated_user():
    first_task = TEST_CLIENT.post(
        "/tasks",
        headers={"Content-Type": "application/json", "RISKRECON-USER-ID": "999"},
        json={"name": "task_name_1", "description": "task_description_1", "due_date": "2001-12-20T01:02:00"},
    )
    assert first_task.status_code == fastapi.status.HTTP_201_CREATED

    second_task = TEST_CLIENT.post(
        "/tasks",
        headers={"Content-Type": "application/json", "RISKRECON-USER-ID": "123"},
        json={"name": "task_name_2", "description": "task_description_2", "due_date": "2001-12-21T01:02:00"},
    )
    assert second_task.status_code == fastapi.status.HTTP_201_CREATED

    response = TEST_CLIENT.get(
        "/tasks",
        headers={"RISKRECON-USER-ID": "999"},
    )

    assert response.status_code == fastapi.status.HTTP_200_OK
    assert response.json() == [
        {
            "deleted": False,
            "description": "task_description_1",
            "due_date": "2001-12-20T01:02:00",
            "id": 1,
            "name": "task_name_1",
        }
    ]


def test_get_tasks_rejects_cross_user_access():
    response = TEST_CLIENT.get(
        "/tasks/123",
        headers={"RISKRECON-USER-ID": "999"},
    )

    assert response.status_code == fastapi.status.HTTP_403_FORBIDDEN
