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
@pytest.fixture(scope="package")
def anon_client():
    client = TestClient(app)
    yield client
    
@pytest.fixture(scope="package")
def auth_client(db_session):
    client = TestClient(app)
    user = db_session.query(UserModel).filter_by(username="testuser").one()
    access_token = generate_access_token(user.id)
    client.headers.update({"Authorization":f"Bearer {access_token}"})
    yield client



@pytest.fixture(scope="package",autouse=True)
def generate_mock_data(db_session):
    user = UserModel(
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    user.set_password("12345678")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    print(f"User create whit Username: {user.username} and ID: {user.id}")

    expenses_list = []
    for _ in range(10):
        created_at = fake.date_time_between(start_date="-6M", end_date="now")

        expenses = ExpenseModel(
            user_id=user.id,
            expense_name=fake.word(),  # یا fake.sentence(nb_words=2)
            mount=random.randint(50_000, 5_000_000),
            create_date=created_at,
            update_date=fake.date_time_between(
                start_date=created_at, end_date="now"
            ),
        )

        expenses_list.append(expenses)
        db_session.add(expenses)
        db_session.commit()
        db_session.refresh(expenses)
        print(f"added 10 Expenses for user id {user.id}")

@pytest.fixture(scope="function")
def random_task(db_session):
    user = db_session.query(UserModel).filter_by(username="testuser").one()
    expense = db_session.query(ExpenseModel).filter_by(user_id=user.id).first()
    return expense
