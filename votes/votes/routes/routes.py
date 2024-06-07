from flask import Blueprint
from werkzeug.exceptions import NotFound
from votes.services.VoteCache import vote_manager
from . import main as router

cache = vote_manager

@router.get("/<int:project_id>")
def vote_home(project_id):
    vote = cache.cache_votes(project_id)
    print(cache)
    if not vote:
        return NotFound()
    return vote