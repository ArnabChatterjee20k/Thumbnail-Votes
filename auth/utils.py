import jwt
from passlib.hash import sha256_crypt
from db import Session, User
from sqlalchemy import select


def create_token(email):
    return jwt.encode({"email": email}, "c2VyCg==", algorithm="HS256")


def decode_token(encoded):
    return jwt.decode(encoded, "c2VyCg==", algorithms="HS256")


def get_hash_password(password):
    return sha256_crypt.hash(password)


def decode_password(hash):
    return sha256_crypt.verify(hash)


def save_user(name, email, password_hash):
    with Session() as session:
        user = User(name=name, email=email, password=password_hash)
        session.add(user)
        session.commit()


def get_user(email):
    with Session() as session:
        query = select(User).where(User.email == email)
        result = session.scalar(query)
        return result