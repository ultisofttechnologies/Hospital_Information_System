from sqlalchemy.orm import relationship
from project import db,login_manager
from sqlalchemy.orm import backref
from datetime import date
from datetime import datetime
from sqlalchemy import join
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from project.staff.models import Staff
#from project.imaging.models import LabResults

class Patient (db.Model):
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(30),nullable=False)
    lastname = db.Column(db.String(30),nullable=False)
    middlename = db.Column(db.String(30),nullable=False)
    dateofbirth = db.Column(db.Date,nullable=False)
    maritalstatus = db.Column(db.String(15),nullable=False)
    phone = db.Column(db.String(15))
    patientDate = db.Column(db.DateTime,nullable=False)
    city = db.Column(db.String(30))
    address = db.Column(db.String(50))
    region = db.Column(db.String(50))
    email = db.Column(db.String(30))
    vitals_id = db.Column(db.Integer,db.ForeignKey('vitals.id'))
    lab_results_id = db.Column(db.Integer,db.ForeignKey('labresults.id'))
    appointment_id = db.Column(db.Integer,db.ForeignKey('appointment.id'))
    emergencyName = db.Column(db.String(30),nullable=False)
    emergencyPhone = db.Column(db.String(15),nullable=False)
    relationshiptoemergencycontact = db.Column(db.String(15))
    emergencyEmail = db.Column(db.String(25))
    sex = db.Column(db.String(10),nullable=False)
    status = db.Column(db.String(10))
    def __init__(self, firstname,middlename,lastname):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname

class Vitals(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    patient_id = db.Column(db.Integer,db.ForeignKey('patient.id'),nullable=False)
    staff_id = db.Column(db.Integer,db.ForeignKey('staff.id'),nullable=False)
    weight = db.Column(db.Float(10),nullable=False)
    height = db.Column(db.Float(10),nullable=False)
    pulse = db.Column(db.Float(10),nullable=False)
    respiratoryRate = db.Column(db.Float(10),nullable=False)
    bloodPressureone = db.Column(db.Float(10),nullable=False)
    bloodPressuretwo = db.Column(db.Float(10),nullable=False)
    pulseOximeter = db.Column(db.Float(10),nullable=False)
    calculatedBMI = db.Column(db.Float(10),nullable=False)
    vitalsTime = db.Column(db.DateTime,nullable=False)
    def __init__(self, patient_id,staff_id):
        self.patient_id = patient_id
        self.staff_id = staff_id

class Appointment (db.Model):
    id = db.Column(db.Integer,primary_key=True)
    patient_id = db.Column(db.Integer,db.ForeignKey('patient.id'),nullable=False)
    staff_id = db.Column(db.Integer,db.ForeignKey('staff.id'),nullable=False)
    doctor_id = db.Column(db.Integer,db.ForeignKey('staff.id'),nullable=False)
    booking_time = db.Column(db.DateTime,nullable=False)
    appointment_time = db.Column(db.DateTime,nullable=False)
    status = db.Column(db.Integer)
    note = db.Column(db.String(250))
    type = db.Column(db.String(50))
    def __init__(self, patient_id,doctor_id,staff_id,booking_time,appointment_time,status,note):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.staff_id = staff_id
        self.booking_time = booking_time
        self.appointment_time = appointment_time
        self.status = status
        self.note = note

class Charges (db.Model):
    id = db.Column(db.Integer,primary_key=True)
    patient_id = db.Column(db.Integer,db.ForeignKey('patient.id'),nullable=False)
    staff_id = db.Column(db.Integer,db.ForeignKey('staff.id'),nullable=False)
