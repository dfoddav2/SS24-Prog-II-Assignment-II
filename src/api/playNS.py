from flask_restx import Namespace, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..app import mongo
from pymongo import ReturnDocument
import random

# Namespace regarding play functionality related operations
play_ns = Namespace(
    "play", description="Play functionality related operations")


# ---------------------
# ====== MODELS =======
# ---------------------

# Model for getting the scores of a user TODO: Is used for leaderboard - maybe create a nested one too for better structure
play_scores_model = play_ns.model("PlayScoresModel", {
    "email": fields.String(required=True, help="The email of the user"),
    "singleplayer_score": fields.Integer(required=True, help="The singlepayer score of the user"),
    "no_singles": fields.Integer(required=True, help="The number of singleplayer games the user has played"),
    "multiplayer_score": fields.Integer(required=True, help="The multiplayer score of the user"),
    "no_multi": fields.Integer(required=True, help="The number of multiplayer games the user has played"),
})

# Model for getting the singleplayer Wortle stats of a user
play_singleplayer_stats_model = play_ns.model("PlaySingleplayerStatsModel", {
    "email": fields.String(required=True, help="The email of the user"),
    "no_singles": fields.Integer(required=True, help="The number of singleplayer games the user has played"),
    "singleplayer_score": fields.Integer(required=True, help="The singlepayer score of the user"),
})

# Model for getting the word of a singleplayer Wortle game
wortle_singleplayer_model = play_ns.model("PlayWortleSingleplayerModel", {
    "word": fields.String(required=True, help="The word the user hass to guess"),
})

# Model for getting the input of the outcome of a singleplayer Wortle game
wortle_singleplayer_outcome_input_model = play_ns.model("PlayWortleSingleplayerInputModel", {
    "outcome": fields.Boolean(required=True, help="The outcome of the game"),
})

# Model for getting the input of the outcome of a multipalyer Wortle game
wortle_multiplayer_outcome_input_model = play_ns.model("PlayWortleMultiplayerInputModel", {
    "outcome": fields.Boolean(required=True, help="The outcome of the game"),
})

# Model for getting the multiplayer Wortle stats of a user
play_multiplayer_stats_model = play_ns.model("PlayMultiplayerStatsModel", {
    "email": fields.String(required=True, help="The email of the user"),
    "no_multi": fields.Integer(required=True, help="The number of multiplayer games the user has played"),
    "multiplayer_score": fields.Integer(required=True, help="The multiplayer score of the user"),
})

# Model for returning unauthorized error - 401
unauthorized_model = play_ns.model("UserUnauthorized", {
    'msg': fields.String(example='Missing Authorization Header')
})


# ---------------------
# ====== ROUTES =======
# ---------------------

@play_ns.route("/wortle/leaderboard")
class PlayLeaderboardAPI(Resource):

    # Getting the leaderboard of the Wortle game, sorted by the multiplayer score
    @play_ns.doc(description="Get leaderboard", responses={200: ("Success", play_scores_model)})
    def get(self):
        # Specify the fields we want to query from the database - these are the _id (email) and the games.wortle.singleplayer and games.wortle.multiplayer fields
        projection = {"_id": 1, "games.wortle.singleplayer": 1, "games.wortle.no_singles": 1,
                      "games.wortle.multiplayer": 1, "games.wortle.no_multi": 1}
        # We query using the projection and sort the results by the multiplayer score in descending order
        sorted_users = mongo.db.users.find(
            {}, projection).sort("games.wortle.multiplayer", -1)
        # We return the sorted users as a list of marshaled dictionaries
        return [marshal({"email": user["_id"], "singleplayer_score": user["games"]["wortle"]["singleplayer"], "no_singles": user["games"]["wortle"]["no_singles"], "multiplayer_score": user["games"]["wortle"]["multiplayer"], "no_multi": user["games"]["wortle"]["no_multi"]}, play_scores_model) for user in sorted_users]


