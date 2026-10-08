from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    internship_id = Column(
        Integer,
        ForeignKey("internships.id"),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False,
        default="Applied"
    )

    applied_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    student = relationship("User")

    internship = relationship("Internship")