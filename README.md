🎓 SkillBridge

SkillBridge is a web-based internship management platform designed to help students discover internship opportunities, manage their career information, and track internship applications.

The project is developed as a full-stack portfolio project using React, FastAPI, MySQL, and SQLAlchemy, with JWT-based authentication and role-based access control.

---

✨ Features

👨‍🎓 Student Features

- Student registration and login
- JWT-based authentication
- Student profile management
- Skills management
- Certificate management
- Browse internship opportunities
- View internship details
- Apply for internships
- View submitted applications
- Track application status

👨‍💼 Admin Features

- Secure admin login
- Admin dashboard
- Internship management
- Create internship opportunities
- Edit internship details
- Delete internships
- Manage internship status
- View student applications
- Update application statuses
- View internship and application statistics

---

🛠️ Technology Stack

Frontend

- React
- Vite
- JavaScript
- HTML
- CSS

Backend

- Python
- FastAPI
- SQLAlchemy
- JWT Authentication
- bcrypt

Database

- MySQL
- PyMySQL

Development Tools

- Visual Studio Code
- Git
- GitHub
- XAMPP

---

👥 User Roles

SkillBridge provides role-based functionality for two main user types.

Student

Students can:

- Create an account
- Log in securely
- Manage their profile
- Add and manage skills
- Add and manage certificates
- Browse internships
- Submit internship applications
- Track their applications

Admin

Administrators can:

- Log in through the admin account
- View the admin dashboard
- Manage internship opportunities
- View student applications
- Update application statuses
- Monitor platform activity

---

🗄️ Database

SkillBridge uses MySQL as its relational database.

The main entities include:

users
students
skills
certificates
internships
applications

The backend uses SQLAlchemy ORM for database operations.

---

🔐 Authentication & Security

The application uses:

- JWT access tokens
- bcrypt password hashing
- Role-based access control
- Protected API endpoints
- Admin-only API operations

Sensitive credentials and secrets should be configured through environment variables when deploying the application.

---

🚀 Getting Started

Prerequisites

Make sure you have installed:

- Python 3.x
- Node.js
- npm
- MySQL
- Git

---

⚙️ Backend Setup

Clone the repository:

git clone https://github.com/nawoda27/SkillBridge.git

Move into the project:

cd SkillBridge

Go to the backend:

cd backend

Create a virtual environment:

python -m venv venv

Activate the virtual environment on Windows:

venv\Scripts\activate

Install the Python dependencies:

pip install -r requirements.txt

Make sure MySQL is running and the "skillbridge" database is configured.

Start the FastAPI server:

python -m uvicorn main:app --reload

Backend:

http://127.0.0.1:8000

FastAPI API documentation:

http://127.0.0.1:8000/docs

---

💻 Frontend Setup

Open another terminal.

Go to the frontend:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

Frontend:

http://localhost:5173

---

📁 Project Structure

SkillBridge/
│
├── backend/
│ ├── main.py
│ ├── auth.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── security.py
│ ├── student_model.py
│ ├── skill_model.py
│ ├── certificate_model.py
│ ├── internship_model.py
│ ├── application_model.py
│ └── requirements.txt
│
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ ├── App.jsx
│ │ └── main.jsx
│ ├── package.json
│ └── README.md
│
├── .gitignore
└── README.md

«The "venv/" directory is used locally and should not be committed to the repository.»

---

🔄 Application Flow

Student

Student
   ↓
Register / Login
   ↓
Student Dashboard
   ├── Profile
   ├── Skills
   ├── Certificates
   ├── Internships
   └── Applications

Admin

Admin
   ↓
Admin Login
   ↓
Admin Dashboard
   ├── Internship Management
   ├── Application Management
   └── Statistics

---

🎯 Project Goals

SkillBridge was developed to demonstrate practical experience with:

- Full-stack web development
- React application development
- REST API development
- FastAPI
- MySQL database design
- SQLAlchemy ORM
- Authentication and authorization
- Role-based access control
- CRUD operations
- Git and GitHub
- Frontend and backend integration

---

📌 Project Status

SkillBridge is an actively developed portfolio project.

The core authentication, student management, internship, application, and administration functionality has been implemented. Additional improvements such as advanced filtering, analytics, UI refinement, testing, and deployment can be added as the project continues to evolve.

---

👩‍💻 Author

Nawoda Hansanee

Software Engineering Student (HNDIT)

GitHub:
https://github.com/nawoda27

LinkedIn:
https://www.linkedin.com/in/nawodahansanee

---

⭐ Repository

GitHub Repository:
https://github.com/nawoda27/SkillBridge