@play_ns.route("/user")
class PlayUserScoreAPI(Resource):

    # Getting the score of the logged in user
    @play_ns.doc(description="Get score of logged in user", responses={200: ("Success", play_scores_model), 401: ("Unauthorized", unauthorized_model)})
    @jwt_required()
    def get(self):
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Retrieve the score of the user from the database
        projection = {"_id": 1, "games.wortle.singleplayer": 1, "games.wortle.no_singles": 1,
                      "games.wortle.multiplayer": 1, "games.wortle.no_multi": 1}
        user_data = mongo.db.users.find_one({"_id": current_user}, projection)
        # If the user exists, return the score of the user, else return 404
        if user_data:
            wortle_data = user_data["games"]["wortle"]
            result = {"email": current_user, "singleplayer_score": wortle_data["singleplayer"], "no_singles": wortle_data[
                "no_singles"], "multiplayer_score": wortle_data["multiplayer"], "no_multi": wortle_data["no_multi"]}
            return marshal(result, play_scores_model)
        return {"message": "User not found"}, 404


@play_ns.route("/wortle/singleplayer")
class PlayWortleAPI(Resource):

    # Getting a random 5 character long word from the user's wordbank for the singleplayer Wortle game, if not found, give a random one from a collection
    @play_ns.doc(description="Get a random 5 character long word from the users / else a random one", responses={200: ("Success", wortle_singleplayer_model), 401: ("Unauthorized", unauthorized_model)})
    @jwt_required()
    def get(self):
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Retrieve the user's wordbank from the database
        user_wordbank = mongo.db.users.find_one(
            {"_id": current_user}, {"wordbank": 1})
        # If the user exists, return a random 5 character long word from the user's wordbank or a random 5 character word, else return 404
        if user_wordbank:
            words_with_5_chars = [word for word in user_wordbank.get(
                "wordbank") if len(word) == 5]
            if words_with_5_chars:
                return marshal({"word": random.choice(words_with_5_chars).lower()}, wortle_singleplayer_model)
            else:
                five_letter_words = ["apfel", "birne", "chips", "dachs", "essen", "fisch", "gabel", "junge", "kabel", "lachs", "maler",
                                     "nacht", "opfer", "pilot", "quark", "radar", "sache", "tisch", "umzug", "vogel", "wagen", "xenon", "yacht", "zange"]
                return marshal({"word": random.choice(five_letter_words)}, wortle_singleplayer_model)
        return {"message": "User not found"}, 404

    # Handling the outcome of the singleplayer Wortle game
    @play_ns.doc(description="Handle the outcome of a singleplayer Wortle game", responses={200: ("Success", play_singleplayer_stats_model), 401: ("Unauthorized", unauthorized_model)})
    @play_ns.expect(wortle_singleplayer_outcome_input_model)
    @jwt_required()
    def post(self):
        # Get the outcome of the game - True = won, False = lost
        outcome = play_ns.payload["outcome"]
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Update the user's score in the database accordingly
        score_iter = 0
        if outcome:
            score_iter += 1
        updated = mongo.db.users.find_one_and_update({"_id": current_user}, {"$inc": {
                                                     "games.wortle.no_singles": 1, "games.wortle.singleplayer": score_iter}}, return_document=ReturnDocument.AFTER)
        # Return the updated score of the user
        if updated:
            result = {"email": current_user, "no_singles": updated["games"]["wortle"]
                      ["no_singles"], "singleplayer_score": updated["games"]["wortle"]["singleplayer"]}
            return marshal(result, play_singleplayer_stats_model)
        return {"message": "User not found"}, 404


@play_ns.route("/wortle/multiplayer")
class PlayWortleAPI(Resource):

    # Handling the outcome of a multiplayer Wortle game
    @play_ns.doc(description="Handle the outcome of a multiplayer Wortle game", responses={200: ("Success", play_multiplayer_stats_model), 401: ("Unauthorized", unauthorized_model)})
    @play_ns.expect(wortle_multiplayer_outcome_input_model)
    @jwt_required()
    def post(self):
        # Get the outcome of the game - True = won, False = lost
        outcome = play_ns.payload["outcome"]
        # Get the email of the logged in user
        current_user = get_jwt_identity()
        # Update the user's score in the database accordingly - num games by 1 always, with score_iter being 1 if won, 0 if lost
        score_iter = 0
        if outcome:
            score_iter += 1
        updated = mongo.db.users.find_one_and_update({"_id": current_user}, {"$inc": {
                                                     "games.wortle.no_multi": 1, "games.wortle.multiplayer": score_iter}}, return_document=ReturnDocument.AFTER)
        # Return the updated score of the user
        if updated:
            result = {"email": current_user, "no_multi": updated["games"]["wortle"]
                      ["no_multi"], "multiplayer_score": updated["games"]["wortle"]["multiplayer"]}
            return marshal(result, play_multiplayer_stats_model)
        return {"message": "User not found"}, 404
