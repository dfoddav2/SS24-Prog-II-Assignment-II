from flask_socketio import SocketIO
from flask_pymongo import PyMongo

# Setting up the extensions for Socket.IO and MongoDB
socketio = SocketIO()
mongo = PyMongo()