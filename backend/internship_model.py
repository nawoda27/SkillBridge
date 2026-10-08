from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Internship(Base):
    __tablename__= "internships"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String(150), nullable=False)
    job_title = Column(String(200), nullable=False)

    description = Column(Text, nullable=True)

    location = Column(String(150), nullable=True)
    work_type = Column(String(50), nullable=True)

    duration = Column(String(50), nullable=True)

    application_deadline = Column(Date, nullable=True)

    requirements = Column(Text, nullable=True)

    status = Column(
        String(30),
        nullable=False,
        default="Open"
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    creator = relationship("User")