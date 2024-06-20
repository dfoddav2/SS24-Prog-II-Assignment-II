from flask import Response, jsonify
from flask_restx import Namespace, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ..app import mongo
from pymongo import ReturnDocument
from dotenv import load_dotenv
from openai import OpenAI
import deepl
import os
import uuid
import time

# Namespace regarding chat related operations
chat_ns = Namespace(
    "chat", description="Chat related operations")

# ====== MODELS =======

# Model for previewing chats of a user - left side of the chat interface
chat_preview_model = chat_ns.model("ChatPreviewInstance", {
    "chat_id": fields.String(required=True, help="The id of the chat instance"),
    "agent_setting": fields.String(required=True, help="The agent of the chat instance"),
})

# List wrapper model of the chat preview model
chat_previews_model = chat_ns.model("ChatPreview", {
    "chat_preview": fields.List(fields.Nested(chat_preview_model), required=True, help="The chat previews of the user"),
})

# Model for a message in the chat
message_model = chat_ns.model("Message", {
    "sender": fields.String(required=True, help="The sender of the message, either agent or user"),
    "message": fields.String(required=True, help="The message of the sender"),
    "timestamp": fields.DateTime(required=True, help="The timestamp of the message"),
})

# List wrapper model for the message model
chat_instance_model = chat_ns.model("ChatInstance", {
    "messages": fields.List(fields.Nested(message_model), required=True, help="The messages of the user"),
})

# Model for initiating a new chat instance - setting the agent
chat_new_chat_input_model = chat_ns.model("NewChatInput", {
    "agent_setting": fields.String(required=True, help="The agent setting of the chat instance"),
})

# Model for the response of creating a new chat instance
chat_new_chat_model = chat_ns.model("NewChat", {
    "chat_id": fields.String(required=True, help="The id of the chat instance"),
    "agent_setting": fields.String(required=True, help="The agent setting of the chat instance"),
})

# Model for the input of a chat message by the user
chat_message_input_model = chat_ns.model("ChatMessageInput", {
    "message": fields.String(required=True, help="The message received from the user"),
})

# Model for getting the grammatical explanation of a sentence
grammatical_explanation_model = chat_ns.model("GrammaticalExplanation", {
    "explanation": fields.String(required=True, help="The grammatical explanation of the sentence"),
})

# Model for translating a german sentence to english
translate_de_to_en_model = chat_ns.model("TranslationDEToENModel", {
    "translation": fields.String(required=True, help="The translation of the German sentence to English"),
})

# Model for returning unauthorized error - 401
unauthorized_model = chat_ns.model("UserUnauthorized", {
    'msg': fields.String(example='Missing Authorization Header')
})


# ---------------------
# ====== ROUTES =======
# ---------------------

@chat_ns.route("")
class ChatAPI(Resource):

    # Create a new chat instance
    @chat_ns.doc(description="Create a new chat using the input setting", security='Bearer', responses={201: ("Success", chat_new_chat_model), 401: ("Unauthorized", unauthorized_model)})
    @chat_ns.expect(chat_new_chat_input_model)
    @jwt_required()
    def post(self):
        agent_setting = chat_ns.payload.get("agent_setting")
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Add to the user's chats, if successful return the chat_id and the agent_setting - else return 404
        chat_id = str(uuid.uuid4())
        updated = mongo.db.users.find_one_and_update({"_id": current_user}, {"$set": {f"chats.{chat_id}": {
                                                     "agent_setting": agent_setting, "history": []}}}, return_document=ReturnDocument.AFTER)
        if updated:
            return marshal({"chat_id": chat_id, "agent_setting": agent_setting}, chat_new_chat_model), 201
        return {"message": "User not found"}, 404


@chat_ns.route("/preview")
class ChatPreviewAPI(Resource):

    # Get the preview of all chat instances of a user - left side of the chat interface
    @chat_ns.doc(description="Get the preview of all chat instances of a user", security='Bearer', responses={200: ("Success", chat_previews_model), 401: ("Unauthorized", unauthorized_model)})
    @jwt_required()
    def get(self):
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Get the chat_ids and agent_settings of the chat instances, if successful return the chat previews - else return 404
        user_data = mongo.db.users.find_one(
            {"_id": current_user}, {"chats": 1})
        if user_data:
            # Iterate over the chats and get the chat_id and agent_setting
            # result = [{"chat_id": chat["chat_id"], "agent_setting": chat["agent_setting"]}
            #           for chat in user_data["chats"]]
            result = [{"chat_id": chat_id, "agent_setting": user_data["chats"][chat_id]["agent_setting"]}
                      for chat_id in user_data["chats"]]
            return {"chat_preview": marshal(result, chat_preview_model)}
        return {"message": "User not found"}, 404


