from sqlalchemy.orm import relationship
from project import db,login_manager
from sqlalchemy.orm import backref
from datetime import date
from datetime import datetime
from sqlalchemy import join
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user (user_id):
    return Staff.query.get(user_id)

class Staff (db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(64),nullable=False)
    lastname = db.Column(db.String(64),nullable=False)
    username = db.Column(db.String(64),unique=True,index=True)
    privilege_column = db.Column(db.Integer)
    password_hash = db.Column(db.String(200))
    contact = db.Column(db.String(15),nullable = False)
    dateofbirth = db.Column(db.Date)
    staffidnumber = db.Column(db.String(20),unique=True,nullable=False)
    staff_appointment_id = db.Column(db.Integer,db.ForeignKey('appointment.id'))
    doctor_appointment_id = db.Column(db.Integer,db.ForeignKey('appointment.id'))
    gender = db.Column(db.String(10),nullable=False)
    qualification = db.Column(db.String(200))
    role = db.Column(db.String(30),nullable=False)
    emergency_contact = db.Column(db.String(15),nullable=False)
    dateofstart = db.Column(db.Date)
    position = db.Column(db.String(60),nullable=False)
    relationshiptoemergency_contact = db.Column(db.String(50))
    specialization = db.Column(db.String(200))
    def __init__(self, username,password,privilege_column):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.privilege_column = privilege_column
    def check_password(self,password):
        return check_password_hash (self.password_hash,password)
