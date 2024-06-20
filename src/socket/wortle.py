from src.extensions import socketio
from flask_socketio import emit, join_room, leave_room
from flask import request
import random

users_list = {}
invites = {}
games = {}


@socketio.on('authentication')
def handle_authentication(email):
    # Get the sid of the connected client
    sid = request.sid
    # Add the user to the users_list
    users_list[sid] = email
    # print(f"User {email} connected with sid {sid}")
    # print(users_list)
    # Broadcast the updated users_list to all connected clients
    emit('users_list', users_list, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    # Get the sid of the disconnected client
    sid = request.sid
    # Remove the user from the users_list
    users_list.pop(sid, None)
    # Cleanup any hanging invites
    # TODO
    # Cleanup any rooms with hanging games
    # Create a copy of keys to iterate over so that we don't get a runtime error for changing the dictionary while iterating over it
    for room_id in list(games.keys()):
        if sid in room_id:
            game = games.pop(room_id, None)
            # Update the game state, to reset frontend
            emit('game_state', {}, room=room_id)
            # Send a message to the player left in the room that the opponent disconnected

            # Notify the other player and add them back to the 'users_list'
            is_player1 = game["player1"] == sid
            if is_player1:
                users_list[game["player2"]] = game["player2_mail"]
                emit('opponent_disconnected',
                     game["player1_mail"], room=room_id)
                leave_room(room_id, sid=game["player2"])
            else:
                users_list[game["player1"]] = game["player1_mail"]
                emit('opponent_disconnect',
                     game["player2_mail"], room=room_id)
                leave_room(room_id, sid=game["player1"])

    # Broadcast the updated users_list to all connected clients
    emit('users_list', users_list, broadcast=True)


@socketio.on('invite')
def on_invite(invitee):
    invitee_sid = invitee
    inviter_sid = request.sid
    # Check if the invitee is connected
    # print(f"Inviter: {inviter_sid} - {users_list.get(inviter_sid)} invited {invitee_sid} - {users_list.get(invitee_sid)}")
    if invitee_sid not in users_list:
        return
    # Send the invite to the invitee
    invites[inviter_sid] = invitee_sid
    emit('invite', {"id": inviter_sid,
         "email": users_list[inviter_sid]}, to=invitee_sid)


@socketio.on('decline_invite')
def on_decline_invite(inviter_sid):
    invitee_sid = request.sid
    # Check if the inviter is connected
    if inviter_sid not in users_list:
        return
    # Send the decline to the inviter
    invites.pop(inviter_sid, None)
    emit('decline_invite', invitee_sid, to=inviter_sid)


def create_game(inviter_sid, invitee_sid):
    # Create the room ID - for now the combination of their sids does it
    print(f"Creating game for inviter {inviter_sid} and invitee {invitee_sid}")
    room_id = inviter_sid + invitee_sid
    # Randomize the starting player
    players = [inviter_sid, invitee_sid]
    random.shuffle(players)
    player1, player2 = players
    # Initialize the game
    game_state = {
        "room_id": room_id,
        "player1": player1,
        "player1_mail": users_list.get(player1),
        "player2": player2,
        "player2_mail": users_list.get(player2),
        "solution": "WORTL",
        "guesses": [None, None, None, None, None, None],
        "history": [],
        "turn": 0,
        "is_correct": False,
    }
    # Remove users from users_list
    users_list.pop(inviter_sid, None)
    users_list.pop(invitee_sid, None)
    # Store the game state
    games[room_id] = game_state
    return room_id


@socketio.on('accept_invite')
def on_accept_invite(inviter_sid):
    invites.pop(inviter_sid, None)
    invitee_sid = request.sid
    # Create a new room and initialize the game for the two users
    room_id = create_game(inviter_sid, invitee_sid)
    # Join the room
    join_room(room_id, sid=inviter_sid)
    join_room(room_id, sid=invitee_sid)
    print(f"Created game, added {inviter_sid}, {
          invitee_sid} to room ID: {room_id}")
    # Emit the gamestate to the two players
    print("Emitting game state to the two players")
    print(f"Game state: {games[room_id]}")
    emit('game_state', games[room_id], room=room_id)


@socketio.on('update_game_state')
def on_game_update(game_state):
    room_id = game_state.get("room_id")
    # Update the game state
    games[room_id] = game_state
    emit('game_state', game_state, room=room_id)
