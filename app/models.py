from sqlalchemy import Column, Integer, String
from .database import Base


class MedicalStaff(Base):
    __tablename__ = "medical_staff"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(20),
        nullable=False
    )