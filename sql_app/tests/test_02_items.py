from datetime import datetime

import pytest


def test_create_item(client, login_admin):
    # Подготовка данных для теста
    item_create = {
        "title": "Test Item",
        "description": "Test Description",
        "created_at": datetime.now().isoformat()  # Преобразуем дату в строку
    }
    # Вызов тестового эндпойнта
    response = client.post("/users/items/", json=item_create, headers={"Authorization": f"Bearer {login_admin}"})
    # Проверка результата
    assert response.status_code == 200
    item = response.json()
    assert item["title"] == item_create["title"]
    assert item["description"] == item_create["description"]


def test_create_item2(client, login_admin):
    # Подготовка данных для теста
    item_create = {
        "title": "Test Item2",
        "description": "Test Description2",
        "created_at": datetime.now().isoformat()  # Преобразуем дату в строку
    }
    # Вызов тестового эндпойнта
    response = client.post("/users/items/", json=item_create, headers={"Authorization": f"Bearer {login_admin}"})
    # Проверка результата
    assert response.status_code == 200
    item = response.json()
    assert item["title"] == item_create["title"]
    assert item["description"] == item_create["description"]


def test_get_items(client):
    # Вызов тестового эндпойнта
    response = client.get("/items/")
    # Проверка результата
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    assert items[0]["title"] == "Test Item"
    assert items[1]["title"] == "Test Item2"


def test_get_item(client):
    # Вызов тестового эндпойнта
    response = client.get("/items/1")
    # Проверка результата
    assert response.status_code == 200
    item_response = response.json()
    assert item_response["title"] == "Test Item"
    assert item_response["description"] == "Test Description"


def test_update_item(client, login_admin):
    # Подготовка данных для теста
    item_update = {
        "title": "Updated Item",
        "description": "Updated Description",
        "created_at": datetime.now().isoformat(),  # Преобразуем дату в строку
        "completed": True
    }
    # Вызов тестового эндпойнта
    response = client.put("/items/1", json=item_update, headers={"Authorization": f"Bearer {login_admin}"})
    # Проверка результата
    assert response.status_code == 200
    updated_item = response.json()
    assert updated_item["title"] == item_update["title"]
    assert updated_item["description"] == item_update["description"]


def test_delete_item(client, login_admin):
    # Вызов тестового эндпойнта
    response = client.delete("/items/2", headers={"Authorization": f"Bearer {login_admin}"})
    # Проверка результата
    assert response.status_code == 200
    deleted_item = response.json()
    assert deleted_item["title"] == "Test Item2"
    assert deleted_item["description"] == "Test Description2"


if __name__ == "__main__":
    pytest.main()
