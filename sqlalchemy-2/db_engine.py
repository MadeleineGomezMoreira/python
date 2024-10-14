from sqlalchemy import create_engine
from models import Base, Home, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def initialize_db():

    Base.metadata.create_all(engine)


def input_sample_data():

    with SessionLocal() as session:
        user_count = session.query(User).count()

        if user_count == 0:

            user1 = User(
                username="username1",
                email="user1email@gmail.com",
                password="user1password",
            )

            session.add(user1)
            session.commit()

        home_count = session.query(Home).count()

        if home_count == 0:

            # Query the inserted user to retrieve its id
            user = session.query(User).first()

            home1 = Home(
                home_name="Home1",
                owner=user,  # We use the relationship between the two entities to assign the user (owned_by)
            )

            session.add(home1)
            session.commit()
