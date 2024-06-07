from flask_socketio import emit, join_room, leave_room, disconnect,ConnectionRefusedError
import functools
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
    """
    args = request.args
    user_id = args.get("user_id")
    project_id = args.get("project_id")
    if not user_id or not project_id:
        raise ConnectionRefusedError("unauthorised")

    cache.cache_votes(int(project_id))


@socketio.on("vote")
def client_vote(message:dict):
    """
        if client got connected then automatically it will get the args on every event
    """
    args = request.args
    user_id = int(args.get("user_id"))
    thumbnail_id = message.get("thumbnail_id")
    project_id = int(args.get("project_id"))
    if not thumbnail_id or thumbnail_id not in cache[project_id]:
        return
    thumbnail_upvoters:list = cache[project_id][thumbnail_id]
    if user_id in thumbnail_upvoters:
        return
    publish_upvote(user_id,thumbnail_id=thumbnail_id)