@chat_ns.route("/<string:chat_id>")
class ChatChatIdAPI(Resource):

    # Get all the messages of a chat instance by the chat's id
    @chat_ns.doc(description="Get all the messages of a chat instance by the chat's id", security='Bearer', responses={200: ("Success", message_model), 401: ("Unauthorized", unauthorized_model), 404: "Chat not found"})
    @jwt_required()
    def get(self, chat_id):
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Get the chats of the user and return the messages of the chat instance where chat ID matches - else return 404
        user_data = mongo.db.users.find_one(
            {"_id": current_user}, {"chats": 1})
        if user_data:
            chat_data = user_data["chats"].get(chat_id)
            if chat_data:
                # Loop through each message of the history and return the sender, message and timestamp
                result = [{"sender": message["sender"], "message": message["message"],
                           "timestamp": message["timestamp"]} for message in chat_data["history"]]
                return {"messages": marshal(result, message_model)}
            return {"message": "Chat not found"}, 404
        return {"message": "User not found"}, 404

    # Handle when a user sends a message to the chat instance
    @chat_ns.doc(description="Send a message to the chat instance", security='Bearer', responses={201: ("Success", message_model), 401: ("Unauthorized", unauthorized_model), 404: "Chat not found"})
    @chat_ns.expect(chat_message_input_model)
    @jwt_required()
    def post(self, chat_id):
        # Get the message from the user
        message = chat_ns.payload.get("message")
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Get the user's chats, if the user doesn't exist or have such chat return 404
        user_data = mongo.db.users.find_one(
            {"_id": current_user}, {"chats": 1})
        if user_data:
            if chat_id in user_data["chats"]:
                # user_data["chats"][chat_id]["history"].append(
                #     {"sender": "user", "message": message, "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")})
                # Mock a call to the agent (mocked for now)
                # TODO: Actually make the call to OpenAI API
                load_dotenv()
                # Check whether the API key is present in the environment variables
                user_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                print("Calling agent...")
                
                # =======================
                # === OPENAI API CALL ===
                # =======================
                # Uncomment for prod - comment for dev (no need to make unnecessary API calls)
                if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "pytest":
                    # If it is not preset, the message should just be a placeholder
                    agent_message = "Example message made by the agent. Please set the OPENAI_API_KEY in the environment variables."
                    time.sleep(2)
                    agent_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                else:
                    client = OpenAI()
                    # Setup the message to send to the agent
                    # Agent setting as first message, then at most 4 of the latest messages from the conversation to reserve token usage
                    last_messages = []
                    for msg in user_data["chats"][chat_id]["history"][-4:]:
                        if msg["sender"] == "agent":
                            last_messages.append({"role": "system", "content": msg["message"]})
                        else:
                            last_messages.append({"role": "user", "content": msg["message"]})
                    # Also add the now just created user message
                    last_messages.append({"role": "user", "content": message})
                    messages_to_send = [
                        {"role": "system", "content": f"{user_data['chats'][chat_id]['agent_setting']} You may only speak German."},
                    ] + last_messages
                    # Send the messages to the agent
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages_to_send
                    )
                    # Get the response from the agent
                    agent_message = str(completion.choices[0].message.content)
                    agent_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                print("Agent replied:")
                print(agent_message)
                # Now that we also have the response we can update the DB
                # Append the user's message
                mongo.db.users.update_one({"_id": current_user}, {"$push": {f"chats.{chat_id}.history": {
                                          "sender": "user", "message": message, "timestamp": user_timestamp}}})
                # Append the agent's message
                mongo.db.users.update_one({"_id": current_user}, {"$push": {f"chats.{chat_id}.history": {
                                          "sender": "agent", "message": agent_message, "timestamp": agent_timestamp}}})
                # Once we have updated the DB, we can return the response to frontend
                return marshal({"sender": "agent", "message": agent_message, "timestamp": agent_timestamp}, message_model), 201
            return {"message": "Chat not found"}, 404
        return {"message": "User not found"}, 404


@chat_ns.route("/grammar")
class ChatGrammarAPI(Resource):
    
    @chat_ns.doc(description="Get a grammatical explanation of a sentence through OpenAI", security='Bearer', responses={200: ("Success", grammatical_explanation_model), 401: ("Unauthorized", unauthorized_model)})
    @chat_ns.expect(chat_message_input_model)
    @jwt_required()
    def post(self):
        # Get the message from the user
        message_to_explain = chat_ns.payload.get("message")
        # Make a call to OpenAI if the API key is present, else return a placeholder
        if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "pytest":
            agent_message = "Example explanation made by the agent. Please set the OPENAI_API_KEY in the environment variables."
            time.sleep(2)
        else:
            # Initialize the OpenAI client and set up messages to send
            messages_to_send = [
                {"role": "system", "content": "Please shortly explain the grammatical rules used in this German sentence. Don't just translate it. Be as concise as possible."},
                {"role": "user", "content": message_to_explain}
            ]
            client = OpenAI()
            # Send the message to the agent
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages_to_send
            )
            # Get the response from the agent
            agent_message = str(completion.choices[0].message.content)
        return marshal({"explanation": agent_message}, grammatical_explanation_model), 200


@chat_ns.route("/translate")
class ChatTranslationAPI(Resource):
    
    @chat_ns.doc(description="Get the translation of a German sentence from DeepL API", security='Bearer', responses={200: ("Success", translate_de_to_en_model), 401: ("Unauthorized", unauthorized_model)})
    @chat_ns.expect(chat_message_input_model)
    @jwt_required()
    def post(self):
        # Get the message from the user
        message_to_translate = chat_ns.payload.get("message")
        # Make a call to DeepL API if the API key is present, else return a placeholder
        if os.getenv("DEEPL_API_KEY") is None or os.getenv("DEEPL_API_KEY") == "pytest":
            agent_message = "Example translation made by the agent. Please set the DEEPL_API_KEY in the environment variables."
            time.sleep(2)
        else:
            # Initialize the DeepL client and set up the message to send
            translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))
            result = translator.translate_text(message_to_translate, source_lang="DE", target_lang="EN-GB")
            agent_message = result.text
        return marshal({"translation": agent_message}, translate_de_to_en_model), 200
