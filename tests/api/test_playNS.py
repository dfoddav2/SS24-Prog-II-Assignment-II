from ..fixtures import app, client, auth_headers


def test_wortle_leaderboard(client, auth_headers):
    # Prepare
    target_output = [
        {"email": "michael.smith@example.com",
            "singleplayer_score": 10, "no_singles": 12, "multiplayer_score": 5, "no_multi": 6},
        {"email": "emma.johnson@example.com",
            "singleplayer_score": 8, "no_singles": 9, "multiplayer_score": 4, "no_multi": 5},
        {"email": "jane.doe@example.com",
            "singleplayer_score": 7, "no_singles": 8, "multiplayer_score": 3, "no_multi": 4},
        {"email": "asd@asd", "singleplayer_score": 5,
            "no_singles": 5, "multiplayer_score": 2, "no_multi": 3},
        {"email": "abc@abc", "singleplayer_score": 3,
            "no_singles": 6, "multiplayer_score": 1, "no_multi": 3}
    ]

    # Act
    response = client.get("/play/wortle/leaderboard")
    parsed_response = response.json

    # Verify
    assert response.status_code == 200
    assert parsed_response == target_output


def test_user_scores(client, auth_headers):
    # Prepare
    target_output = {
        "email": "asd@asd",
        "singleplayer_score": 5,
        "no_singles": 5,
        "multiplayer_score": 2,
        "no_multi": 3
    }

    # Act
    response = client.get("/play/user", headers=auth_headers)
    parsed_response = response.json

    # Verify
    assert response.status_code == 200
    assert parsed_response == target_output

    # No auth headers
    response = client.get("/play/user")
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}

# TODO: Add a case where the user has no 5 letter word - different auth header needed for this


def test_get_wortle_word(client, auth_headers):
    # Prepare
    target_wordbank = ["hallo", "bananen",
                       "fahrrad", "jeman", "autos", "danke"]

    # Act
    response = client.get("/play/wortle/singleplayer", headers=auth_headers)
    parsed_response = response.json

    # Verify
    assert response.status_code == 200
    assert parsed_response["word"] in target_wordbank

    # No auth headers
    response = client.post("/play/wortle/singleplayer")
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}

# TODO: Update this to also check no_sinlges, not just wins


def test_wortle_singleplayer_outcome(client, auth_headers):
    # 1. Check WIN
    # Prepare
    single_wins_before = client.get(
        "/play/user", headers=auth_headers).json["singleplayer_score"]
    outcome = {"outcome": True}

    # Act
    response = client.post("/play/wortle/singleplayer",
                           json=outcome, headers=auth_headers)

    # Verify
    assert response.status_code == 200
    assert response.json["singleplayer_score"] == single_wins_before + 1
    assert client.get(
        "/play/user", headers=auth_headers).json["singleplayer_score"] == single_wins_before + 1

    # 2. Check LOST
    # Prepare
    single_wins_before = client.get(
        "/play/user", headers=auth_headers).json["singleplayer_score"]
    outcome = {"outcome": False}

    # Act
    response = client.post("/play/wortle/singleplayer",
                           json=outcome, headers=auth_headers)

    # Verify
    assert response.status_code == 200
    assert response.json["singleplayer_score"] == single_wins_before
    assert client.get(
        "/play/user", headers=auth_headers).json["singleplayer_score"] == single_wins_before

    # No auth headers
    response = client.post("/play/wortle/singleplayer", json=outcome)
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}


def test_wortle_multiplayer_outcome(client, auth_headers):
    # 1. Check WIN
    # Prepare
    multi_wins_before = client.get(
        "/play/user", headers=auth_headers).json["multiplayer_score"]
    outcome = {"outcome": True}

    # Act
    response = client.post("/play/wortle/multiplayer",
                           json=outcome, headers=auth_headers)

    # Verify
    assert response.status_code == 200
    assert response.json["multiplayer_score"] == multi_wins_before + 1
    assert client.get(
        "/play/user", headers=auth_headers).json["multiplayer_score"] == multi_wins_before + 1

    # 2. Check LOST
    # Prepare
    multi_wins_before = client.get(
        "/play/user", headers=auth_headers).json["multiplayer_score"]
    outcome = {"outcome": False}

    # Act
    response = client.post("/play/wortle/multiplayer",
                           json=outcome, headers=auth_headers)

    # Verify
    assert response.status_code == 200
    assert response.json["multiplayer_score"] == multi_wins_before
    assert client.get(
        "/play/user", headers=auth_headers).json["multiplayer_score"] == multi_wins_before

    # No auth headers
    response = client.post("/play/wortle/multiplayer", json=outcome)
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}
