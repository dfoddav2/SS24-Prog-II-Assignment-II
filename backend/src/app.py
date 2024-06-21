from flask import Flask, jsonify
from flask import request
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError

from flask_cors import CORS
from flask_socketio import emit, join_room, leave_room
from src.extensions import mongo, socketio
from dotenv import load_dotenv
import json
import os
import bcrypt

# Namespace imports
from .api.userNS import user_ns
from .api.playNS import play_ns
from .api.wordbankNS import wordbank_ns
from .api.chatNS import chat_ns

# Importing the socket logic
import src.socket.wortle


# Setting up the create_app function for the Application Factory pattern
def create_app():
    app = Flask(__name__)

    # Setting up SocketIO
    socketio.init_app(app, cors_allowed_origins="*")

    # Setting up MongoDB based on the environmental variables
    load_dotenv()
    flask_env = os.getenv("FLASK_ENV", "development")
    print(f"FLASK_ENV: {flask_env}")
    
    # Setting up MongoDB based on the environmental variables
    mongo_env = os.getenv("MONGO_URI", "mongodb://localhost:27017/languageDB")
    app.config["MONGO_URI"] = mongo_env
    mongo.init_app(app)

    # Resetting MongoDB with mock data if we are on dev environment
    if flask_env == 'development':
        mongo.db.users.delete_many({})  # Delete all documents

        with open("data/mock_db_copy.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for email, user_data in data.items():
            user_data['_id'] = email  # Use the email as the document ID
            # Hash the password before storing
            user_data['password'] = bcrypt.hashpw(
                user_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            mongo.db.users.insert_one(user_data)

    # Enable CORS for development
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Setup JWT for authentication
    app.config["JWT_SECRET_KEY"] = "my_secret_key"
    jwt = JWTManager(app)

    # ----------------------
    # ----- API Routes -----
    # ----------------------

    # Setting up api routes
    api = Api(
        app, title="Language Learning API", version="1.0", description="An API for language learning app of Assignment 2, Prog II, SS2024", security='Bearer',
        # Setting up Bearer authorization
        authorizations={
            'Bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
        })
    
    # Decorator for handling missing Authorization Header - JWT Exception
    @api.errorhandler(NoAuthorizationError)
    def handle_auth_error(e):
        return {"message": "Missing Authorization Header"}, 401

    # add individual namespaces
    api.add_namespace(user_ns)
    api.add_namespace(play_ns)
    api.add_namespace(wordbank_ns)
    api.add_namespace(chat_ns)

    # Return the application factory
    return app
