from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    phone = Column(
        String(20),
        nullable=True
    )

    university = Column(
        String(150),
        nullable=True
    )

    course = Column(
        String(150),
        nullable=True
    )

    bio = Column(
        Text,
        nullable=True
    )

    github_url = Column(
        String(255),
        nullable=True
    )

    linkedin_url = Column(
        String(255),
        nullable=True
    )

    user = relationship(
        "User",
        backref="student_profile"
    )
