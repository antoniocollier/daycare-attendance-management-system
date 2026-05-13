# Daycare Attendance Management System

A browser-based daycare management application built with Python, Flask, SQLite, HTML, and CSS. The system allows daycare staff to manage child records, track attendance, view attendance history, and organize parent, emergency contact, immunization, and schedule information.

## Project Overview

This project was created as a Software Engineering class project and designed to solve a real-world daycare record management problem. The application uses role-based access so administrators, employees, and parents can view different information based on their responsibilities.

## Features

- Role-based login for administrators, employees, and parents
- Admin dashboard for managing daycare records
- Employee dashboard for attendance-related tasks
- Parent dashboard for viewing child information
- Child profile management
- Attendance tracking with date, check-in time, and check-out time
- Attendance history for children and staff
- Parent and emergency contact information
- Immunization status tracking
- Schedule type tracking
- SQLite database with database initialization script

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Git and GitHub

## Screenshots

### Login Page
![Login Page](screenshots/login.png)

### Admin Dashboard
![Admin Dashboard](screenshots/admin-dashboard.png)

### Manage Children Form
![Manage Children Form](screenshots/manage-children-form.png)

### Manage Children List
![Manage Children List](screenshots/manage-children-list.png)

### Mark Attendance
![Mark Attendance](screenshots/mark-attendance.png)

### Parent Dashboard
![Parent Dashboard](screenshots/parent-dashboard.png)

## User Roles

### Administrator

Administrators can manage child records, view attendance history, and access daycare management features.

### Employee

Employees can mark attendance, view assigned attendance information, and access staff-related dashboard features.

### Parent

Parents can view information related to their child, including attendance records and daycare profile information.

## How to Run Locally

1. Clone the repository or download the project folder.
2. Open the project folder in VS Code or another code editor.
3. Create and activate a virtual environment.
4. Install Flask.
5. Run the database setup file.
6. Start the Flask application.

```bash
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install flask
python init_db.py
python app.py
```

Then open the application in your browser:

```text
http://127.0.0.1:5000
```

## Demo Accounts

| Role | Username | Password |
|---|---|---|
| Admin | admin1 | admin123 |
| Employee | teacher1 | teach123 |
| Parent 1 | parent1 | parent123 |
| Parent 2 | parent2 | parent234 |
| Parent 3 | parent3 | parent345 |

## Project Structure

```text
daycare_project/
│
├── app.py
├── init_db.py
├── README.md
├── .gitignore
│
├── screenshots/
│   ├── login.png
│   ├── admin-dashboard.png
│   ├── manage-children-form.png
│   ├── manage-children-list.png
│   ├── mark-attendance.png
│   └── parent-dashboard.png
│
├── static/
│   └── style.css
│
└── templates/
    ├── admin_dashboard.html
    ├── admin_history.html
    ├── attendance_history.html
    ├── edit_child.html
    ├── login.html
    ├── manage_children.html
    ├── mark_attendance.html
    ├── parent_dashboard.html
    ├── staff_history.html
    ├── teacher_dashboard.html
    └── teacher_history.html
```

## Database Setup

The `daycare.db` file is not included in the repository because it is generated locally. To create the database, run:

```bash
python init_db.py
```

This creates the SQLite database and sample records needed to test the application.

## Security Note

This project is currently designed for local development and demonstration purposes. Future improvements would include password hashing, stronger authentication, environment variables, and production database support before using the system in a real daycare setting.

## Future Improvements

- Deploy the application online
- Add password hashing for improved security
- Improve the user interface for mobile devices
- Add PostgreSQL support for production deployment
- Add admin reporting features
- Add downloadable forms for parent and immunization records
- Add cloud deployment using AWS or another hosting platform

## Author

Antonio Collier  
Management Information Systems Student  
GitHub: github.com/antoniocollier