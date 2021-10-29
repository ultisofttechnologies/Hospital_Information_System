from sqlalchemy.orm import relationship
from project import db,login_manager
from sqlalchemy.orm import backref
from datetime import date
from datetime import datetime
from sqlalchemy import join
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


class Patient (db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False)
    date_of_birth = db.Column(db.Date,nullable=False)
    marital_status = db.Column(db.String(15))
    patient_contact = db.Column(db.String(15))
    emergency_contact = db.Column(db.String(15))
    relationship_to_emergency_contact = db.Column(db.String(15))
    gender = db.Column(db.String(10))
    nhis_number = db.Column(db.String(30))
    def __init__(self, name,date_of_birth,marital_status):
        self.name = name
        self.date_of_birth = date_of_birth
        self.marital_status = marital_status
