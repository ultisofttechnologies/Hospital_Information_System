from sqlalchemy.orm import relationship
from project import db,login_manager
from sqlalchemy.orm import backref
from datetime import date
from datetime import datetime
from sqlalchemy import join
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from project.staff.models import Staff
#from project.patient.models import Patient

class LabResults(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    patient_id = db.Column(db.Integer,db.ForeignKey('patient.id'),nullable=False)
    staff_id = db.Column(db.Integer,db.ForeignKey('staff.id'),nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    lab_date = db.Column(db.DateTime,nullable=False)
    lab_type = db.Column(db.String(100))
    def __init__(self,patient_id,staff_id,data,lab_date,lab_type ):
        self.patient_id = patient_id
        self.staff_id = staff_id
        self.data = data
        self.lab_date = lab_date
        self.lab_type = lab_type
