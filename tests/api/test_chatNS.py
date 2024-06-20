from ..fixtures import app, client, auth_headers
from unittest.mock import patch
import os


def test_new_chat(client, auth_headers):
    # Prepare
    num_chats_before = len(client.get(
        "/chat/preview", headers=auth_headers).json["chat_preview"])
    agent_setting = "Test Agent"
    new_chat = {"agent_setting": agent_setting}

    # Act
    response = client.post("/chat", json=new_chat, headers=auth_headers)

    # Verify
    assert response.status_code == 201
    assert response.json["agent_setting"] == agent_setting
    new_chats = client.get(
        "/chat/preview", headers=auth_headers).json["chat_preview"]
    assert len(new_chats) == num_chats_before + 1
    assert new_chats[-1]["agent_setting"] == agent_setting

    # No auth headers
    response = client.post("/chat", json=new_chat)
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}


def test_preview_chat(client, auth_headers):
    # Prepare
    target_output = {"chat_preview": [
        {"chat_id": "1", "agent_setting": "A german police officer is asking for your ID."},
        {"chat_id": "2", "agent_setting": "You are a cashier at Lidl. Going through a checkout."},
    ]}

    # Act
    response = client.get("/chat/preview", headers=auth_headers)
    parsed_response = response.json

    # Verify
    assert response.status_code == 200
    assert parsed_response == target_output

    # No auth headers
    response = client.post("/chat/preview")
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}


def test_get_chat(client, auth_headers):
    # Prepare
    chat_id = "1"
    target_output = {"messages": [
        {
            "sender": "user",
            "message": "Guten Tag!",
            "timestamp": "2020-12-01T12:00:00"
        },
        {
            "sender": "agent",
            "message": "Guten Tag, ich bin Polizist. Kann ich bitte Ihren Ausweis sehen?",
            "timestamp": "2020-12-01T12:00:00"
        },
        {
            "sender": "user",
            "message": "Ja, natürlich. Hier ist mein Ausweis.",
            "timestamp": "2020-12-01T12:00:05"
        },
        {
            "sender": "agent",
            "message": "Vielen Dank. Haben Sie einen schönen Tag.",
            "timestamp": "2020-12-01T12:00:10"
        }
    ]}

    # Act
    response = client.get(f"/chat/{chat_id}", headers=auth_headers)
    parsed_response = response.json

    # Verify
    assert response.status_code == 200
    assert parsed_response == target_output

    # Not found
    response = client.get(f"/chat/6", headers=auth_headers)
    assert response.status_code == 404

    # No authorization headers
    response = client.get(f"/chat/{chat_id}")
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}

@patch.dict(os.environ, {"OPENAI_API_KEY": "pytest"}) # Patching the api key, to not make calls to the real API
def test_send_message(client, auth_headers):
    # Prepare
    chat_id = "1"
    new_message = {"message": "Ich hätte gerne ein Schnitzel und eine Cola."}
    length_before = len(client.get(
        f"/chat/{chat_id}", headers=auth_headers).json["messages"])

    # Act
    response = client.post(
        f"/chat/{chat_id}", json=new_message, headers=auth_headers)
    parsed_response = response.json

    # Verify
    assert response.status_code == 201
    assert parsed_response["sender"] == "agent"
    assert parsed_response["message"] == "Example message made by the agent. Please set the OPENAI_API_KEY in the environment variables."
    # 2 new messages, since we also handle the agent's response
    assert length_before + \
        2 == len(client.get(f"/chat/{chat_id}",
                 headers=auth_headers).json["messages"])

    # Not found
    response = client.post(f"/chat/6", json=new_message, headers=auth_headers)
    assert response.status_code == 404

    # No authorization headers
    response = client.post(f"/chat/{chat_id}", json=new_message)
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}

@patch.dict(os.environ, {"OPENAI_API_KEY": "pytest"}) # Patching the api key, to not make calls to the real API
def test_grammar(client, auth_headers):
    # Prepare
    expected_output = {"explanation": "Example explanation made by the agent. Please set the OPENAI_API_KEY in the environment variables."}
    example_message = "Ich hätte gerne ein Schnitzel und eine Cola."

    # Act
    response = client.post(f"/chat/grammar", headers=auth_headers, json={"message": example_message})
    parsed_response = response.json
    
    # Verify
    assert response.status_code == 200
    assert parsed_response == expected_output

    # No authorization headers
    response = client.post(f"/chat/grammar", json={"message": example_message})
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}
    
@patch.dict(os.environ, {"DEEPL_API_KEY": "pytest"}) # Patching the api key, to not make calls to the real API
def test_translation(client, auth_headers):
    # Prepare
    expected_output = {"translation": "Example translation made by the agent. Please set the DEEPL_API_KEY in the environment variables."}
    example_message = "Ich hätte gerne ein Schnitzel und eine Cola."

    # Act
    response = client.post(f"/chat/translate", headers=auth_headers, json={"message": example_message})
    parsed_response = response.json
    
    # Verify
    assert response.status_code == 200
    assert parsed_response == expected_output

    # No authorization headers
    response = client.post(f"/chat/translate", json={"message": example_message})
    assert response.status_code == 401
    assert response.json == {"message": "Missing Authorization Header"}
