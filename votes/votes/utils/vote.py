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
def add_thumbnail(session:Session,project_id,thumbnail_id,admin_id):
    vote = Vote(project_id=project_id,thumbnail_id=thumbnail_id,admin_id=admin_id)
    session.add(vote)
    session.commit()

@with_db_session()
def get_vote(session:Session,project_id):
    query = select(Vote).where(Vote.project_id == project_id).with_for_update()
    return session.execute(query).scalars().all()

@with_db_session()
def get_voters(session:Session,thumbnail_id):
    query = select(Voters).where(Voters.thumbnail_voted == thumbnail_id)
    return session.execute(query).scalars().all()

@with_db_session()
def up_vote(session:Session,user_id,thumbnail_id):    
    voter = Voters(user_id=user_id,thumbnail_voted=thumbnail_id)
    session.add(voter)
    session.commit()

@with_db_session()
def get_admin(session:Session,project_id):
    query = select(Vote).where(Vote.project_id == project_id)
    vote = session.execute(query).scalar_one_or_none()
    if vote:
        return vote.admin_id
    return None