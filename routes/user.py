from fastapi import APIRouter, Response, status
from config.db import engine, conn
from models.user import User
from schemas.user import UserScheme
from sqlalchemy.orm import sessionmaker
from starlette.status import HTTP_204_NO_CONTENT

from cryptography.fernet import Fernet

user = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


@user.get("/users", response_model=list[UserScheme], tags=["users"])
def get_users():
    users = session.query(User).all()
    return users


@user.post("/users", response_model=UserScheme, tags=["users"])
def create_user(user: UserScheme):

    new_user = User(
        name=user.name, email=user.email,
        password=f.encrypt(user.password.encode("utf-8")))
    session.add(new_user)
    session.commit()
    return "User created succesfully"


@user.get("/users/{id}", response_model=UserScheme, tags=["users"])
def get_user(id: int):
    user = session.query(User).get(id)
    return user


@user.delete("/users/{id}", status_code=HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: int):
    session.query(User).filter(User.id == id).delete()
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@user.put("/users/{id}", response_model=UserScheme, tags=["users"])
def update_user(id: int, user_data: UserScheme):
    user = session.query(User).get(id)

    user.name = user_data.name
    user.email = user_data.email
    user.password = f.encrypt(user_data.password.encode("utf-8"))

    session.commit()
    return "User updated succesfully"
