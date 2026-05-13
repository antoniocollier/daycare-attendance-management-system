from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from init_db import initialize_database
import sqlite3
import os
from datetime import date

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key_change_later")

initialize_database()


def get_db_connection():
    conn = sqlite3.connect("daycare.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_today_counts(conn, today_str):
    present_today = conn.execute("""
        SELECT COUNT(DISTINCT child_id) AS count
        FROM attendance
        WHERE date = ? AND status = 'Present'
    """, (today_str,)).fetchone()["count"]

    absent_today = conn.execute("""
        SELECT COUNT(DISTINCT child_id) AS count
        FROM attendance
        WHERE date = ? AND status = 'Absent'
    """, (today_str,)).fetchone()["count"]

    return present_today, absent_today


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            elif user["role"] == "teacher":
                return redirect(url_for("teacher_dashboard"))
            elif user["role"] == "parent":
                return redirect(url_for("parent_dashboard"))

        flash("Incorrect username or password.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/admin")
def admin_dashboard():
    if "role" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()

    total_children = conn.execute(
        "SELECT COUNT(*) AS count FROM children"
    ).fetchone()["count"]

    total_parents = conn.execute(
        "SELECT COUNT(*) AS count FROM users WHERE role = 'parent'"
    ).fetchone()["count"]

    today_str = date.today().isoformat()
    present_today, absent_today = get_today_counts(conn, today_str)

    recent_children = conn.execute("""
        SELECT children.*, users.username AS parent_username
        FROM children
        LEFT JOIN users ON children.parent_user_id = users.id
        ORDER BY children.id DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        username=session["username"],
        role=session["role"],
        total_children=total_children,
        total_parents=total_parents,
        present_today=present_today,
        absent_today=absent_today,
        recent_children=recent_children,
        today_str=today_str
    )


@app.route("/teacher")
def teacher_dashboard():
    if "role" not in session or session["role"] != "teacher":
        return redirect(url_for("login"))

    conn = get_db_connection()

    total_children = conn.execute(
        "SELECT COUNT(*) AS count FROM children"
    ).fetchone()["count"]

    today_str = date.today().isoformat()
    present_today, absent_today = get_today_counts(conn, today_str)

    children = conn.execute("SELECT * FROM children ORDER BY name").fetchall()

    conn.close()

    return render_template(
        "teacher_dashboard.html",
        username=session["username"],
        role=session["role"],
        total_children=total_children,
        present_today=present_today,
        absent_today=absent_today,
        today_str=today_str,
        children=children
    )


@app.route("/parent")
def parent_dashboard():
    if "role" not in session or session["role"] != "parent":
        return redirect(url_for("login"))

    conn = get_db_connection()

    child = conn.execute("""
        SELECT * FROM children
        WHERE parent_user_id = ?
        ORDER BY id
        LIMIT 1
    """, (session["user_id"],)).fetchone()

    attendance_count = 0
    present_count = 0
    absent_count = 0

    if child:
        attendance_count = conn.execute(
            "SELECT COUNT(*) AS count FROM attendance WHERE child_id = ?",
            (child["id"],)
        ).fetchone()["count"]

        present_count = conn.execute(
            "SELECT COUNT(*) AS count FROM attendance WHERE child_id = ? AND status = 'Present'",
            (child["id"],)
        ).fetchone()["count"]

        absent_count = conn.execute(
            "SELECT COUNT(*) AS count FROM attendance WHERE child_id = ? AND status = 'Absent'",
            (child["id"],)
        ).fetchone()["count"]

    conn.close()

    return render_template(
        "parent_dashboard.html",
        username=session["username"],
        role=session["role"],
        child=child,
        attendance_count=attendance_count,
        present_count=present_count,
        absent_count=absent_count
    )


@app.route("/admin/children", methods=["GET", "POST"])
def manage_children():
    if "role" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        name = request.form["name"]
        date_of_birth = request.form["date_of_birth"]
        grade = request.form["grade"]
        age = request.form["age"]
        schedule_type = request.form["schedule_type"]
        parent_user_id = request.form["parent_user_id"]
        parent_name = request.form["parent_name"]
        parent_address = request.form["parent_address"]
        parent_phone = request.form["parent_phone"]
        emergency_contact = request.form["emergency_contact"]
        immunization_status = request.form["immunization_status"]

        if parent_user_id.strip() == "":
            parent_user_id = None

        conn.execute("""
            INSERT INTO children
            (name, date_of_birth, grade, age, schedule_type, parent_user_id, parent_name, parent_address, parent_phone, emergency_contact, immunization_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, date_of_birth, grade, age, schedule_type, parent_user_id,
            parent_name, parent_address, parent_phone, emergency_contact, immunization_status
        ))
        conn.commit()
        conn.close()
        flash("Child added successfully.")
        return redirect(url_for("manage_children"))

    children = conn.execute("""
        SELECT children.*, users.username AS parent_username
        FROM children
        LEFT JOIN users ON children.parent_user_id = users.id
        ORDER BY children.id
    """).fetchall()

    parents = conn.execute(
        "SELECT id, username FROM users WHERE role = 'parent' ORDER BY username"
    ).fetchall()

    conn.close()
    return render_template(
        "manage_children.html",
        children=children,
        parents=parents,
        username=session["username"],
        role=session["role"]
    )


@app.route("/admin/edit_child/<int:child_id>", methods=["GET", "POST"])
def edit_child(child_id):
    if "role" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        name = request.form["name"]
        date_of_birth = request.form["date_of_birth"]
        grade = request.form["grade"]
        age = request.form["age"]
        schedule_type = request.form["schedule_type"]
        parent_user_id = request.form["parent_user_id"]
        parent_name = request.form["parent_name"]
        parent_address = request.form["parent_address"]
        parent_phone = request.form["parent_phone"]
        emergency_contact = request.form["emergency_contact"]
        immunization_status = request.form["immunization_status"]

        if parent_user_id.strip() == "":
            parent_user_id = None

        conn.execute("""
            UPDATE children
            SET name = ?, date_of_birth = ?, grade = ?, age = ?, schedule_type = ?,
                parent_user_id = ?, parent_name = ?, parent_address = ?, parent_phone = ?,
                emergency_contact = ?, immunization_status = ?
            WHERE id = ?
        """, (
            name, date_of_birth, grade, age, schedule_type,
            parent_user_id, parent_name, parent_address, parent_phone,
            emergency_contact, immunization_status, child_id
        ))
        conn.commit()
        conn.close()
        flash("Child updated successfully.")
        return redirect(url_for("manage_children"))

    child = conn.execute(
        "SELECT * FROM children WHERE id = ?",
        (child_id,)
    ).fetchone()

    parents = conn.execute(
        "SELECT id, username FROM users WHERE role = 'parent' ORDER BY username"
    ).fetchall()

    conn.close()

    if child is None:
        flash("Child not found.")
        return redirect(url_for("manage_children"))

    return render_template(
        "edit_child.html",
        child=child,
        parents=parents,
        username=session["username"],
        role=session["role"]
    )


@app.route("/admin/delete_child/<int:child_id>")
def delete_child(child_id):
    if "role" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()
    conn.execute("DELETE FROM children WHERE id = ?", (child_id,))
    conn.commit()
    conn.close()

    flash("Child deleted successfully.")
    return redirect(url_for("manage_children"))


@app.route("/attendance", methods=["GET", "POST"])
def mark_attendance():
    if "role" not in session or session["role"] not in ["admin", "teacher"]:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        date_value = request.form["date"]
        children = conn.execute("SELECT * FROM children ORDER BY name").fetchall()

        for child in children:
            status = request.form.get(f"status_{child['id']}")
            check_in_time = request.form.get(f"checkin_{child['id']}")
            check_out_time = request.form.get(f"checkout_{child['id']}")

            if status:
                existing = conn.execute(
                    "SELECT * FROM attendance WHERE child_id = ? AND date = ?",
                    (child["id"], date_value)
                ).fetchone()

                if existing:
                    conn.execute("""
                        UPDATE attendance
                        SET status = ?, check_in_time = ?, check_out_time = ?
                        WHERE child_id = ? AND date = ?
                    """, (status, check_in_time, check_out_time, child["id"], date_value))
                else:
                    conn.execute("""
                        INSERT INTO attendance (child_id, date, status, check_in_time, check_out_time)
                        VALUES (?, ?, ?, ?, ?)
                    """, (child["id"], date_value, status, check_in_time, check_out_time))

        conn.commit()
        conn.close()
        flash("Attendance saved successfully.")
        return redirect(url_for("mark_attendance"))

    children = conn.execute("SELECT * FROM children ORDER BY name").fetchall()
    conn.close()
    return render_template(
        "mark_attendance.html",
        children=children,
        username=session["username"],
        role=session["role"]
    )


@app.route("/history")
def attendance_history():
    if "role" not in session or session["role"] not in ["admin", "teacher"]:
        return redirect(url_for("login"))

    conn = get_db_connection()
    records = conn.execute("""
        SELECT attendance.date, attendance.status, attendance.check_in_time, attendance.check_out_time,
               children.name AS child_name, children.grade, children.schedule_type
        FROM attendance
        JOIN children ON attendance.child_id = children.id
        ORDER BY attendance.date DESC, children.name ASC
    """).fetchall()
    conn.close()

    return render_template(
        "staff_history.html",
        records=records,
        username=session["username"],
        role=session["role"]
    )


@app.route("/parent/history")
def parent_history():
    if "role" not in session or session["role"] != "parent":
        return redirect(url_for("login"))

    conn = get_db_connection()

    child = conn.execute("""
        SELECT * FROM children
        WHERE parent_user_id = ?
        ORDER BY id
        LIMIT 1
    """, (session["user_id"],)).fetchone()

    attendance_records = []
    if child:
        attendance_records = conn.execute("""
            SELECT date, status, check_in_time, check_out_time
            FROM attendance
            WHERE child_id = ?
            ORDER BY date DESC
        """, (child["id"],)).fetchall()

    conn.close()
    return render_template(
        "attendance_history.html",
        child=child,
        attendance_records=attendance_records,
        username=session["username"],
        role=session["role"]
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)