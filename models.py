from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    
    


class Company(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    approval_status = db.Column(db.String(20), default="pending")


class Drive(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    job_title = db.Column(db.String(100))
    deadline = db.Column(db.String(50))
    status = db.Column(db.String(20), default="pending")


class Application(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'))
    status = db.Column(db.String(20), default="Applied")