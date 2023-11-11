def test_me(client, mock_uow, mock_auth, mock_database):
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == mock_auth.model_dump()


def test_registration(client, mock_uow, mock_database_for_registration):
    user_data = {"username": "testuser", "hashed_password": "testpassword"}
    response = client.post("/users/registration", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["access_token"] is not None


def test_token(client, mock_uow, mock_database_for_token):
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/users/token", data=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["access_token"] is not None
