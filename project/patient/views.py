import os,sys,subprocess,platform
import pdfkit
from numpy import genfromtxt
import csv
from flask import send_file,make_response,flash,Blueprint,render_template, redirect,url_for,request,session,abort
from project import db,app
from flask_cors import CORS
from project import ALLOWED_EXTENSIONS
from project.patient.models import Patient,Vitals
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
            firstname = request.form['firstname'].strip().capitalize()
            middlename= request.form['middlename'].strip().capitalize()
            lastname = request.form['lastname'].strip().capitalize()
            dateofbirth = request.form['dateofbirth']
            sex = request.form['sex']
            maritalstatus = request.form['maritalstatus']
            address = request.form['address']
            city = request.form['city']
            region = request.form['region']
            phone = request.form['phone']
            dateofbirth = datetime.strptime(dateofbirth,'%Y-%m-%d')
            emergencyName = request.form['emergencyName'].strip().capitalize()
            relationship = request.form['relationship']
            emergencyPhone = request.form['emergencyPhone']
            emergencyEmail = request.form['emergencyEmail']
            email = request.form['email']
            newPatient = Patient(firstname,middlename,lastname)
            newPatient.dateofbirth = dateofbirth
            newPatient.sex = sex
            newPatient.email = email
            newPatient.relationshiptoemergencycontact = relationship
            newPatient.patientDate = datetime.utcnow()
            newPatient.maritalstatus = maritalstatus
            newPatient.phone = phone
            newPatient.emergencyName = emergencyName
            newPatient.emergencyPhone = emergencyPhone
            newPatient.emergencyEmail = emergencyEmail
            newPatient.city = city
            newPatient.address = address
            newPatient.region = region
            db.session.add(newPatient)
            db.session.commit()
            text = 'New Patient with name ' + str(newPatient.firstname) + ' ' + (newPatient.middlename) + ' ' + (newPatient.lastname) + ' added successfully to Natural Solutions Herbal Clinic!'
            flash(text)
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
            patientVitals.calculatedBMI = round((weight/height/height),3)
            patientVitals.pulse = pulse
            patientVitals.pulseOximeter = pulseOximeter
            patientVitals.temperature = temperature
            patientVitals.respiratoryRate = respiratoryRate
            patientVitals.bloodPressureone = bloodPressureone
            patientVitals.bloodPressuretwo = bloodPressuretwo
            patientVitals.vitalsTime = datetime.utcnow()
            db.session.add(patientVitals)
            db.session.commit()
            patient = Patient.query.get(patientCode)
            text = 'Vitals of ' + str(patient.firstname) + ' ' + (patient.middlename) + ' ' + (patient.lastname) + ' recorded successfully!'
            flash(text)
            return redirect (url_for('patient.captureVitals'))
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
  messages = 'View All Patients In The System'
  all_patients = Patient.query.order_by(desc(Patient.id)).all()
  if request.method == 'POST':
      all_patients = Patient.query.order_by(desc(Patient.id)).all()
      for x in all_patients:
          id = {}
          id['edit'] = 'edit'+str(x.id)
          id['delete'] = 'delete'+str(x.id)
          if request.form['submit'] == id['edit']:
              session['id_edit'] = x.id
              return redirect (url_for('patient.editPatient',id=x.id))
          elif request.form['submit']==id['delete']:
              session['id_delete'] = x.id
              return redirect(url_for('patient.deletePatient',id=x.id))
          else:
              pass
  else:
      pass
  return render_template('viewPatients.html',title=title, messages=messages,all_patients=all_patients)


@patient_blueprint.route('/edit/<id>',methods = ['GET','POST'])
#@login_required
def editPatient (id):
  title = 'Natural Solutions Herbal Clinic | Edit Patient'
  messages = ''
  messages = 'Edit Patient messages to popup'
  patient = Patient.query.get(id)
  success = 0
  age = '0'
  try:
      id = int(id)
      if Patient.query.get(id)==None:
          messages = 'No existing patient in database with this ID: ' + str(id)
          success = 0
          age = '0'
      else:
          patient = Patient.query.get(id)
          success = 1
          age = relativedelta(date.today(),patient.dateofbirth)
          if age.years == 0:
              age = str(age.months) + ' months'
          else:
              age = str(age.years) + ' years'
          messages = 'Please you are editing details of ' + str(patient.firstname) + ' ' + (patient.middlename) + ' ' + (patient.lastname)
  except:
      messages = 'Please check the ID entered!'
  if request.method == 'POST':
      if request.form['submit'] == 'editPatient':
          id = int(id)
          patient = Patient.query.get(id)
          firstname = request.form['firstname'].strip().capitalize()
          middlename= request.form['middlename'].strip().capitalize()
          lastname = request.form['lastname'].strip().capitalize()
          dateofbirth = request.form['dateofbirth']
          dateofbirth = datetime.strptime(dateofbirth,'%Y-%m-%d')
          sex = request.form['sex']
          maritalstatus = request.form['maritalstatus']
          address = request.form['address']
          city = request.form['city']
          region = request.form['region']
          phone = request.form['phone']
          emergencyName = request.form['emergencyName'].strip().capitalize()
          relationship = request.form['relationship']
          emergencyPhone = request.form['emergencyPhone']
          emergencyEmail = request.form['emergencyEmail']
          email = request.form['email']
          patient.firstname = firstname
          patient.middlename = middlename
          patient.lastname = lastname
          patient.dateofbirth = dateofbirth
          patient.sex = sex
          patient.relationshiptoemergencycontact = relationship
          patient.email = email
          patient.maritalstatus = maritalstatus
          patient.phone = phone
          patient.emergencyName = emergencyName
          patient.emergencyPhone = emergencyPhone
          patient.emergencyEmail = emergencyEmail
          patient.city = city
          patient.address = address
          patient.region = region
          #patient.status = status
          db.session.add(patient)
          db.session.commit()
          return redirect (url_for('patient.viewPatients'))
          text = 'Detail change of ' + str(patient.firstname) + ' ' + (patient.middlename) + ' ' + (patient.lastname) + ' successful!'
          flash(text)
      else:
          pass
  else:
      pass
  return render_template('editPatient.html',success=success,patient=patient,title=title, age=age,messages=messages, id=id)


@patient_blueprint.route('/delete/<id>',methods = ['GET','POST'])
#@login_required
def deletePatient (id):
  title = 'Natural Solutions Herbal Clinic | Delete Patient'
  messages = ''
  messages = 'Delete patient messages to popup'
  try:
      id = int(id)
      if Patient.query.get(id)==None:
          messages = 'No existing patient in database with this ID: ' + str(id)
          patient = None
      else:
          patient = Patient.query.get(id)
          messages = 'Please you are about deleting ' + str(patient.firstname) + ' ' + (patient.middlename) + ' ' + (patient.lastname) + ' from the database, please this action is irreversible, thank you!'
  except:
      messages = 'Please check the ID entered!'
      patient = None
  if request.method == 'POST':
      if request.form['submit'] == 'deletePatient':
          patient = Patient.query.get(id)
          try:
             id = int(id)
             patient = Patient.query.get(id)
             db.session.delete(patient)
             db.session.commit()
             text = 'Deletion successful!'
             flash(text)
             return redirect(url_for('patient.viewPatients'))
          except:
              text = 'Please check the ID entered!'
              flash(text)
      else:
          pass
  else:
      pass
  return render_template('deletePatient.html',title=title, messages=messages, id=id,patient=patient)
