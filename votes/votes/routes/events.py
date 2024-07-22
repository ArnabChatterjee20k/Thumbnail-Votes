from flask_socketio import emit, join_room, leave_room, disconnect, ConnectionRefusedError
import functools , json
from votes.services.VoteCache import vote_manager
from votes.publisher import publish_upvote
from flask import request
from .. import socketio

cache = vote_manager


@socketio.on("connect")
def user_connect_and_validate():
    """
        somehow getting headers not working in flask_socketio
        so we will pass data for auth through querystring
        we can authenticate here as well
        but since its a service and will be connected through a gateway so using not verifying directly
    """
    args = request.args
    user_id = args.get("email")
    project_id = args.get("project_id")
    print(project_id,user_id)
    if not user_id or not project_id:
        print("error")
        raise ConnectionRefusedError("unauthorised")
    join_room(room=project_id)
    cache.cache_votes(int(project_id))


@socketio.on("vote")
def client_vote(message: dict):
    """
        if client got connected then automatically it will get the args on every event
    """
    args = request.args
    user_id = args.get("email")
    thumbnail_id = json.loads(message).get("thumbnail_id")
    project_id = int(args.get("project_id"))
    if not thumbnail_id or thumbnail_id not in cache[project_id]:
        return
    thumbnail_upvoters: list = cache[project_id][thumbnail_id]
    if user_id in thumbnail_upvoters:
        return
    # TODO: send results every 2mins
    join_room(project_id)
    publish_upvote(user_id, thumbnail_id=thumbnail_id)