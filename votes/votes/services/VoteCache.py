from typing import Iterator

class VoteManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VoteManager, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        self._votes = {}

    def __getitem__(self, vote_id):
        return self._votes.__getitem__(vote_id)

    def __setitem__(self, key, value):
        self._votes.__setitem__(key, value)

    def __iter__(self) -> Iterator:
        return self._votes.__iter__()

    def __len__(self) -> int:
        return self._votes.__len__()

    def pop(self, vote_id):
        if self.__getitem__(vote_id):
            return self._votes.pop(vote_id)
        return None
