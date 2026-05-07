# Daycare Attendance Management System

A web-based daycare attendance management system built for a Software Engineering class project.

## Features
- Role-based login
- Admin dashboard
- Employee dashboard
- Parent dashboard
- Manage children records
- Attendance tracking with date and check-in/check-out times
- Attendance history
- Parent and emergency contact information
- Immunization status tracking
- Schedule type tracking

## Technologies Used
- Python
- Flask
- SQLite
- HTML
- CSS

## How to Run
1. Open the project folder
2. Create and activate a virtual environment
3. Install Flask
4. Run the database setup
5. Run the Flask app

```bash
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install flask
python init_db.py
python app.py

Then open:
http://127.0.0.1:5000
