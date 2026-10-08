from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    skill_name = Column(
        String(100),
        nullable=False
    )

    skill_level = Column(
        String(50),
        nullable=True
    )

    student = relationship(
        "Student",
        backref="skills"
    )