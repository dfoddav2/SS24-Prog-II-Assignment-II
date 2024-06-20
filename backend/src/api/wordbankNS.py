from flask import Response, jsonify
from flask_restx import Namespace, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..app import mongo

# Namespace regarding wordbank related operations
wordbank_ns = Namespace(
    "wordbank", description="Wordbank related operations")


# ---------------------
# ====== MODELS =======
# ---------------------

wordbank_model = wordbank_ns.model("Wordbank", {
    "wordbank": fields.List(fields.String, required=True, help="The wordbank of the user"),
})

wordbank_word_model = wordbank_ns.model("WordbankWord", {
    "wordbank_word": fields.String(required=True, help="The word the user wants to add")
})

unauthorized_model = wordbank_ns.model("UserUnauthorized", {
    'msg': fields.String(example='Missing Authorization Header')
})


# ---------------------
# ====== ROUTES =======
# ---------------------

@wordbank_ns.route("/user")
class WordbankUserAPI(Resource):

    @wordbank_ns.doc(description="Get the wordbank of a specific user", responses={200: ("Success", wordbank_model), 401: ("Unauthorized", unauthorized_model)})
    @jwt_required()
    def get(self):
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Retieve the user's wordbank
        user_data = mongo.db.users.find_one(
            {"_id": current_user}, {"wordbank": 1})
        # print(user_data)
        if user_data:
            return marshal({"wordbank": user_data["wordbank"]}, wordbank_model)
        return {"message": "User not found"}, 404

    @wordbank_ns.doc(description="Add a word to the logged in user's wordbank", responses={201: ("Success", wordbank_model), 401: ("Unauthorized", unauthorized_model), 409: "Word already in wordbank"})
    @wordbank_ns.expect(wordbank_word_model)
    @jwt_required()
    def post(self):
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Check whether the user exists, if it does, get the wordbank
        user_data = mongo.db.users.find_one(
            {"_id": current_user}, {"wordbank": 1})
        
        # If user is not found
        if not user_data:
            return {"message": "User not found"}, 404
        
        # If word already in wordbank
        word_to_add = wordbank_ns.payload["wordbank_word"]
        if word_to_add in user_data["wordbank"]:
            return {"message": "Word already in Wordbank"}, 409

        # If everything is fine, add the new word
        new_wordbank = mongo.db.users.find_one_and_update(
            {"_id": current_user},
            { "$push": { "wordbank": word_to_add }},
            return_document=True
        )
        return marshal({"wordbank": new_wordbank["wordbank"]}, wordbank_model), 201
        
    @wordbank_ns.doc(description="Delete a word from the logged in user's wordbank", responses={200: ("Success", wordbank_model), 401: ("Unauthorized", unauthorized_model), 404: "Word is not in wordbank"})
    @wordbank_ns.expect(wordbank_word_model)
    @jwt_required()
    def delete(self):
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Check whether the user exists
        user_data = mongo.db.users.find_one(
            {"_id": current_user}, {"wordbank": 1})
        
        # Check whether the user exists
        if not user_data:
            return {"message": "User not found"}, 404
            
        # Check whether the word exists in the wordbank
        word_to_delete = wordbank_ns.payload["wordbank_word"]
        if word_to_delete not in user_data["wordbank"]:
            return {"message": "Word not in Wordbank"}, 404
        
        # If everything is fine, we can delete the word and return the new wordbank
        new_wordbank = mongo.db.users.find_one_and_update(
            {"_id": current_user},
            { "$pull": { "wordbank": word_to_delete }},
            return_document=True
        )
        return marshal({"wordbank": new_wordbank["wordbank"]}, wordbank_model), 200
