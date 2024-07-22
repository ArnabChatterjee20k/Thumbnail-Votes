from flask import request,jsonify
from werkzeug.exceptions import NotFound, BadRequest
from votes.services.VoteCache import vote_manager
from votes.decorators.is_loggedin import is_loggedin
from votes.publisher import publish_upvote
from votes.utils.vote import up_vote
from votes.utils.is_voted import is_voted
from . import main as router

cache = vote_manager

@router.get("/<int:project_id>")
@is_loggedin
def vote_home(project_id):
    vote = cache.cache_votes(project_id)
    if not vote:
        return NotFound()
    print(cache)
    body = request.args
    email = body.get("email")
    print(cache)
    voters = [voter for thumbnail_voters in vote.values() for voter in thumbnail_voters]
    voted = email in voters
    response = {"voted":voted,"results":vote if voted else {}}
    return response

@router.post("/<int:project_id>/<string:thumbnail_id>")
@is_loggedin
def upvote(project_id,thumbnail_id):
    body = request.args
    email = body.get("email")
    if is_voted(email,project_id):
        return BadRequest()
    up_vote(email,thumbnail_id)
    publish_upvote(email,project_id,thumbnail_id)
    cache.pop(project_id)
    return {"status":"success"},201

@router.get("/cache")
def get_cache():
    """For celery scheduler"""
    return jsonify(cache.to_json())