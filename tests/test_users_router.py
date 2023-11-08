import pytest

from tests.conftest import TEST_USER, MockDatabase, MockDBForRegistration, MockDBForToken


@pytest.mark.parametrize(
    "mock_database",
    [MockDatabase]
)
def test_me(client, mock_uow):
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == TEST_USER.model_dump()


@pytest.mark.parametrize(
    "mock_database",
    [MockDBForRegistration]
)
def test_registration(client, mock_uow):
    user_data = {"username": "testuser", "hashed_password": "testpassword"}
    response = client.post("/users/registration", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["access_token"] is not None


@pytest.mark.parametrize(
    "mock_database",
    [MockDBForToken]
)
def test_token(client, mock_uow):
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/users/token", data=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["access_token"] is not None
