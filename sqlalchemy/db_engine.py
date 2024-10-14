from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
import datetime


engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(bind=engine)
# Base.metadata.create_all(engine)


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))

    # I'll set default values for activated, activation_date, and activation_code
    activated: Mapped[bool] = mapped_column(Boolean, default=False)
    activation_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    activation_code: Mapped[str] = mapped_column(String(45), default="N/A")

    # Here we will define the relationship with Home (one user can own multiple homes)
    homes: Mapped[list["Home"]] = relationship(back_populates="owner")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.username!r}, activated={self.activated!r})"


class Home(Base):
    __tablename__ = "home"

    id: Mapped[int] = mapped_column(primary_key=True)
    home_name: Mapped[str] = mapped_column(String(15))

    # Foreign key pointing to the User table
    owned_by: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # We will define the back-populated relationship to User
    owner: Mapped["User"] = relationship(back_populates="homes")


def initialize_db():

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


def main() -> None:
    Base.metadata.create_all(engine)
    initialize_db()

    user2 = User(
        username="username2",
        email="user2email@gmail.com",
        password="user2password",
    )

    with SessionLocal() as session:
        session.add(user2)
        session.commit()

        users = session.query(User).all()
        for user in users:
            print(user)


if __name__ == "__main__":
    main()
