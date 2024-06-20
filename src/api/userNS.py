from flask_restx import Namespace, Resource, fields, marshal
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..app import mongo
import bcrypt

# Namespace regarding user related operations
user_ns = Namespace("user", description="User related operations")


# ---------------------
# ====== MODELS =======
# ---------------------

# Model for getting a logged in users data
user_data_model = user_ns.model("UserDataModel", {
    "email": fields.String(required=True, help="The email of the user"),
    "name": fields.String(required=True, help="The name of the user"),
})

# Models for editing a user's data (just email for now)
user_edit_model = user_ns.model("UserEditModel", {
    "name": fields.String(required=True, help="The new name of the user"),
})

# Model for authentication, login TODO: The password should not be returned in a real application
user_model = user_ns.model("AuthenticatedUserModel", {
    "access_token": fields.String(required=True, help="The authentication token of the user"),
    "email": fields.String(required=True, help="The email of the user"),
    "password": fields.String(required=True, help="The password of the user"),
    "name": fields.String(required=True, help="The name of the user"),
})

# Model for getting the login input from the user
login_model = user_ns.model("UserLoginModel", {
    "email": fields.String(required=True, help="The email of the user"),
    "password": fields.String(required=True, help="The password of the user"),
})

# Model for getting the register input from the user
register_model = user_ns.model("UserRegisterModel", {
    "email": fields.String(required=True, help="The email of the user"),
    "password": fields.String(required=True, help="The password of the user"),
    "name": fields.String(required=True, help="The name of the user"),
})

# Model for returning invalid credentials error - 401
invalid_credentials_model = user_ns.model("UserInvalidCredentialsModel", {
    'msg': fields.String(example='Invalid credentials')
})

# Model for returning email exists error - 409
email_exists_model = user_ns.model("UserEmailExistsModel", {
    'msg': fields.String(example='User with email already exists')
})

# Model for returning unauthorized error - 401
unauthorized_model = user_ns.model("UserUnauthorizedModel", {
    'msg': fields.String(example='Missing Authorization Header')
})


# ---------------------
# ====== ROUTES =======
# ---------------------

@user_ns.route("")
class UserAPI(Resource):

    @user_ns.doc(description="Get a logged in user's data", responses={200: ("Success", user_data_model), 401: ("Unauthorized", unauthorized_model)})
    @jwt_required()
    def get(self):
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Check if user exists
        user = mongo.db.users.find_one({"_id": current_user})
        if not user:
            return "User could not be found", 404
        # Get the user data (name) from the db
        user_name = mongo.db.users.find_one(
            {"_id": current_user}, {"name": 1})["name"]
        # Return the user data
        if not user_name:
            return "User could not be found", 404
        return marshal({"email": current_user, "name": user_name}, user_data_model), 200

    @user_ns.doc(description="Edit a user's data (just name for now)", responses={200: ("Success", user_edit_model), 401: ("Unauthorized", unauthorized_model)})
    @jwt_required()
    @user_ns.expect(user_edit_model)
    def put(self):
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Get the new name
        new_name = user_ns.payload["name"]
        # Check if user exists
        user = mongo.db.users.find_one({"_id": current_user})
        if not user:
            return "User could not be found", 404
        # Else we can update the email of the user in the db
        mongo.db.users.update_one({"_id": current_user}, {
                                  "$set": {"name": new_name}})
        # Return the user data
        return marshal({"name": new_name}, user_edit_model), 200

    @user_ns.doc(description="Delete a user", responses={204: ("Success", None), 401: ("Unauthorized", unauthorized_model)})
    @jwt_required()
    def delete(self):
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Check if user exists
        user = mongo.db.users.find_one({"_id": current_user})
        if not user:
            return "User could not be found", 404
        # Delete the user from the db
        mongo.db.users.delete_one({"_id": current_user})
        return None, 204


# TODO:
# - Passwords should not be returned in a real application
# - The password should be hashed and salted
@user_ns.route("/login")
class UserLoginAPI(Resource):

    @user_ns.doc(description="Login user", responses={200: ("Success", user_model), 401: ("Invalid credentials", invalid_credentials_model)})
    @user_ns.expect(login_model)
    def post(self):
        # We read the email and password from the request
        email = user_ns.payload["email"]
        password = user_ns.payload["password"]
        # Find the user in the db, if it exists, return the user data and the access token to the user
        # - Else return 401 invalid credentials
        user = mongo.db.users.find_one({"_id": email})
        if user:
            # Convert the hashed password to bytes
            hashed_password = user["password"].encode('utf-8')
            # Check if the hashed password matches the provided password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                access_token = create_access_token(identity=email)
                result = {
                    "access_token": access_token,
                    "password": password,
                    "email": email,
                    "name": user["name"]
                }
                return marshal(result, user_model)
        return {"message": "Invalid credentials"}, 401


@user_ns.route("/register")
class UserRegisterAPI(Resource):

    @user_ns.doc(description="Register user", responses={201: ("Success", user_model), 409: ("User with email already exists", email_exists_model)})
    @user_ns.expect(register_model)
    def post(self):
        # We read the email, password and name from the request
        email = user_ns.payload["email"]
        password = user_ns.payload["password"]
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        name = user_ns.payload["name"]
        # Checks if the email exists in the db (if it does, 409 email exists)
        user = mongo.db.users.find_one({"_id": email})
        if user:
            return {"message": "User with email already exists"}, 409
        # If it doesn't exist, we insert the user into the db with the data from the request
        mongo.db.users.insert_one({"_id": email, "password": hashed_password.decode('utf-8'), "name": name, "games": {
                                  "wortle": {
                                      "singleplayer": 0,
                                      "no_singles": 0,
                                      "multiplayer": 0,
                                      "no_multi": 0
                                  }}, "wordbank": [], "chats": {}})
        access_token = create_access_token(identity=email)
        # Return the user data and the access token
        result = {
            "access_token": access_token,
            "email": email,
            # TODO: Of course, returning the password makes no sense in a real application
            "password": password,
            "name": name
        }
        return marshal(result, user_model), 201
