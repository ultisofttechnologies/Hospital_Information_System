import os,sys,subprocess,platform
import pdfkit
from numpy import genfromtxt
import csv
from flask import send_file,make_response,flash,Blueprint,render_template, redirect,url_for,request,session,abort
from project import db,app
from flask_cors import CORS
from project import ALLOWED_EXTENSIONS
from project.patient.models import Patient
from werkzeug.utils import secure_filename
from project.staff.models import Staff
from datetime import date,datetime,timedelta
from sqlalchemy import extract,text,func,and_,desc,asc
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user
from dotenv import load_dotenv
from itertools import filterfalse
from calendar import monthrange

patient_blueprint = Blueprint('patient',__name__,template_folder='templates/patient',static_folder='static',static_url_path='/static/')

@patient_blueprint.route('/add_patient',methods = ['GET','POST'])
#@login_required
def addPatient ():
    title = 'Natural Solutions Herbal Clinic | Add Patient'
    if request.method == 'POST':
        if request.form['submit'] == 'addPatient':
            firstname = request.form['firstname']
            middlename= request.form['middlename']
            lastname = request.form['lastname']
            dateofbirth = request.form['dateofbirth']
            sex = request.form['sex']
            maritalstatus = request.form['maritalstatus']
            address = request.form['address']
            city = request.form['city']
            region = request.form['region']
            phone = request.form['phone']
            emergencyName = request.form['emergencyName']
            relationship = request.form['relationship']
            emergencyPhone = request.form['emergencyPhone']
            emergencyEmail = request.form['emergencyEmail']
            newPatient = Patient(firstname,middlename,lastname)
            newPatient.dateofbirth = dateofbirth
            newPatient.sex = sex
            newPatient.maritalstatus = maritalstatus
            newPatient.phone = phone
            newPatient.emergencyName = emergencyName
            newPatient.emergencyPhone = emergencyPhone
            db.session.add(newPatient)
            db.session.commit()
        else:
            pass
    else:
        pass
    return render_template('newPatient.html',title=title)


@patient_blueprint.route('/capture_vitals',methods = ['GET','POST'])
#@login_required
def captureVitals ():
    title = 'Natural Solutions Herbal Clinic | Capture Vitals'
    all_patients = Patient.query.all()
    if request.method == 'POST':
        if request.form['submit'] == 'captureVitals':
            weight = float(request.form['weight'])
            height = float(request.form['height'])
            calculatedBMI = float(request.form['calculatedBMI'])
            pulse = float(request.form['pulse'])
            pulseOximeter = float(request.form['pulseOximeter'])
            temperature = float(request.form['temperature'])
            respiratoryRate = float(request.form['respiratoryRate'])
            bloodPressureone = float(request.form['bloodPressureone'])
            bloodPressuretwo = float(request.form['bloodPressuretwo'])
            pulseOximeter = float(request.form['pulseOximeter'])
            patientCode = int(request.form['patientCode'])
            patientVitals = Vitals(patientCode,1)
            patientVitals.weight = weight
            patientVitals.height = height
            patientVitals.calculatedBMI = calculatedBMI
            patientVitals.pulse = pulse
            patientVitals.pulseOximeter = pulseOximeter
            patientVitals.temperature = temperature
            patientVitals.respiratoryRate = respiratoryRate
            patientVitals.bloodPressureone = bloodPressureone
            patientVitals.bloodPressuretwo = bloodPressuretwo
            patientVitals.vitalsTime = datetime.utcnow()
            db.session.add(patientVitals)
            db.session.commit()
        else:
            pass
    else:
        pass
    return render_template('captureVitals.html',all_patients=all_patients,title=title)


@patient_blueprint.route('/view_patients',methods = ['GET','POST'])
#@login_required
def viewPatients ():
  title = 'Natural Solutions Herbal Clinic | View Patients'
  messages = ''
  messages = 'View Patients messages to popup'
  return render_template('viewPatients.html',title=title, messages=messages)


@patient_blueprint.route('/edit/<id>',methods = ['GET','POST'])
#@login_required
def editPatient (id):
  title = 'Natural Solutions Herbal Clinic | Edit Patient'
  messages = ''
  messages = 'Edit Patient messages to popup'
  return render_template('editPatient.html',title=title, messages=messages, id=id)


@patient_blueprint.route('/delete/<id>',methods = ['GET','POST'])
#@login_required
def deletePatient (id):
  title = 'Natural Solutions Herbal Clinic | Delete Patient'
  messages = ''
  messages = 'Delete patient messages to popup'
  return render_template('deletePatient.html',title=title, messages=messages, id=id)
