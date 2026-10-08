from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from database import engine, get_db, Base
from models import User
from student_model import Student
from skill_model import Skill
from certificate_model import Certificate
from internship_model import Internship
from application_model import Application

from schemas import (
    UserCreate, UserLogin, StudentProfileCreate,
    SkillCreate, SkillUpdate, CertificateCreate,
    CertificateUpdate, InternshipCreate, InternshipUpdate,
    ApplicationCreate, ApplicationStatusUpdate,
)
from security import hash_password, verify_password
from auth import create_access_token, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkillBridge API", description="Internship and Skill Tracking Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "SkillBridge API is running!"}

@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "MySQL connection successful!"}
    except Exception as error:
        return {"message": "MySQL connection failed.", "error": str(error)}

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    return current_user

# --- FIX: MISSING STATS ENDPOINT (was breaking AdminDashboard) ---
@app.get("/admin/stats")
def get_admin_stats(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    return {
        "students": db.query(func.count(User.id)).filter(User.role == "student").scalar() or 0,
        "internships": db.query(func.count(Internship.id)).scalar() or 0,
        "applications": db.query(func.count(Application.id)).scalar() or 0,
        "certificates": db.query(func.count(Certificate.id)).scalar() or 0,
    }

@app.get("/admin/students")
def get_all_students(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    students = db.query(User, Student).outerjoin(Student, User.id == Student.user_id).filter(User.role == "student").order_by(User.id.desc()).all()
    return [{"id": user.id, "name": user.name, "email": user.email, "role": user.role, "created_at": user.created_at, "profile": {"id": student.id, "phone": student.phone, "university": student.university, "course": student.course, "bio": student.bio, "github_url": student.github_url, "linkedin_url": student.linkedin_url} if student else None} for user, student in students]

@app.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered.")
    new_user = User(name=user_data.name, email=user_data.email, password=hash_password(user_data.password), role=user_data.role)
    db.add(new_user); db.commit(); db.refresh(new_user)
    return {"message": "User registered successfully!", "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email, "role": new_user.role}}

@app.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    token = create_access_token(user.id, user.role)
    return {"message": "Login successful!", "access_token": token, "token_type": "bearer", "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}}

@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "name": current_user.name, "email": current_user.email, "role": current_user.role}

@app.post("/student-profile")
def create_student_profile(profile_data: StudentProfileCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if db.query(Student).filter(Student.user_id == current_user.id).first():
        raise HTTPException(status_code=400, detail="Student profile already exists.")
    new_profile = Student(user_id=current_user.id, phone=profile_data.phone, university=profile_data.university, course=profile_data.course, bio=profile_data.bio, github_url=profile_data.github_url, linkedin_url=profile_data.linkedin_url)
    db.add(new_profile); db.commit(); db.refresh(new_profile)
    return {"message": "Student profile created successfully!", "profile": {"id": new_profile.id, "user_id": new_profile.user_id, "phone": new_profile.phone, "university": new_profile.university, "course": new_profile.course, "bio": new_profile.bio, "github_url": new_profile.github_url, "linkedin_url": new_profile.linkedin_url}}

@app.get("/student-profile")
def get_student_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not profile: raise HTTPException(status_code=404, detail="Student profile not found.")
    return {"id": profile.id, "user_id": profile.user_id, "phone": profile.phone, "university": profile.university, "course": profile.course, "bio": profile.bio, "github_url": profile.github_url, "linkedin_url": profile.linkedin_url}

@app.put("/student-profile")
def update_student_profile(profile_data: StudentProfileCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not profile:
        profile = Student(user_id=current_user.id); db.add(profile)
    profile.phone = profile_data.phone; profile.university = profile_data.university; profile.course = profile_data.course; profile.bio = profile_data.bio; profile.github_url = profile_data.github_url; profile.linkedin_url = profile_data.linkedin_url
    db.commit(); db.refresh(profile)
    return {"message": "Student profile updated successfully!", "profile": {"id": profile.id, "user_id": profile.user_id, "phone": profile.phone, "university": profile.university, "course": profile.course, "bio": profile.bio, "github_url": profile.github_url, "linkedin_url": profile.linkedin_url}}

@app.post("/skills")
def create_skill(skill_data: SkillCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student: raise HTTPException(status_code=404, detail="Student profile not found.")
    new_skill = Skill(student_id=student.id, skill_name=skill_data.skill_name, skill_level=skill_data.skill_level)
    db.add(new_skill); db.commit(); db.refresh(new_skill)
    return {"id": new_skill.id, "student_id": new_skill.student_id, "skill_name": new_skill.skill_name, "skill_level": new_skill.skill_level}

@app.get("/skills")
def get_skills(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student: raise HTTPException(status_code=404, detail="Student profile not found.")
    skills = db.query(Skill).filter(Skill.student_id == student.id).all()
    return [{"id": s.id, "student_id": s.student_id, "skill_name": s.skill_name, "skill_level": s.skill_level} for s in skills]

@app.put("/skills/{skill_id}")
def update_skill(skill_id: int, skill_data: SkillUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    skill = db.query(Skill).filter(Skill.id == skill_id, Skill.student_id == student.id).first() if student else None
    if not skill: raise HTTPException(status_code=404, detail="Skill not found.")
    skill.skill_name = skill_data.skill_name; skill.skill_level = skill_data.skill_level; db.commit(); db.refresh(skill)
    return {"id": skill.id, "student_id": skill.student_id, "skill_name": skill.skill_name, "skill_level": skill.skill_level}

@app.delete("/skills/{skill_id}")
def delete_skill(skill_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    skill = db.query(Skill).filter(Skill.id == skill_id, Skill.student_id == student.id).first() if student else None
    if not skill: raise HTTPException(status_code=404, detail="Skill not found.")
    db.delete(skill); db.commit(); return {"message": "Skill deleted successfully!"}

@app.post("/certificates")
def create_certificate(certificate_data: CertificateCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student: raise HTTPException(status_code=404, detail="Student profile not found.")
    new_certificate = Certificate(student_id=student.id, certificate_name=certificate_data.certificate_name, issuer=certificate_data.issuer, issue_date=certificate_data.issue_date, credential_id=certificate_data.credential_id, credential_url=certificate_data.credential_url)
    db.add(new_certificate); db.commit(); db.refresh(new_certificate)
    return {"id": new_certificate.id, "student_id": new_certificate.student_id, "certificate_name": new_certificate.certificate_name, "issuer": new_certificate.issuer, "issue_date": new_certificate.issue_date, "credential_id": new_certificate.credential_id, "credential_url": new_certificate.credential_url}

@app.get("/certificates")
def get_certificates(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student: raise HTTPException(status_code=404, detail="Student profile not found.")
    certificates = db.query(Certificate).filter(Certificate.student_id == student.id).all()
    return [{"id": c.id, "student_id": c.student_id, "certificate_name": c.certificate_name, "issuer": c.issuer, "issue_date": c.issue_date, "credential_id": c.credential_id, "credential_url": c.credential_url} for c in certificates]

@app.put("/certificates/{certificate_id}")
def update_certificate(certificate_id: int, certificate_data: CertificateUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id, Certificate.student_id == student.id).first() if student else None
    if not certificate: raise HTTPException(status_code=404, detail="Certificate not found.")
    certificate.certificate_name = certificate_data.certificate_name; certificate.issuer = certificate_data.issuer; certificate.issue_date = certificate_data.issue_date; certificate.credential_id = certificate_data.credential_id; certificate.credential_url = certificate_data.credential_url
    db.commit(); db.refresh(certificate)
    return {"id": certificate.id, "student_id": certificate.student_id, "certificate_name": certificate.certificate_name, "issuer": certificate.issuer, "issue_date": certificate.issue_date, "credential_id": certificate.credential_id, "credential_url": certificate.credential_url}

@app.delete("/certificates/{certificate_id}")
def delete_certificate(certificate_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id, Certificate.student_id == student.id).first() if student else None
    if not certificate: raise HTTPException(status_code=404, detail="Certificate not found.")
    db.delete(certificate); db.commit(); return {"message": "Certificate deleted successfully!"}

@app.post("/internships")
def create_internship(internship_data: InternshipCreate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    new_internship = Internship(company_name=internship_data.company_name, job_title=internship_data.job_title, description=internship_data.description, location=internship_data.location, work_type=internship_data.work_type, duration=internship_data.duration, application_deadline=internship_data.application_deadline, requirements=internship_data.requirements, status=internship_data.status, created_by=current_user.id)
    db.add(new_internship); db.commit(); db.refresh(new_internship)
    # Return direct object for frontend compatibility
    return {"id": new_internship.id, "company_name": new_internship.company_name, "job_title": new_internship.job_title, "description": new_internship.description, "location": new_internship.location, "work_type": new_internship.work_type, "duration": new_internship.duration, "application_deadline": new_internship.application_deadline, "requirements": new_internship.requirements, "status": new_internship.status, "created_by": new_internship.created_by}

@app.get("/internships")
def get_internships(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    internships = db.query(Internship).order_by(Internship.id.desc()).all()
    return [{"id": i.id, "company_name": i.company_name, "job_title": i.job_title, "description": i.description, "location": i.location, "work_type": i.work_type, "duration": i.duration, "application_deadline": i.application_deadline, "requirements": i.requirements, "status": i.status, "created_by": i.created_by} for i in internships]

@app.put("/internships/{internship_id}")
def update_internship(internship_id: int, internship_data: InternshipUpdate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    internship = db.query(Internship).filter(Internship.id == internship_id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found.")
    
    # Update only if value is provided - fake company check nathuwa
    internship.company_name = internship_data.company_name
    internship.job_title = internship_data.job_title
    internship.description = internship_data.description
    internship.location = internship_data.location
    internship.work_type = internship_data.work_type
    internship.duration = internship_data.duration
    internship.application_deadline = internship_data.application_deadline
    internship.requirements = internship_data.requirements
    internship.status = internship_data.status
    
    db.commit()
    db.refresh(internship)
    return {
        "id": internship.id, 
        "company_name": internship.company_name, 
        "job_title": internship.job_title, 
        "description": internship.description, 
        "location": internship.location, 
        "work_type": internship.work_type, 
        "duration": internship.duration, 
        "application_deadline": internship.application_deadline, 
        "requirements": internship.requirements, 
        "status": internship.status, 
        "created_by": internship.created_by,
        "message": "Updated successfully!"
    }


@app.delete("/internships/{internship_id}")
def delete_internship(internship_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    internship = db.query(Internship).filter(Internship.id == internship_id).first()
    if not internship: raise HTTPException(status_code=404, detail="Internship not found.")
    db.query(Application).filter(Application.internship_id == internship_id).delete()
    db.delete(internship); db.commit()
    return {"message": "Internship deleted successfully!"}

@app.post("/applications")
def apply_for_internship(application_data: ApplicationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    internship = db.query(Internship).filter(Internship.id == application_data.internship_id).first()
    if not internship: raise HTTPException(status_code=404, detail="Internship not found.")
    if internship.status != "Open": raise HTTPException(status_code=400, detail="This internship is no longer open.")
    if db.query(Application).filter(Application.student_id == current_user.id, Application.internship_id == application_data.internship_id).first():
        raise HTTPException(status_code=400, detail="You have already applied for this internship.")
    new_application = Application(student_id=current_user.id, internship_id=application_data.internship_id, status="Applied")
    db.add(new_application); db.commit(); db.refresh(new_application)
    return {"id": new_application.id, "student_id": new_application.student_id, "internship_id": new_application.internship_id, "status": new_application.status, "applied_at": new_application.applied_at}

@app.get("/applications")
def get_my_applications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    applications = db.query(Application).filter(Application.student_id == current_user.id).order_by(Application.id.desc()).all()
    return [{"id": a.id, "student_id": a.student_id, "internship_id": a.internship_id, "status": a.status, "applied_at": a.applied_at} for a in applications]

@app.get("/admin/applications")
def get_all_applications(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    applications = db.query(Application, User, Internship).join(User, Application.student_id == User.id).join(Internship, Application.internship_id == Internship.id).order_by(Application.id.desc()).all()
    return [{"id": app.id, "student_id": user.id, "student_name": user.name, "student": {"id": user.id, "name": user.name, "email": user.email}, "internship_id": intern.id, "internship": {"id": intern.id, "company_name": intern.company_name, "job_title": intern.job_title, "location": intern.location, "work_type": intern.work_type, "duration": intern.duration}, "status": app.status, "applied_at": app.applied_at} for app, user, intern in applications]

@app.put("/admin/applications/{application_id}/status")
def update_application_status(application_id: int, status_data: ApplicationStatusUpdate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found.")
    
    application.status = status_data.status
    db.commit()
    db.refresh(application)
    return {"id": application.id, "status": application.status}

    
@app.put("/applications/{application_id}/status")
def update_application_status(application_id: int, status_data: ApplicationStatusUpdate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application: raise HTTPException(status_code=404, detail="Application not found.")
    if status_data.status not in ["Applied", "Under Review", "Shortlisted", "Rejected", "Accepted"]:
        raise HTTPException(status_code=400, detail="Invalid application status.")
    application.status = status_data.status; db.commit(); db.refresh(application)
    return {"id": application.id, "student_id": application.student_id, "internship_id": application.internship_id, "status": application.status, "applied_at": application.applied_at}