from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import Base, Home, User


engine = create_async_engine(
    "sqlite+aiosqlite:///db.sqlite3",
    connect_args={"check_same_thread": False},
    echo=True,
)
SessionLocal = async_sessionmaker(engine)


def input_sample_data():

    with SessionLocal() as session:

        print("Inputting sample data...")  # Agregar esta línea para verificar

        user1 = User(
            username="username1",
            email="user1email@gmail.com",
            password="user1password",
        )

        session.add(user1)
        session.commit()

        # Query the inserted user to retrieve its id
        user = session.query(User).first()

        home1 = Home(
            home_name="Home1",
            owner=user,  # We use the relationship between the two entities to assign the user (owned_by)
        )

        session.add(home1)
        session.commit()


# This will get the DB Session for each request


async def get_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
