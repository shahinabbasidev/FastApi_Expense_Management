from faker import Faker
from core.database import SessionLocal
from sqlalchemy.orm import Session
from users.models import UserModel
from expenses.models import ExpenseModel
from datetime import datetime
import random

fake = Faker()


def seed_users(db):
    user = UserModel(
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    user.set_password("12345678")
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"User create whit Username: {user.username} and ID: {user.id}")
    return user


def seed_expenses(db, user, count=10):
    expenses_list = []
    for _ in range(count):
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
        db.add(expenses)
        db.commit()
        db.refresh(expenses)
        print(f"added 10 Expenses for user id {user.id}")


def main():
    db = SessionLocal()
    try:
        user = seed_users(db)
        seed_expenses(db, user)
    finally:
        db.close()


if __name__ == "__main__":
    main()
