import pytest


def test_create_first_admin(clean_db, client):
    # Проверяем создание первого администратора
    response = client.post("/create_first_admin",
                           json={"username": "admin", "email": "admin@example.com", "password": "admin",
                                 "role": "admin"})
    assert response.status_code == 200
    assert response.json()["username"] == "admin"


def test_create_first_admin_conflict(client):
    # Проверяем конфликт при попытке создать первого администратора, когда он уже существует
    response = client.post("/create_first_admin",
                           json={"username": "admin", "email": "admin@example.com", "password": "admin",
                                 "role": "admin"})
    assert response.status_code == 409
    assert response.json()["detail"] == "Admin already exists"


def test_create_user(client, login_admin):
    # Проверяем создание пользователя администратором
    response = client.post("/users/", json={"username": "new_user", "email": "new_user@example.com",
                                            "password": "password", "role": "user"},
                           headers={"Authorization": f"Bearer {login_admin}"})
    assert response.status_code == 200
    assert response.json()["username"] == "new_user"


def test_create_user_unauthorized(client):
    # Проверяем отказ в доступе при попытке создать пользователя без аутентификации администратора
    response = client.post("/users/", json={"username": "new_user", "email": "new_user@example.com",
                                            "password": "password", "role": "user"})
    assert response.status_code == 401


def test_create_user_email_conflict(client, login_admin):
    # Проверяем конфликт при попытке создать пользователя с уже существующим email
    response = client.post("/users/", json={"username": "new_user2", "email": "new_user@example.com",
                                            "password": "password"},
                           headers={"Authorization": f"Bearer {login_admin}"})
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


def test_create_user_username_conflict(client, login_admin):
    # Проверяем конфликт при попытке создать пользователя с уже существующим username
    response = client.post("/users/", json={"username": "new_user", "email": "new_user2@example.com",
                                            "password": "password"},
                           headers={"Authorization": f"Bearer {login_admin}"})
    assert response.status_code == 409
    assert response.json()["detail"] == "Username already registered"


def test_get_users(client, login_admin):
    # Проверяем получение списка пользователей администратором
    response = client.get("/users/", headers={"Authorization": f"Bearer {login_admin}"})
    assert response.status_code == 200
    assert len(response.json()) == 2  # Проверяем количество пользователей


def test_get_users_unauthorized(client):
    # Проверяем отказ в доступе при попытке получить список пользователей без аутентификации администратора
    response = client.get("/users/")
    assert response.status_code == 401


def test_get_user(client, login_admin):
    # Проверяем получение пользователя по ID администратором
    response = client.get("/users/2", headers={"Authorization": f"Bearer {login_admin}"})
    assert response.status_code == 200
    assert response.json()["username"] == "new_user"


def test_get_user_not_found(client, login_admin):
    # Проверяем получение несуществующего пользователя администратором
    response = client.get("/users/999", headers={"Authorization": f"Bearer {login_admin}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


if __name__ == "__main__":
    pytest.main()
