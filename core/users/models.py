from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    Text,
    Boolean,
    Table,
    ForeignKey,
    create_engine,
)
from sqlalchemy.orm import relationship
from core.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=True)
    username = Column(String(120), nullable=False, unique=True)
    password = Column(Text(200), nullable=False)
    is_active = Column(Boolean, default=True)
    create_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), server_default=func.now())

    expenses = relationship("ExpenseModel", back_populates="user",cascade="all, delete-orphan")

    @staticmethod
    def hash_password(plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    def set_password(self, plain_text: str):
        self.password = self.hash_password(plain_text)
