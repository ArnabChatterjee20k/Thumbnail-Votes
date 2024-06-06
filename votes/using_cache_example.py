from votes.models import *
from votes.db import create_db
from votes.services.VoteCache import VoteManager
from votes.utils.vote import add_thumbnail,up_vote
# add_thumbnail(project_id=24,thumbnail_id=12)
# add_thumbnail(project_id=23,thumbnail_id=11)
cache = VoteManager()
cache.cache_votes(12)
cache.pop(23)
cache.cache_votes(23)
for i in cache:
    print(i,cache[i])