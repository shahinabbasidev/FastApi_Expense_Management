import os
# ensure settings loads without errors during testing
os.environ.setdefault("SQLALCHEMY_DATABASE_URL", "sqlite:///:memory:")

from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from core.database import Base,create_engine,sessionmaker,get_db
from main import app
import pytest
from faker import Faker
from users.models import UserModel
from expenses.models import ExpenseModel
from auth.jwt_cookie_auth import generate_access_token
import random

fake = Faker()

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# module
@pytest.fixture(scope="package")
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# module
@pytest.fixture(scope="module",autouse=True)
def override_dependencies(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db,None)


# session
@pytest.fixture(scope="session",autouse=True)
def tear_up_and_down_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# function
@pytest.fixture(scope="function")
def anon_client():
    # fresh TestClient for each test to avoid cookie carry‑over
    client = TestClient(app)
    yield client
    
@pytest.fixture(scope="function")
def auth_client(db_session):
    client = TestClient(app)
    user = db_session.query(UserModel).filter_by(username="testuser").one()
    access_token = generate_access_token(user.id)
    # authentication is based on cookies in this project
    client.cookies.set("access_token", access_token)
    yield client



@pytest.fixture(scope="package",autouse=True)
def generate_mock_data(db_session):
    # create a deterministic user so tests can rely on the credentials
    user = UserModel(
        username="testuser",
        first_name="Test",
        last_name="User",
    )
    # use a simple known password
    user.set_password("testpass")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    print(f"User created with Username: {user.username} and ID: {user.id}")

    # add a handful of expenses for the test user
    for i in range(10):
        created_at = fake.date_time_between(start_date="-6M", end_date="now")

        expense = ExpenseModel(
            user_id=user.id,
            expense_name=fake.word(),
            mount=random.randint(50_000, 5_000_000),
            create_date=created_at,
            update_date=fake.date_time_between(
                start_date=created_at, end_date="now"
            ),
        )
        db_session.add(expense)
        db_session.commit()
        db_session.refresh(expense)
        print(f"added expense {i+1} for user id {user.id}")

@pytest.fixture(scope="function")
def random_task(db_session):
    user = db_session.query(UserModel).filter_by(username="testuser").one()
    expense = db_session.query(ExpenseModel).filter_by(user_id=user.id).first()
    return expense
