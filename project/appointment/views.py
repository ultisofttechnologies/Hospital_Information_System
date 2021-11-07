import os,sys,subprocess,platform
import pdfkit
from numpy import genfromtxt
import csv
from flask import send_file,make_response,flash,Blueprint,render_template, redirect,url_for,request,session,abort
from project import db,app
from flask_cors import CORS
from project import ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
from project.staff.models import Staff
from project.patient.models import Appointment
from datetime import date,datetime,timedelta
from sqlalchemy import extract,text,func,and_,desc,asc
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user
from dotenv import load_dotenv
from itertools import filterfalse
from calendar import monthrange

appointment_blueprint = Blueprint('appointment',__name__,template_folder='templates/appointment',static_folder='static',static_url_path='/static/')

@appointment_blueprint.route('/new_appointment',methods = ['GET','POST'])
#@login_required
def newAppointment ():
  title = 'Natural Solutions Herbal Clinic | New Appointment'
  messages = ''
  messages = 'New Appointment'
  alldoctors = Staff.query.filter_by(role='Doctor').order_by(asc(Staff.firstname)).all()
  if request.method == 'POST':
      if request.form['submit'] == 'newAppointment':
          patientCode = int(request.form['patientCode'])
          doctor = int(request.form['doctordetails'])
          status = int(request.form['status'])
          note = request.form['note']
          appointmenttime = request.form['appointmenttime']
          appointmentdate = request.form['appointmentdate']
          appointmenttime = datetime.strptime(appointmenttime,'%H:%M:%S')
          appointmentdate = datetime.strptime(appointmentdate,'%Y-%m-%d')
          type = request.form['type']
          appointmenttime = datetime.datetime.combine(appointmentdate,appointmenttime)
          newAppointment = Appointment(patientCode,doctor,1,datetime.utcnow(),appointmenttime,status,note)
          newAppointment.type = type
          db.session.add(newAppointment)
          db.session.commit()
          doctor = Staff.query.get(doctor)
          text = 'Appointment with Dr. ' + doctor.firstname + ' ' + doctor.middlename + ' ' + doctor.lastname + ' ' + ' added successfully.'
          flash(text)
      else:
          pass
  else:
      pass
  return render_template('newAppointment.html',title=title,alldoctors=alldoctors)


@appointment_blueprint.route('/view_appointments',methods = ['GET','POST'])
#@login_required
def viewAppointments ():
  title = 'Natural Solutions Herbal Clinic | View Appointments'
  messages = ''
  messages = 'Showing most recent appointments ...'
  appointments = Appointment.query.order_by(desc(Appointment.booking_time)).all()
  if request.method == 'POST':
      appointments = Appointment.query.order_by(desc(Appointment.booking_time)).all()
      for x in appointments:
          id = {}
          id['edit'] = 'editAppointment'+str(x.id)
          id['delete'] = 'deleteAppointment'+str(x.id)
          if request.form['submit'] == id['edit']:
              session['id_edit'] = x.id
              return redirect (url_for('appointment.editAppointment',id=x.id))
          elif request.form['submit']==id['delete']:
              session['id_delete'] = x.id
              return redirect(url_for('appointment.deleteAppointment',id=x.id))
          else:
              pass
  else:
      pass
  return render_template('viewAppointments.html',appointments=appointments,title=title, messages=messages)

@appointment_blueprint.route('/edit/<id>',methods = ['GET','POST'])
#@login_required
def editAppointment (id):
  title = 'Natural Solutions Herbal Clinic | View Appointments'
  messages = ''
  messages = 'Edit appointments messages to popup'
  try:
      id = int(id)
      if Patient.query.get(id)==None:
          messages = 'No existing patient in database with this ID: ' + str(id)
      else:
          patient = Patient.query.get(id)
          messages = 'Please you are editing details of ' + str(patient.firstname) + ' ' + (patient.middlename) + ' ' + (patient.lastname)
  except:
      messages = 'Please check the ID entered!'
  return render_template('editAppointment.html',title=title, id=id, messages=messages)

@appointment_blueprint.route('/delete/<id>',methods = ['GET','POST'])
#@login_required
def deleteAppointment (id):
  title = 'Natural Solutions Herbal Clinic | Delete Appointments'
  messages = ''
  messages = 'Delete appointments messages to popup'
  return render_template('deleteAppointment.html',title=title, id=id, messages=messages)
