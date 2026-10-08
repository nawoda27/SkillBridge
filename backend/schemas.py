from pydantic import BaseModel, EmailStr
from datetime import date, datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "student"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class StudentProfileCreate(BaseModel):
    phone: str | None = None
    university: str | None = None
    course: str | None = None
    bio: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None


class SkillCreate(BaseModel):
    skill_name: str
    skill_level: str | None = None


class SkillUpdate(BaseModel):
    skill_name: str
    skill_level: str | None = None


class CertificateCreate(BaseModel):
    certificate_name: str
    issuer: str
    issue_date: date | None = None
    credential_id: str | None = None
    credential_url: str | None = None


class CertificateUpdate(BaseModel):
    certificate_name: str
    issuer: str
    issue_date: date | None = None
    credential_id: str | None = None
    credential_url: str | None = None


class InternshipCreate(BaseModel):
    company_name: str
    job_title: str
    description: str | None = None
    location: str | None = None
    work_type: str | None = None
    duration: str | None = None
    application_deadline: datetime | None = None
    requirements: str | None = None
    status: str = "Open"


class InternshipUpdate(BaseModel):
    company_name: str
    job_title: str
    description: str | None = None
    location: str | None = None
    work_type: str | None = None
    duration: str | None = None
    application_deadline: datetime | None = None
    requirements: str | None = None
    status: str


class ApplicationCreate(BaseModel):
    internship_id: int


class ApplicationStatusUpdate(BaseModel):
    status: str