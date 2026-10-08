from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Certificate(Base):
    __tablename__= "certificates"

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

    certificate_name = Column(
        String(200),
        nullable=False
    )

    issuer = Column(
        String(150),
        nullable=False
    )

    issue_date = Column(
        Date,
        nullable=True
    )

    credential_id = Column(
        String(150),
        nullable=True
    )

    credential_url = Column(
        String(255),
        nullable=True
    )

    student = relationship(
        "Student",
        backref="certificates"
    )