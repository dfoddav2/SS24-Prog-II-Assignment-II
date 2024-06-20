from ..fixtures import app, client, auth_headers

def test_get_wordbank_of_user(client, auth_headers):
    # Prepare
    expected_data = {"wordbank": ["hallo", "bananen", "fahrrad", "jeman", "autos", "danke"]}
    
    # Act
    response = client.get("/wordbank/user", headers=auth_headers)
    parsed_response = response.json
    
    # Verify
    assert response.status_code == 200
    assert parsed_response == expected_data

    # No auth headers
    response = client.get("/wordbank/user")
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}
    
    
def test_add_word_to_wordbank(client, auth_headers):
    # Prepare
    new_word = {"wordbank_word": "samstag"}
    wordbank_before = {"wordbank": ["hallo", "bananen", "fahrrad", "jeman", "autos", "danke"]}
    assert client.get("/wordbank/user", headers=auth_headers).json == wordbank_before
    expected_wordbank_after = {"wordbank": ["hallo", "bananen", "fahrrad", "jeman", "autos", "danke", "samstag"]}
    
    # Act
    response = client.post("/wordbank/user", headers=auth_headers, json=new_word)
    parsed_response = response.json
    
    # Verify
    assert response.status_code == 201
    assert parsed_response == expected_wordbank_after
    
    # Word already exists in the wordbank
    new_word = {"wordbank_word": "samstag"} # We know this one is in there, since we added just before
    response = client.post("/wordbank/user", headers=auth_headers, json=new_word)
    assert response.status_code == 409
    assert response.json == {"message": "Word already in Wordbank"}

    # No auth headers
    response = client.post("/wordbank/user", json=new_word)
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}

def test_delete_word_from_wordbank(client, auth_headers):
    # Prepare
    word_to_delete = "danke"
    wordbank_before = client.get("/wordbank/user", headers=auth_headers).json["wordbank"]
    assert word_to_delete in wordbank_before
    
    # Act
    response = client.delete("/wordbank/user", headers=auth_headers, json={"wordbank_word": word_to_delete})
    parsed_response = response.json
    
    # Verify
    assert response.status_code == 200
    assert word_to_delete not in parsed_response["wordbank"]
    
    # The word is not in the wordbank to begein with
    word_to_delete = "WORD_NOT_IN_WORDBANK"
    response = client.delete("/wordbank/user", headers=auth_headers, json={"wordbank_word": word_to_delete})
    assert response.status_code == 404
    assert response.json == {"message": "Word not in Wordbank"}
    
    # No auth headers
    response = client.delete("/wordbank/user", json=word_to_delete)
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}
