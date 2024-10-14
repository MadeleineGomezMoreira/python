from models import User
from sqlalchemy.orm import Session


# Save a new user
def save_user(session: Session, user: User):
    session.add(user)
    session.commit()
    return user


# Delete an existing user by user.id
def delete_user(session: Session, user_id: int):
    user = session.query(User).filter_by(id=user_id).first()

    if user:
        session.delete(user)
        session.commit()


# Update an existing user (works the same as save)
def update_user(session: Session, user: User):
    session.add(user)
    session.commit()


# Find all users
def get_all_users(session: Session):
    return session.query(User).all()


# Find a user by user_id
def get_user_by_id(session: Session, user_id: int):
    return session.query(User).filter_by(id=user_id).first()


# Find a user by username
def get_user_by_username(session: Session, username: str):
    return session.query(User).filter_by(username=username).first()
