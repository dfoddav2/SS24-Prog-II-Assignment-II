from ..fixtures import app, client, auth_headers

def test_get_user_data(client, auth_headers):
    # Prepare
    expected_data = {"email": "asd@asd", "name": "David Fodor"}
    
    # Act
    response = client.get("/user", headers=auth_headers)
    parsed_response = response.json
    
    # Verify
    assert response.status_code == 200
    assert parsed_response == expected_data
    
    # No auth headers
    response = client.get("/user")
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}

    
def test_edit_user(client, auth_headers):
    # Prepare
    new_name = "New Name"
    data = {"name": new_name}
    
    # Assert that the user's email is not the new email
    assert client.get("/user", headers=auth_headers).json["name"] != new_name
    
    # Act
    response = client.put("/user", json=data, headers=auth_headers)
    parsed_response = response.json
    
    # Verify
    assert response.status_code == 200
    assert parsed_response["name"] == new_name
    
    # No auth headers
    response = client.get("/user")
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}
    
def test_delete_user(client, auth_headers):
    # Prepare
    # Assert that the user exists
    assert client.get("/user", headers=auth_headers).status_code == 200
    
    # Act
    response = client.delete("/user", headers=auth_headers)
    
    # Verify
    assert response.status_code == 204
    
    # Assert that the user does not exist anymore
    assert client.get("/user", headers=auth_headers).status_code == 404
    
    # No auth headers
    response = client.get("/user")
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}
    
def test_login(client):
    # Prepare
    auth = {"email": "asd@asd", "password": "123"}
    
    # Act
    response = client.post("/user/login", json=auth)
    parsed_response = response.json
    
    # Verify
    assert response.status_code == 200
    assert "access_token" in parsed_response
    assert parsed_response["email"] == auth["email"]
    assert parsed_response["name"] == "David Fodor"
    
    # Invalid credentials
    auth["password"] = "WRONG_PASSWORD"
    response = client.post("/user/login", json=auth)
    assert response.status_code == 401
    assert response.json == {"message": "Invalid credentials"}
    
def test_register(client):
    # Prepare
    test_mail = "test@test"
    test_password = "test"
    test_name = "Test User"
    data = {"email": test_mail, "password": test_password, "name": test_name}
    
    # Act
    response = client.post("/user/register", json=data)
    parsed_response = response.json
    
    # Verify
    assert response.status_code == 201
    assert "access_token" in parsed_response
    assert parsed_response["email"] == test_mail
    assert parsed_response["name"] == test_name
    
    # User with email already exists
    test_mail = "asd@asd"
    response = client.post("/user/register", json=data)
    assert response.status_code == 409
    assert response.json == {"message": "User with email already exists"}
    