from votes.services.VoteCache import vote_manager
def is_voted(user_id,project_id):
    cache = vote_manager
    vote = cache.cache_votes(project_id)
    voters = [voter for thumbnail_voters in vote.values() for voter in thumbnail_voters]
    return user_id in voters