from models import Home
from sqlalchemy.orm import Session

# TODO: implement error handling


# Save a new home
def save_home(session: Session, home: Home):
    session.add(home)
    session.commit()
    return home


# Update an existing home (works the same as save)
def update_home(session: Session, home: Home):
    session.add(home)
    session.commit()


# Find all homes
def get_all_homes(session: Session):
    return session.query(Home).all()


# Find all homes by owner
def get_all_homes_by_owner(session: Session, owner_id: int):
    return session.query(Home).filter_by(owned_by=owner_id).all()


# Find a home by home_id
def get_home_by_id(session: Session, home_id: int):
    return session.query(Home).filter_by(id=home_id).first()


# Find a home by owner (owned_by -> user.id)
def get_home_by_owner(session: Session, owner_id: int):
    return session.query(Home).filter_by(owned_by=owner_id).first()
