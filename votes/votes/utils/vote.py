from votes.models import Vote,Voters
from votes.db import Session as BindSession
from sqlalchemy.orm import Session
from sqlalchemy import select
import contextlib

class with_db_session(contextlib.ContextDecorator):
    def __enter__(self):
        self.session = BindSession()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        if exc_type:
            raise Exception(exc_val)
        
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with self:
                return func(self.session, *args, **kwargs)
        return wrapper

@with_db_session()
def add_thumbnail(session:Session,project_id,thumbnail_id):
    vote = Vote(project_id=project_id,thumbnail_id=thumbnail_id)
    session.add(vote)
    session.commit()

@with_db_session()
def get_vote(session:Session,vote_id):
    query = select(Vote.id).where(Vote.id == vote_id).with_for_update()
    return session.execute(query).scalar_one()

@with_db_session()
def up_vote(session:Session,user_id,vote_id):    
    voter = Voters(user_id=user_id,vote_id=vote_id)
    session.add(voter)
    session.commit()