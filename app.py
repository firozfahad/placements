from flask import Flask, render_template, request, redirect
from models import db, Student, Company, Drive, Application

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


# --------------------------------
# Home Page
# --------------------------------
@app.route("/")
def home():
    return redirect("/register_student")


# --------------------------------
# Student Registration
# --------------------------------
@app.route("/register_student", methods=["GET", "POST"])
def register_student():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        student = Student(
            name=name,
            email=email,
            password=password
        )

        db.session.add(student)
        db.session.commit()

        return "Student Registered Successfully!"

    return render_template("register_student.html")


# --------------------------------
# Company Registration
# --------------------------------
@app.route("/register_company", methods=["GET", "POST"])
def register_company():

    if request.method == "POST":

        company_name = request.form["company_name"]
        email = request.form["email"]
        password = request.form["password"]

        company = Company(
            company_name=company_name,
            email=email,
            password=password
        )

        db.session.add(company)
        db.session.commit()

        return "Company Registered! Waiting for Admin Approval."

    return render_template("register_company.html")


# --------------------------------
# Admin Dashboard
# --------------------------------
@app.route("/admin_dashboard")
def admin_dashboard():

    companies = Company.query.all()

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = Drive.query.count()
    total_applications = Application.query.count()

    return render_template(
        "admin_dashboard.html",
        companies=companies,
        total_students=total_students,
        total_companies=total_companies,
        total_drives=total_drives,
        total_applications=total_applications
    )


# --------------------------------
# Approve Company
# --------------------------------
@app.route("/approve_company/<int:id>")
def approve_company(id):

    company = Company.query.get(id)
    company.approval_status = "approved"

    db.session.commit()

    return redirect("/admin_dashboard")


# --------------------------------
# Reject Company
# --------------------------------
@app.route("/reject_company/<int:id>")
def reject_company(id):

    company = Company.query.get(id)
    company.approval_status = "rejected"

    db.session.commit()

    return redirect("/admin_dashboard")


# --------------------------------
# Create Placement Drive
# --------------------------------
@app.route("/create_drive", methods=["GET", "POST"])
def create_drive():

    if request.method == "POST":

        company_id = request.form["company_id"]
        job_title = request.form["job_title"]
        deadline = request.form["deadline"]

        drive = Drive(
            company_id=company_id,
            job_title=job_title,
            deadline=deadline
        )

        db.session.add(drive)
        db.session.commit()

        return "Placement Drive Created Successfully!"

    return render_template("create_drive.html")


# --------------------------------
# View Placement Drives
# --------------------------------
@app.route("/view_drives")
def view_drives():

    drives = Drive.query.all()

    return render_template(
        "view_drives.html",
        drives=drives
    )


# --------------------------------
# Apply for Drive
# --------------------------------
@app.route("/apply_drive/<int:drive_id>")
def apply_drive(drive_id):

    student_id = 1   # temporary login

    existing_application = Application.query.filter_by(
        student_id=student_id,
        drive_id=drive_id
    ).first()

    if existing_application:
        return "You have already applied for this drive."

    application = Application(
        student_id=student_id,
        drive_id=drive_id
    )

    db.session.add(application)
    db.session.commit()

    return "Application Submitted Successfully!"


# --------------------------------
# Student Dashboard
# --------------------------------
@app.route("/student_dashboard")
def student_dashboard():

    student_id = 1

    applications = Application.query.filter_by(
        student_id=student_id
    ).all()

    drives = []

    for app_data in applications:
        drive = Drive.query.get(app_data.drive_id)
        drives.append(drive)

    return render_template(
        "student_dashboard.html",
        drives=drives
    )


# --------------------------------
# Company View Applications
# --------------------------------
@app.route("/company_applications/<int:drive_id>")
def company_applications(drive_id):

    applications = Application.query.filter_by(
        drive_id=drive_id
    ).all()

    students = []

    for app_data in applications:
        student = Student.query.get(app_data.student_id)
        students.append(student)

    return render_template(
        "company_applications.html",
        students=students
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form["role"]

        if role == "student":
            return redirect("/student_dashboard")
        elif role == "company":
            return redirect("/company_dashboard")
        elif role == "admin":
            return redirect("/admin_dashboard")

    return render_template("login.html")

@app.route("/company_dashboard")
def company_dashboard():

    company_id = 1  # temporary login

    drives = Drive.query.filter_by(company_id=company_id).all()

    return render_template("company_dashboard.html", drives=drives)
# --------------------------------
# blacjklisted
# --------------------------------

@app.route("/blacklist_student/<int:id>")
def blacklist_student(id):

    student = Student.query.get(id)
    student.is_blacklisted = True

    db.session.commit()

    return redirect("/admin_dashboard")

# --------------------------------
# Run Server
# --------------------------------
if __name__ == "__main__":
    app.run(debug=True)