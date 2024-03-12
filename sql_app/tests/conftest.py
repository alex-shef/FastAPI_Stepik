import pytest
from fastapi.testclient import TestClient

from sql_app import main, database


@pytest.fixture(scope="session")
def client():
    with TestClient(main.app) as c:
        yield c


# Создание тестовой сессии базы данных
@pytest.fixture(scope="session")
def db():
    db = database.SessionLocal()
    yield db
    db.close()


# Фикстура для очистки таблиц базы данных
@pytest.fixture()
def clean_db(db):
    for table in reversed(database.Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()


# Фикстура аутентификации
@pytest.fixture(scope="session")
def login_admin(client):
    response = client.post("/login", data={"username": "admin", "email": "admin@example.com", "password": "admin",
                                           "role": "admin"})
    token = response.json()["access_token"]
    return token
