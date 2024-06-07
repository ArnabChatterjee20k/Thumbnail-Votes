from typing import Iterator
from votes.utils.vote import get_vote,get_voters
class VoteManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VoteManager, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        self._votes = {}

    def __getitem__(self, project_id):
        return self._votes.__getitem__(project_id)

    def __setitem__(self, key, value):
        self._votes.__setitem__(key, value)

    def __iter__(self) -> Iterator:
        return self._votes.__iter__()

    def __len__(self) -> int:
        return self._votes.__len__()

    def __repr__(self) -> str:
        return str(self._votes)

    def pop(self, project_id):
        if project_id in self._votes:
            return self._votes.pop(project_id)
        return None

    def cache_votes(self,project_id):
        if project_id in self._votes:
            return self._votes[project_id]
        thumbnails = self._cache_thumbnails(project_id)
        for thumbnail in thumbnails:
            self._cache_voters(project_id,thumbnail.thumbnail_id)
        return self._votes[project_id]

    def _cache_thumbnails(self,project_id):
        try:
            vote = get_vote(project_id=project_id)
            if vote:
                self._votes[project_id] = {data.thumbnail_id:[] for data in vote}
            return vote
        except Exception as e:
            print(e)
            return None

    def _cache_voters(self,project_id,thumbnail_id):
        voters = get_voters(thumbnail_id=thumbnail_id)
        for voter in voters:
            self._votes[project_id][voter.thumbnail_voted].append(voter.user_id)